import math
import pyglet

from pygd.bike import Bike as PhysicsBike
from pygd.graphics.poly_line import PolyLine


class Bike:
    COLOR_BIKE_FRAME = (50, 50, 50)
    LINE_WIDTH_BIKE_FRAME = 1.0
    COLOR_DRIVER_HEAD = (85, 35, 35)

    def __init__(self, batch, group):
        self.load_images()

        # Wheel sprites
        self.sprites_wheel = []
        for _ in range(2):
            sprite = pyglet.sprite.Sprite(self.img_wheel, batch=batch, group=group)
            sprite.scale = PhysicsBike.WHEEL_RADIUS / (self.img_wheel.width / 2)
            self.sprites_wheel.append(sprite)

        # Bike frame
        self.bike_frame_lines = PolyLine(
            [(0.0, 0.0) for _ in PhysicsBike.FRAME_POINTS],
            close=True,
            color=self.COLOR_BIKE_FRAME,
            width=self.LINE_WIDTH_BIKE_FRAME,
            batch=batch,
            group=group,
            vertex_usage="stream",
        )

        # Driver head
        self.driver_head = pyglet.shapes.Circle(
            *(2 * (0,)),
            PhysicsBike.DRIVER_RADIUS,
            16,
            color=self.COLOR_DRIVER_HEAD,
            batch=batch,
            group=group,
        )

        # Driver body
        # driver_shape = ((0.0, 0.0), (0.0, 60.0))
        # self.driver_shape = PolyLine(
        #     driver_shape, batch=batch, group=group, vertex_usage="stream"
        # )

    def load_images(self):
        self.img_wheel = pyglet.resource.image("wheel.png")
        self.img_wheel.anchor_x = self.img_wheel.width // 2
        self.img_wheel.anchor_y = self.img_wheel.height // 2

    def update(self, game):
        # Wheels
        for i in range(2):
            wheel_body = game.bike.wheels_body[i]
            x, y = wheel_body.position
            rotation = -math.degrees(wheel_body.angle)
            self.sprites_wheel[i].update(x=x, y=y, rotation=rotation)

        # Bike frame
        frame_shape = game.bike.frame_shape
        frame_body = game.bike.frame_body
        bike_frame_points = [
            # Local to world coords
            (v.rotated(frame_body.angle) + frame_body.position)
            for v in frame_shape.get_vertices()
        ]
        self.bike_frame_lines.update(bike_frame_points)

        # Driver
        x, y = game.bike.driver_head_body.position
        self.driver_head.x = x
        self.driver_head.y = y
