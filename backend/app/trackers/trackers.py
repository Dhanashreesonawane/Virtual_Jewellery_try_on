"""Trackers turn one frame's landmarks into Placement(s). They hold no state; temporal
smoothing is done by PlacementSmoother so every frame is recalculated from landmarks."""
from ..processors import placements as P


class RingTracker:
    def __init__(self, finger: str = "ring_finger"):
        self.finger = finger

    def track(self, hand):
        return [P.ring_placement(hand, self.finger)]


class BangleTracker:
    def track(self, hand):
        return [P.bangle_placement(hand)]


class EarringTracker:
    def __init__(self, side: str = "both"):
        self.side = side

    def track(self, face):
        return P.earring_placements(face, self.side)


class NecklaceTracker:
    def track(self, pose, face=None):
        chin = face.pts[152] if face is not None else None
        return [P.necklace_placement(pose, chin)]


def describe(pl) -> dict:
    """Tracker output as JSON: {center, scale (px width), rotation, confidence}."""
    return {"center": [round(float(pl.center[0]), 1), round(float(pl.center[1]), 1)],
            "scale": round(float(pl.width), 1), "rotation": round(float(pl.rotation), 1),
            "confidence": round(float(pl.confidence), 3)}
