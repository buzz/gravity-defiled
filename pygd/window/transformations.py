import pyglet.gl as gl


class BaseGlTransformation:
    def __init__(self, win):
        self.win = win

    def begin(self):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError

    def __enter__(self):
        self.begin()

    def __exit__(self, *_):
        self.end()


class ToPymunkCoords(BaseGlTransformation):
    def begin(self):
        gl.glPushMatrix()
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glTranslatef(0.0, -self.win.height, 0.0)

    def end(self):
        gl.glPopMatrix()


class WorldCamera(BaseGlTransformation):
    def begin(self):
        gl.glPushMatrix()
        bike = self.win.game.bike
        if bike:
            pos = bike.frame_body.position
            x = -(pos.x - self.win.width // 2)
            y = -(pos.y - self.win.height // 2)
            gl.glTranslatef(x, y, 0.0)

    def end(self):
        gl.glPopMatrix()
