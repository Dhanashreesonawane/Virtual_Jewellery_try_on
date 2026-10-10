CATEGORIES = ("ring", "bangle", "earring", "necklace")
ALLOWED_TYPES = {"image/jpeg", "image/png"}
# MediaPipe Hands: (MCP, PIP) landmark indices per finger
FINGERS = {"thumb": (2, 3), "index_finger": (5, 6), "middle_finger": (9, 10),
           "ring_finger": (13, 14), "pinky": (17, 18)}
# MediaPipe Face Mesh
FACE_LEFT_EDGE, FACE_RIGHT_EDGE, FACE_TOP, FACE_CHIN = 234, 454, 10, 152
# MediaPipe Pose
POSE_MOUTH = (9, 10)
POSE_SHOULDERS = (11, 12)
