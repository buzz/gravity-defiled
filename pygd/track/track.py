class Track:
    elasticity = 0.5
    friction = 1.0
    width = 0.0

    def __init__(self, points, start, finish):
        self.points = points
        self.start = start
        self.finish = finish

    def __repr__(self):
        return (
            f"<Track point_count={len(self.points)} "
            f"start={self.start} finish={self.finish}>"
        )
