import pymunk
from pymunk.vec2d import Vec2d


class Bike:
    JOINT_BREAK_THRESHOLD = 700000
    ACCEL_ANG_VEL = 1.5
    MAX_ANG_VEL = 24.0
    BRAKE_FACTOR = 0.7

    WHEEL_RADIUS = 20.5
    WHEEL_RADIUS_INNER = 14.1
    WHEEL_FRICTION = 3.4
    WHEEL_ELASTICITY = 0.5

    WHEEL_L_POS = Vec2d(-34.0, 6.0)
    WHEEL_L_MASS = 25

    WHEEL_R_POS = Vec2d(41.0, 6.0)
    WHEEL_R_MASS = 8

    FRAME_FRICTION = 0.1
    FRAME_POINTS = (
        Vec2d(31, -36),
        Vec2d(10, 3.55),
        Vec2d(-18, 0.55),
    )

    def __init__(self, start_pos, space):
        self.space = space
        self.start_pos = start_pos
        self.crashed = False

        self.filter_group = pymunk.ShapeFilter(group=1)
        self.frame_body = None
        self.frame_shape = None
        self.wheels_body = []
        self.wheels_shape = []
        self.joints = []

        self.create_wheels()
        self.create_frame()
        self.create_joints()

    def __del__(self):
        self.space.remove(
            *self.wheels_body,
            *self.wheels_shape,
            self.frame_body,
            self.frame_shape,
            *self.joints,
        )

    def create_wheels(self):
        for (pos, mass) in (
            (self.WHEEL_L_POS, self.WHEEL_L_MASS),
            (self.WHEEL_R_POS, self.WHEEL_R_MASS),
        ):
            moment = pymunk.moment_for_circle(
                mass, self.WHEEL_RADIUS_INNER, self.WHEEL_RADIUS
            )
            wheel_body = pymunk.Body(mass, moment)
            wheel_shape = pymunk.Circle(wheel_body, self.WHEEL_RADIUS)
            wheel_shape.friction = self.WHEEL_FRICTION
            wheel_shape.elasticity = self.WHEEL_ELASTICITY
            wheel_body.position = self.start_pos + pos
            wheel_shape.filter = self.filter_group
            self.wheels_body.append(wheel_body)
            self.wheels_shape.append(wheel_shape)
            self.space.add(wheel_body, wheel_shape)

    def create_frame(self):
        frame_mass = 3
        moment = pymunk.moment_for_poly(frame_mass, self.FRAME_POINTS)
        self.frame_body = pymunk.Body(frame_mass, moment)
        self.frame_shape = pymunk.Poly(self.frame_body, self.FRAME_POINTS)
        self.frame_shape.friction = self.FRAME_FRICTION
        self.frame_body.position = self.start_pos
        self.frame_shape.filter = self.filter_group
        self.space.add(self.frame_body, self.frame_shape)

    def create_joints(self):
        self.joints = [
            # Left wheel to bottom frame
            pymunk.SlideJoint(
                self.wheels_body[0], self.frame_body, (0, 0), (-10, -2), 25, 26
            ),
            # Left wheel to top frame
            pymunk.SlideJoint(
                self.wheels_body[0], self.frame_body, (0, 0), (0, -25.0), 38, 41
            ),
            pymunk.DampedSpring(
                self.wheels_body[0], self.frame_body, (0, 0), (0, -25.0), 42, 170, 50
            ),
            # Right wheel to bottom frame
            pymunk.SlideJoint(
                self.wheels_body[1], self.frame_body, (0, 0), (0, 0), 40, 42
            ),
            # Right wheel to top frame
            pymunk.SlideJoint(
                self.wheels_body[1], self.frame_body, (0, 0), (26.5, -25.0), 30, 56
            ),
            pymunk.DampedSpring(
                self.wheels_body[1], self.frame_body, (0, 0), (26.5, -25.0), 45, 120, 30
            ),
            # Left to right wheel, only min distance important here, so bike can't
            # fold into itself
            pymunk.SlideJoint(
                self.wheels_body[0], self.wheels_body[1], (0, 0), (0, 0), 60, 500
            ),
        ]
        self.space.add(*self.joints)

    def update(self, game, delta_t):
        if not self.crashed:
            self.apply_input(game)
            self.check_joint_break(delta_t)

    def apply_input(self, game):
        if game.accelerating:
            self.wheels_body[0].angular_velocity += self.ACCEL_ANG_VEL
        if game.braking and abs(self.wheels_body[0].angular_velocity) > 0.15:
            self.wheels_body[0].angular_velocity *= self.BRAKE_FACTOR

        if self.wheels_body[0].angular_velocity > self.MAX_ANG_VEL:
            self.wheels_body[0].angular_velocity = self.MAX_ANG_VEL
        elif self.wheels_body[0].angular_velocity < -self.MAX_ANG_VEL:
            self.wheels_body[0].angular_velocity = -self.MAX_ANG_VEL

    def check_joint_break(self, delta_t):
        for joint in self.joints:
            if joint.impulse / delta_t > self.JOINT_BREAK_THRESHOLD:
                self.crashed = True
                self.space.remove(*self.joints)
                self.joints = []
                break
