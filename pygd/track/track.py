class Track:
    COLLISION_TYPE = 10
    ELASTICITY = 0.5
    FRICTION = 3.0
    WIDTH = 0.0

    def __init__(self, name, points, start, finish):
        self.name = name
        self.points = points
        self.start = start
        self.finish = finish

    def __repr__(self):
        return (
            f"<Track {self.name} point_count={len(self.points)} "
            f"start={self.start} finish={self.finish}>"
        )
