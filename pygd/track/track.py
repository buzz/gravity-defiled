from pygd.bike import Bike


class Track:
    COLLISION_TYPE = 10
    ELASTICITY = 0.5
    FRICTION = 3.0
    WIDTH = 0.0

    def __init__(self, name, points, start, finish_x):
        self.name = name
        self.points = points
        self.start = start
        self.finish_x = finish_x

    def get_start_line(self):
        bike_right = self.start[0] + Bike.WHEEL_R_POS[0] + Bike.WHEEL_RADIUS
        return self.find_point_to_the_right(bike_right)

    def get_finish_line(self):
        return self.find_point_to_the_right(self.finish_x)

    def find_point_to_the_right(self, x):
        return next(p for p in self.points if p[0] > x)

    def __repr__(self):
        return (
            f"<Track {self.name} point_count={len(self.points)} "
            f"start={self.start} finish={self.finish_x}>"
        )
