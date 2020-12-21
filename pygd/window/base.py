from pyglet.window import Window

from pygd.window.transformations import ToPymunkCoords, WorldCamera


class BaseWindow(Window):
    def __init__(self, space, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.space = space

        self.to_pymunk_coords = ToPymunkCoords(self)
        self.world_camera = WorldCamera(self)

        self.set_mouse_visible(False)

    def on_draw(self):
        self.clear()

        with self.to_pymunk_coords:
            with self.world_camera:
                self.draw_objects()

        self.draw_hud()

    def draw_objects(self):
        raise NotImplementedError

    def draw_hud(self):
        raise NotImplementedError

    def show_message(self, text, auto_clear=True):
        raise NotImplementedError

    def update_track(self, points):
        raise NotImplementedError
