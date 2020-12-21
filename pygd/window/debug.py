from pyglet.window import FPSDisplay
import pymunk.pyglet_util

from pygd.window.base import BaseWindow


class DebugWindow(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.fps_display = FPSDisplay(window=self)
        self.fps_display.label.color = (255, 255, 255, 255)
        self.fps_display.label.font_size = 10

    def on_draw(self):
        self.clear()
        self.game.space.debug_draw(self.draw_options)
        self.fps_display.draw()

    def show_message(self, text, timeout):
        print(f"DEBUG: show_message '{text}'")

    def update_track(self, track):
        pass
