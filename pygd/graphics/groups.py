from pyglet.graphics import Group
import pyglet.gl as gl


class PymunkCoordsGroup(Group):
    def __init__(self, win, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win = win

    def set_state(self):
        gl.glPushMatrix()
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glTranslatef(0.0, -self.win.height, 0.0)

    def unset_state(self):
        gl.glPopMatrix()


class WorldCameraGroup(Group):
    def __init__(self, win, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win = win

    def set_state(self):
        gl.glPushMatrix()
        bike = self.win.game.bike
        if bike:
            pos = bike.frame_body.position
            x = -(pos.x - self.win.width // 2)
            y = -(pos.y - self.win.height // 2)
            gl.glTranslatef(x, y, 0.0)

    def unset_state(self):
        gl.glPopMatrix()
