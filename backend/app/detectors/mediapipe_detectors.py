"""MediaPipe Hands / Face Mesh / Pose wrappers.

Models are created once and reused. `live=True` uses MediaPipe's video mode
(detect once, then track between frames) which is faster and smoother.
Live models keep tracking state, so this build assumes one live user at a time.
Calls are guarded by a lock because MediaPipe objects are not thread-safe.
"""
import threading
import numpy as np
from ..models.jewelry import Detection

_lock = threading.Lock()
_cache: dict = {}


def _solution(name: str, live: bool):
    key = (name, live)
    if key not in _cache:
        import mediapipe as mp  # lazy so tests/health work without it
        s, static = mp.solutions, not live
        _cache[key] = {
            "hands": lambda: s.hands.Hands(static_image_mode=static, max_num_hands=2,
                                           min_detection_confidence=0.5, min_tracking_confidence=0.5),
            "face": lambda: s.face_mesh.FaceMesh(static_image_mode=static, max_num_faces=1,
                                                 min_detection_confidence=0.5, min_tracking_confidence=0.5),
            "pose": lambda: s.pose.Pose(static_image_mode=static, model_complexity=0, smooth_landmarks=live,
                                        min_detection_confidence=0.5, min_tracking_confidence=0.5),
        }[name]()
    return _cache[key]


def _px(landmarks, w: int, h: int) -> np.ndarray:
    return np.array([[p.x * w, p.y * h] for p in landmarks], dtype=np.float32)


def detect_hands(rgb: np.ndarray, live: bool = False) -> list[Detection]:
    h, w = rgb.shape[:2]
    with _lock:
        res = _solution("hands", live).process(rgb)
    if not res.multi_hand_landmarks:
        return []
    scores = [c.classification[0].score for c in res.multi_handedness]
    return [Detection(_px(hl.landmark, w, h), float(s)) for hl, s in zip(res.multi_hand_landmarks, scores)]


def detect_face(rgb: np.ndarray, live: bool = False) -> Detection | None:
    h, w = rgb.shape[:2]
    with _lock:
        res = _solution("face", live).process(rgb)
    if not res.multi_face_landmarks:
        return None
    return Detection(_px(res.multi_face_landmarks[0].landmark, w, h), 1.0)


def detect_pose(rgb: np.ndarray, live: bool = False) -> Detection | None:
    h, w = rgb.shape[:2]
    with _lock:
        res = _solution("pose", live).process(rgb)
    if not res.pose_landmarks:
        return None
    lm = res.pose_landmarks.landmark
    vis = np.array([p.visibility for p in lm], dtype=np.float32)
    return Detection(_px(lm, w, h), float(vis.mean()), vis)
