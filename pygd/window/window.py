import math

import pyglet
import pyglet.gl as gl

from pygd.bike import Bike
from pygd.window.base import BaseWindow
from pygd.window.poly_line import PolyLine
from pygd.menu import FONT_COLOR, FONT_NAME, FONT_SIZE_BIG

GL_CONFIG = {
    "alpha_size": 8,
    "depth_size": 0,
    "double_buffer": True,
    "sample_buffers": 1,
    "samples": 8,
}


class MainWindow(BaseWindow):
    COLOR_BG = (1.0, 1.0, 1.0, 1.0)

    COLOR_TRACK = (0, 255, 0)
    LINE_WIDTH_TRACK = 1.0

    COLOR_BIKE_FRAME = (50, 50, 50)
    LINE_WIDTH_BIKE_FRAME = 1.0
    COLOR_DRIVER_HEAD = (85, 35, 35)

    POLE_HEIGHT = 100
    COLOR_START = (255, 0, 0)
    COLOR_FINISH = (0, 0, 255)

    def __init__(self, *args, **kwargs):
        super().__init__(config=pyglet.gl.Config(**GL_CONFIG), *args, **kwargs)
        self.gl_setup()
        self.load_images()

        self.batch_menu = pyglet.graphics.Batch()
        self.batch_game = pyglet.graphics.Batch()

        self.create_track()
        self.create_bike()
        self.create_message()

    def create_track(self):
        self.track_lines = PolyLine(
            [],
            width=self.LINE_WIDTH_TRACK,
            color=self.COLOR_TRACK,
            batch=self.batch_game,
            group=self.group_world_camera,
        )
        self.start = pyglet.shapes.Line(
            *(4 * (0,)),
            color=self.COLOR_START,
            batch=self.batch_game,
            group=self.group_world_camera,
        )
        self.finish = pyglet.shapes.Line(
            *(4 * (0,)),
            color=self.COLOR_FINISH,
            batch=self.batch_game,
            group=self.group_world_camera,
        )

    def create_bike(self):
        # Wheel sprites
        self.sprites_wheel = []
        for _ in range(2):
            sprite = pyglet.sprite.Sprite(
                self.img_wheel,
                batch=self.batch_game,
                group=self.group_world_camera,
            )
            sprite.scale = Bike.WHEEL_RADIUS / (self.img_wheel.width / 2)
            self.sprites_wheel.append(sprite)

        # Bike frame
        self.bike_frame_lines = PolyLine(
            [(0.0, 0.0) for _ in Bike.FRAME_POINTS],
            close=True,
            color=self.COLOR_BIKE_FRAME,
            width=self.LINE_WIDTH_BIKE_FRAME,
            batch=self.batch_game,
            group=self.group_world_camera,
            vertex_usage="stream",
        )

        # Driver head
        self.driver_head = pyglet.shapes.Circle(
            *(2 * (0,)),
            Bike.DRIVER_RADIUS,
            16,
            color=self.COLOR_DRIVER_HEAD,
            batch=self.batch_game,
            group=self.group_world_camera,
        )

    def create_message(self):
        self.message_label = pyglet.text.Label(
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

    def gl_setup(self):
        gl.glClearColor(*self.COLOR_BG)
        # Enable alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def load_images(self):
        self.img_wheel = pyglet.resource.image("wheel.png")
        self.img_wheel.anchor_x = self.img_wheel.width // 2
        self.img_wheel.anchor_y = self.img_wheel.height // 2

    def show_message(self, text, timeout):
        self.message_label.text = text
        self.message_label.visible = True
        pyglet.clock.schedule_once(self.clear_message, timeout)

    def clear_message(self, _):
        self.message_label.visible = False

    def update_track(self, track):
        self.track_lines.update(track.points)
        self.start.x, self.start.y = track.start_line
        self.start.x2, self.start.y2 = track.start_line - (0, self.POLE_HEIGHT)
        self.finish.x, self.finish.y = track.finish_line
        self.finish.x2, self.finish.y2 = track.finish_line - (0, self.POLE_HEIGHT)

    def update_objects(self):
        # Wheels
        for i in range(2):
            wheel_body = self.game.bike.wheels_body[i]
            x, y = wheel_body.position
            rotation = -math.degrees(wheel_body.angle)
            self.sprites_wheel[i].update(x=x, y=y, rotation=rotation)

        # Bike frame
        frame_shape = self.game.bike.frame_shape
        frame_body = self.game.bike.frame_body
        bike_frame_points = [
            # Local to world coords
            (v.rotated(frame_body.angle) + frame_body.position)
            for v in frame_shape.get_vertices()
        ]
        self.bike_frame_lines.update(bike_frame_points)

        # Driver
        x, y = self.game.bike.driver_body.position
        self.driver_head.x = x
        self.driver_head.y = y

    # Events

    def on_draw(self):
        self.clear()
        if self.game.bike:
            self.update_objects()
            self.batch_game.draw()

        self.batch_menu.draw()

    def on_key_press(self, symbol, modifiers):
        # Prevent default action: close window on escape
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        return None
