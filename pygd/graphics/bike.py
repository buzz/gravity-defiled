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
        wheel_l_sprite = pyglet.sprite.Sprite(
            self.img_wheel_l, batch=batch, group=group, usage="stream"
        )
        wheel_l_sprite.scale = PhysicsBike.WHEEL_L_RADIUS / (self.img_wheel_l.width / 2)
        self.sprites_wheel.append(wheel_l_sprite)
        wheel_r_sprite = pyglet.sprite.Sprite(
            self.img_wheel_r, batch=batch, group=group, usage="stream"
        )
        wheel_r_sprite.scale = PhysicsBike.WHEEL_R_RADIUS / (self.img_wheel_r.width / 2)
        self.sprites_wheel.append(wheel_r_sprite)

        # Frame sprite
        self.sprite_frame = pyglet.sprite.Sprite(
            self.img_frame, batch=batch, group=group, usage="stream"
        )
        self.sprite_frame.scale = 0.5
        self.sprite_frame.scale_x = -1.0

        # Bike frame (pymunk)
        # self.bike_frame_lines_pymunk = PolyLine(
        #     [(0.0, 0.0) for _ in PhysicsBike.FRAME_POINTS],
        #     close=True,
        #     color=self.COLOR_BIKE_FRAME,
        #     width=self.LINE_WIDTH_BIKE_FRAME,
        #     batch=batch,
        #     group=group,
        #     vertex_usage="stream",
        # )

        # Driver head
        self.driver_head = pyglet.shapes.Circle(
            *(0.0, 0.0),
            PhysicsBike.DRIVER_RADIUS,
            16,
            color=self.COLOR_DRIVER_HEAD,
            batch=batch,
            group=group,
        )

        # Driver body
        self.driver_body = PolyLine(
            [(0.0, 0.0) for _ in range(3)],
            batch=batch,
            group=group,
            vertex_usage="stream",
        )

        # Driver leg sprite
        # self.sprite_driver_leg = pyglet.sprite.Sprite(
        #     self.img_driver_leg, batch=batch, group=group, usage="stream"
        # )
        # self.sprite_driver_leg.scale = 0.135
        # self.sprite_driver_leg.scale_y = -1.0

    def load_images(self):
        self.img_frame = pyglet.resource.image("frame.png")
        self.img_frame.anchor_x = 58.0
        self.img_frame.anchor_y = 8.0

        self.img_wheel_l = pyglet.resource.image("wheel_l.png")
        self.img_wheel_l.anchor_x = self.img_wheel_l.width // 2
        self.img_wheel_l.anchor_y = self.img_wheel_l.height // 2

        self.img_wheel_r = pyglet.resource.image("wheel_r.png")
        self.img_wheel_r.anchor_x = self.img_wheel_r.width // 2
        self.img_wheel_r.anchor_y = self.img_wheel_r.height // 2

        self.img_driver_leg = pyglet.resource.image("driver_leg.png")
        self.img_driver_leg.anchor_x = 0.0
        self.img_driver_leg.anchor_y = 0.0

    def update(self, game):
        # Wheels
        for i in range(2):
            wheel_body = game.bike.wheels_body[i]
            x, y = wheel_body.position
            rotation = -math.degrees(wheel_body.angle)
            self.sprites_wheel[i].update(x=x, y=y, rotation=rotation)

        # Bike frame points
        frame_shape = game.bike.frame_shape
        frame_body = game.bike.frame_body
        bike_frame_points_pymunk = [
            # Local to world coords
            (v.rotated(frame_body.angle) + frame_body.position)
            for v in frame_shape.get_vertices()
        ]

        # Bike frame (sprite)
        bike_frame_rot = frame_body.angle
        self.sprite_frame.update(
            x=bike_frame_points_pymunk[0].x,
            y=bike_frame_points_pymunk[0].y,
            rotation=-math.degrees(bike_frame_rot + math.pi),
        )

        # Bike frame (pymunk)
        # bike_frame_points_pymunk = [
        #     # Local to world coords
        #     (v.rotated(frame_body.angle) + frame_body.position)
        #     for v in frame_shape.get_vertices()
        # ]
        # self.bike_frame_lines_pymunk.update(bike_frame_points_pymunk)

        # Driver head
        head_pos = game.bike.driver_head_body.position
        self.driver_head.x, self.driver_head.y = head_pos

        # Driver body
        self.update_body(
            head_pos, bike_frame_points_pymunk[0], bike_frame_points_pymunk[1]
        )

    def update_body(self, head_pos, footpeg_pos, handle_pos):
        # Driver body lines
        self.driver_body.update((footpeg_pos, head_pos, handle_pos))

        # Driver leg sprite
        # rot = 0
        # self.sprite_driver_leg.update(x=footpeg_pos.x, y=footpeg_pos.y, rotation=rot)
