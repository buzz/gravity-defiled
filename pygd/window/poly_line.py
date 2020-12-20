import pyglet.gl as gl


class PolyLine:
    def __init__(self, points, close=False, line_width=1.0, color=(0.0, 0.0, 0.0)):
        self.points = points
        self.close = close
        self.line_width = line_width
        self.color = color

    def draw(self):
        gl.glLineWidth(self.line_width)
        gl.glColor3ub(*self.color)
        gl.glBegin(gl.GL_LINE_LOOP if self.close else gl.GL_LINE_STRIP)
        for p in self.points:
            gl.glVertex3f(*p, 0)
        gl.glEnd()

    def update(self, points):
        self.points = points
