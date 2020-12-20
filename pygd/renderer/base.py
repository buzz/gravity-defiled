from pyglet.window import Window
import pyglet.gl as gl


class BaseWindow(Window):
    def __init__(self, camera, space, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.game = game
        self.space = space

    def on_draw(self):
        self.clear()

        self.camera.project()

        # Use transformations, so we can draw in pymunk coordinate space

        # Invert y axis
        gl.glPushMatrix()
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glTranslatef(0.0, -self.height, 0.0)

        # Translate objects to viewport center (camera follow)
        gl.glPushMatrix()
        gl.glTranslatef(self.camera.x, self.camera.y, 0.0)

        self.draw_objects()

        gl.glPopMatrix()
        gl.glPopMatrix()

        self.draw_hud()

    def draw_objects(self):
        raise NotImplementedError

    def draw_hud(self):
        raise NotImplementedError

    def show_message(self, text):
        raise NotImplementedError

    def update_track(self, points):
        raise NotImplementedError
