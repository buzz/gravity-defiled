import pyglet
import pyglet.gl as gl

from pygd.graphics.bike import Bike
from pygd.graphics.track import Track
from pygd.graphics.window.base import BaseWindow
from pygd.menu import FONT_COLOR, FONT_NAME, FONT_SIZE_BIG

GL_CONFIG = {
    "alpha_size": 8,
    "depth_size": 0,
    "double_buffer": True,
    "sample_buffers": 1,
    "samples": 3,
}


class MainWindow(BaseWindow):
    COLOR_BG = (1.0, 1.0, 1.0, 1.0)

    def __init__(self, *args, **kwargs):
        super().__init__(config=pyglet.gl.Config(**GL_CONFIG), *args, **kwargs)
        self.gl_setup()

        self.batch_menu = pyglet.graphics.Batch()
        self.batch_game = pyglet.graphics.Batch()

        self.track = Track(self.batch_game, self.group_world_camera)
        self.bike = Bike(self.batch_game, self.group_world_camera)
        self.message_label = self.create_message_label()

    def gl_setup(self):
        gl.glClearColor(*self.COLOR_BG)
        # Enable alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def create_message_label(self):
        return pyglet.text.Label(
            "",
            color=FONT_COLOR,
            font_name=FONT_NAME,
            font_size=FONT_SIZE_BIG,
            x=self.width // 2,
            y=self.height // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch_game,
        )

    def show_message(self, text, timeout):
        self.message_label.text = text
        self.message_label.visible = True
        pyglet.clock.schedule_once(self.clear_message, timeout)

    def clear_message(self, _):
        self.message_label.visible = False

    def update_track(self, track):
        self.track.update(track)

    def update_objects(self):
        self.bike.update(self.game)

    # Events

    def on_draw(self):
        self.clear()
        if self.game.bike:
            self.update_objects()
            self.batch_game.draw()

        self.batch_menu.draw()

    def on_key_press(self, symbol, _):
        # Prevents window from closing on escape
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        return None
