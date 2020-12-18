import math

import pyglet
import pyglet.gl as gl

from pygd.bike import Bike
from pygd.renderer.base import BaseWindow
from pygd.renderer.poly_line import PolyLine


class RendererWindow(BaseWindow):
    COLOR_BG = (1.0, 1.0, 1.0, 1.0)

    COLOR_TRACK = (0, 255, 0)
    LINE_WIDTH_TRACK = 1.0

    COLOR_BIKE_FRAME = (50, 50, 50)
    LINE_WIDTH_BIKE_FRAME = 1.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gl.glClearColor(*self.COLOR_BG)

        # Enable alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.config.alpha_size = 8

        self.batch_track_line = None
        self.track_lines = None

        self.load_images()

        # Create wheel sprites
        self.batch_bike_sprites = pyglet.graphics.Batch()
        self.sprites_wheel = []
        for _ in range(2):
            sprite = pyglet.sprite.Sprite(self.img_wheel, batch=self.batch_bike_sprites)
            sprite.scale = Bike.WHEEL_RADIUS / (self.img_wheel.width / 2)
            self.sprites_wheel.append(sprite)

        # Create bike frame
        self.bike_frame_lines = PolyLine(
            [(0.0, 0.0) for _ in Bike.FRAME_POINTS],
            close=True,
            line_width=self.LINE_WIDTH_BIKE_FRAME,
            color=self.COLOR_BIKE_FRAME,
        )

    def load_images(self):
        self.img_wheel = pyglet.resource.image("wheel.png")
        self.img_wheel.anchor_x = self.img_wheel.width // 2
        self.img_wheel.anchor_y = self.img_wheel.height // 2

    def update_track(self, points):
        self.batch_track_line = pyglet.graphics.Batch()
        self.track_lines = PolyLine(
            points, line_width=self.LINE_WIDTH_TRACK, color=self.COLOR_TRACK
        )

    def draw_objects(self):
        self.update_objects()
        self.track_lines.draw()
        self.bike_frame_lines.draw()
        self.batch_bike_sprites.draw()

    def draw_hud(self):
        pass

    def update_objects(self):
        # Wheels
        for i, attr in enumerate(("wheel_l_body", "wheel_r_body")):
            wheel_body = getattr(self.game.bike, attr)
            x, y = wheel_body.position
            rotation = -math.degrees(wheel_body.angle)
            self.sprites_wheel[i].update(x=x, y=y, rotation=rotation)

        # Bike frame
        frame_shape = self.game.bike.frame_shape
        frame_body = self.game.bike.frame_body
        points = [  # Transform to world coords
            (v.rotated(frame_body.angle) + frame_body.position)
            for v in frame_shape.get_vertices()
        ]
        self.bike_frame_lines.update(points)
