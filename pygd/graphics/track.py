import pyglet

from pygd.graphics.poly_line import PolyLine


class Track:
    COLOR_TRACK = (0, 255, 0)
    LINE_WIDTH_TRACK = 1.0

    POLE_HEIGHT = 100
    COLOR_START = (255, 0, 0)
    COLOR_FINISH = (0, 0, 255)

    def __init__(self, batch, group):
        self.track_lines = PolyLine(
            [],
            width=self.LINE_WIDTH_TRACK,
            color=self.COLOR_TRACK,
            batch=batch,
            group=group,
        )
        self.start = pyglet.shapes.Line(
            *(4 * (0,)), color=self.COLOR_START, batch=batch, group=group
        )
        self.finish = pyglet.shapes.Line(
            *(4 * (0,)), color=self.COLOR_FINISH, batch=batch, group=group
        )

    def update(self, track):
        self.track_lines.update(track.points)
        self.start.x, self.start.y = track.start_line
        self.start.x2, self.start.y2 = track.start_line - (0, self.POLE_HEIGHT)
        self.finish.x, self.finish.y = track.finish_line
        self.finish.x2, self.finish.y2 = track.finish_line - (0, self.POLE_HEIGHT)
