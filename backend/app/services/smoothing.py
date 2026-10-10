from dataclasses import replace


class PlacementSmoother:
    """Exponential smoothing of position, size and rotation to reduce landmark jitter.
    Higher alpha = snappier but jittery; lower = smoother but laggy."""
    def __init__(self, alpha: float = 0.6):
        self.alpha, self.prev = alpha, None

    def reset(self):
        self.prev = None

    def __call__(self, placements):
        if self.prev is None or len(self.prev) != len(placements):
            self.prev = placements
            return placements
        a, out = self.alpha, []
        for p, q in zip(placements, self.prev):
            d = (p.rotation - q.rotation + 180) % 360 - 180      # shortest turn, no 360 jumps
            out.append(replace(p, center=(q.center[0] + a * (p.center[0] - q.center[0]),
                                          q.center[1] + a * (p.center[1] - q.center[1])),
                               width=q.width + a * (p.width - q.width), rotation=q.rotation + a * d))
        self.prev = out
        return out
