from pyglet.window import Window

from gravity_defiled.graphics.groups import PymunkCoordsGroup, WorldCameraGroup


class BaseWindow(Window):
    def __init__(self, space, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.space = space

        self.group_pymunk_coords = PymunkCoordsGroup(self)
        self.group_world_camera = WorldCameraGroup(
            self, parent=self.group_pymunk_coords
        )

        self.set_mouse_visible(False)

    def on_draw(self):
        raise NotImplementedError

    def show_message(self, text, timeout):
        raise NotImplementedError

    def update_track(self, track):
        raise NotImplementedError
