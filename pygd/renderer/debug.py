from pyglet.window import FPSDisplay
import pymunk.pyglet_util

from pygd.renderer.base import BaseWindow


class DebugRendererWindow(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.fps_display = FPSDisplay(window=self)
        self.fps_display.label.color = (255, 255, 255, 255)
        self.fps_display.label.font_size = 10

    def draw_objects(self):
        self.space.debug_draw(self.draw_options)

    def draw_hud(self):
        self.fps_display.draw()

    def show_message(self, text):
        print(f"DEBUG: show_message '{text}'")

    def update_track(self, points):
        pass
