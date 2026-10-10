"""Landmarks -> Placement (ROI + scale + rotation) for each jewelry type.

Pure geometry on numpy arrays, so it is testable without MediaPipe.
"""
import numpy as np
from ..core import constants as C
from ..core.errors import AppError
from ..models.jewelry import Detection, Placement
from ..utils.geometry import angle_deg, dist, lerp, upright_rotation


def ring_placement(hand: Detection, anchor_type: str) -> Placement:
    """Ring sits midway between a finger's knuckle (MCP) and middle joint (PIP)."""
    mcp_i, pip_i = C.FINGERS.get(anchor_type, C.FINGERS["ring_finger"])
    p = hand.pts
    palm_w = dist(p[5], p[17])
    finger_w = palm_w / 4.0 * (1.25 if anchor_type == "thumb" else 1.0)
    direction = angle_deg(p[mcp_i], p[pip_i])
    return Placement(tuple(lerp(p[mcp_i], p[pip_i], 0.5)), finger_w * 1.05,
                     upright_rotation(direction), 0.5, hand.score, clip_pts=p)


def bangle_placement(hand: Detection) -> Placement:
    """Bangle is centred just past the wrist, along the forearm direction."""
    p = hand.pts
    forearm = p[0] - p[9]
    center = p[0] + 0.15 * forearm
    direction = angle_deg(p[0], p[9])
    return Placement(tuple(center), dist(p[5], p[17]) * 1.1,
                     upright_rotation(direction), 0.5, hand.score)


def earring_placements(face: Detection, side: str) -> list[Placement]:
    """Anchor below the cheek-edge landmarks (approximate ear-lobe position)."""
    p = face.pts
    left, right = p[C.FACE_LEFT_EDGE], p[C.FACE_RIGHT_EDGE]
    face_w, face_h = dist(left, right), dist(p[C.FACE_TOP], p[C.FACE_CHIN])
    if face_w < 1:
        raise AppError("NO_EAR_LANDMARKS", "No suitable ear landmarks were found.")
    down = (p[C.FACE_CHIN] - p[C.FACE_TOP]) / max(face_h, 1e-6)
    rot = -angle_deg(left, right)           # head roll
    out = []
    for name, pt in (("left", left), ("right", right)):
        if side in ("both", name):
            out.append(Placement(tuple(pt + 0.2 * face_h * down), face_w * 0.11,
                                 rot, 0.0, face.score))
    return out


def necklace_placement(pose: Detection, chin=None) -> Placement:
    """Neck base = point between mouth and shoulder midpoint; width from shoulders."""
    p = pose.pts
    ls, rs = sorted((p[C.POSE_SHOULDERS[0]], p[C.POSE_SHOULDERS[1]]), key=lambda q: q[0])
    mouth = (p[C.POSE_MOUTH[0]] + p[C.POSE_MOUTH[1]]) / 2
    # Face Mesh chin (if found) is a better top reference than the pose mouth points.
    neck = lerp(chin, (ls + rs) / 2, 0.5) if chin is not None else lerp(mouth, (ls + rs) / 2, 0.6)
    vis = pose.vis[[9, 10, 11, 12]].mean() if pose.vis is not None else pose.score
    if vis < 0.3:
        raise AppError("NO_POSE_DETECTED", "Shoulders and face must be visible.")
    return Placement(tuple(neck), dist(ls, rs) * 0.5, -angle_deg(ls, rs), 0.0, float(vis))
