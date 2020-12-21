import math

import pyglet
import pyglet.gl as gl

from pygd.bike import Bike
from pygd.window.base import BaseWindow
from pygd.window.poly_line import PolyLine


class MainWindow(BaseWindow):
    COLOR_BG = (1.0, 1.0, 1.0, 1.0)

    COLOR_TRACK = (0, 255, 0)
    LINE_WIDTH_TRACK = 1.0

    COLOR_BIKE_FRAME = (50, 50, 50)
    LINE_WIDTH_BIKE_FRAME = 1.0

    POLE_HEIGHT = 100
    COLOR_START = (255, 0, 0)
    COLOR_FINISH = (0, 0, 255)

    MESSAGE_TIMEOUT = 2.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gl.glClearColor(*self.COLOR_BG)

        # Enable alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.config.alpha_size = 8

        self.track_lines = None
        self.start = pyglet.shapes.Line(0, 0, 0, 0, color=self.COLOR_START)
        self.finish = pyglet.shapes.Line(0, 0, 0, 0, color=self.COLOR_FINISH)

        self.load_images()

        # Wheel sprites
        self.batch_bike_sprites = pyglet.graphics.Batch()
        self.sprites_wheel = []
        for _ in range(2):
            sprite = pyglet.sprite.Sprite(self.img_wheel, batch=self.batch_bike_sprites)
            sprite.scale = Bike.WHEEL_RADIUS / (self.img_wheel.width / 2)
            self.sprites_wheel.append(sprite)

        # Bike frame
        self.bike_frame_lines = PolyLine(
            [(0.0, 0.0) for _ in Bike.FRAME_POINTS],
            close=True,
            line_width=self.LINE_WIDTH_BIKE_FRAME,
            color=self.COLOR_BIKE_FRAME,
        )

        # Driver head
        self.driver_head = pyglet.shapes.Circle(
            0, 0, Bike.DRIVER_RADIUS, 16, color=(85, 35, 35)
        )

        # Message label
        self.batch_hud = pyglet.graphics.Batch()
        self.message_label = pyglet.text.Label(
            "",
            color=(0, 0, 0, 255),
            font_name="Arial",
            font_size=36,
            x=self.width // 2,
            y=self.height // 4,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch_hud,
        )

    def show_message(self, text, auto_clear=True):
        self.message_label.text = text
        self.message_label.visible = True
        if auto_clear:
            pyglet.clock.schedule_once(self.clear_message, self.MESSAGE_TIMEOUT)

    def clear_message(self, _):
        self.message_label.text = ""
        self.message_label.visible = False

    def load_images(self):
        self.img_wheel = pyglet.resource.image("wheel.png")
        self.img_wheel.anchor_x = self.img_wheel.width // 2
        self.img_wheel.anchor_y = self.img_wheel.height // 2

    def update_track(self, track):
        self.track_lines = PolyLine(
            track.points, line_width=self.LINE_WIDTH_TRACK, color=self.COLOR_TRACK
        )
        start_line = track.get_start_line()
        self.start.x, self.start.y = start_line
        self.start.x2, self.start.y2 = start_line - (0, self.POLE_HEIGHT)
        finish_line = track.get_finish_line()
        self.finish.x, self.finish.y = finish_line
        self.finish.x2, self.finish.y2 = finish_line - (0, self.POLE_HEIGHT)

    def draw_objects(self):
        if self.game.bike:
            self.update_objects()
            self.track_lines.draw()
            self.start.draw()
            self.finish.draw()
            self.bike_frame_lines.draw()
            self.driver_head.draw()
            self.batch_bike_sprites.draw()

    def draw_hud(self):
        if self.game.current_menu:
            self.game.current_menu.draw()
        self.batch_hud.draw()

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
        points = [  # Transform to world coords
            (v.rotated(frame_body.angle) + frame_body.position)
            for v in frame_shape.get_vertices()
        ]
        self.bike_frame_lines.update(points)

        # Driver
        x, y = self.game.bike.driver_body.position
        self.driver_head.x = x
        self.driver_head.y = y

    def on_key_press(self, symbol, modifiers):
        # Prevent default action: close window on escape
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        return None
