from pyglet.window import FPSDisplay, key, Window
import pyglet.gl as gl
import pymunk.pyglet_util


class DebugRendererWindow(Window):
    def __init__(self, size, space):
        super().__init__(size[0], size[1], caption="Gravity Defied")
        self.space = space
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.fps_display = FPSDisplay(window=self)
        self.fps_display.label.color = (255, 255, 255, 255)
        self.fps_display.label.font_size = 10

    def on_draw(self):
        self.clear()

        # Invert y axis
        gl.glPushMatrix()
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glTranslatef(0.0, -self.height, 0.0)
        self.space.debug_draw(self.draw_options)
        gl.glPopMatrix()

        self.fps_display.draw()
