import pymunk


class Track:
    def __init__(self):
        self.segments = []

    @classmethod
    def from_points(cls, points, space):
        track = cls()
        friction = 1.0
        width = 0.0
        for idx in range(len(points) - 1):
            p1 = points[idx]
            p2 = points[idx + 1]
            segment = pymunk.Segment(space.static_body, p1, p2, width)
            segment.elasticity = 0.5
            segment.friction = friction
            track.segments.append(segment)
            space.add(segment)
        return track
