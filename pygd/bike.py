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
        self.create_wheels()
        self.create_frame()
        self.joints = []
        self.create_joints()

    def __del__(self):
        self.space.remove(
            self.wheel_l_body,
            self.wheel_l_shape,
            self.wheel_r_body,
            self.wheel_r_shape,
            self.frame_body,
            self.frame_shape,
            *self.joints,
        )

    def create_wheels(self):
        moment = pymunk.moment_for_circle(
            self.WHEEL_L_MASS, self.WHEEL_RADIUS_INNER, self.WHEEL_RADIUS
        )
        self.wheel_l_body = pymunk.Body(self.WHEEL_L_MASS, moment)
        self.wheel_l_shape = pymunk.Circle(self.wheel_l_body, self.WHEEL_RADIUS)
        self.wheel_l_shape.friction = self.WHEEL_FRICTION
        self.wheel_l_shape.elasticity = self.WHEEL_ELASTICITY
        self.wheel_l_body.position = self.start_pos + self.WHEEL_L_POS
        self.wheel_l_shape.filter = self.filter_group
        self.space.add(self.wheel_l_body, self.wheel_l_shape)

        moment = pymunk.moment_for_circle(
            self.WHEEL_R_MASS, self.WHEEL_RADIUS_INNER, self.WHEEL_RADIUS
        )
        self.wheel_r_body = pymunk.Body(self.WHEEL_R_MASS, moment)
        self.wheel_r_shape = pymunk.Circle(self.wheel_r_body, self.WHEEL_RADIUS)
        self.wheel_r_shape.friction = self.WHEEL_FRICTION
        self.wheel_l_shape.elasticity = self.WHEEL_ELASTICITY
        self.wheel_r_body.position = self.start_pos + self.WHEEL_R_POS
        self.wheel_r_shape.filter = self.filter_group
        self.space.add(self.wheel_r_body, self.wheel_r_shape)

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
                self.wheel_l_body, self.frame_body, (0, 0), (-10, -2), 25, 26
            ),
            # Left wheel to top frame
            pymunk.SlideJoint(
                self.wheel_l_body, self.frame_body, (0, 0), (0, -25.0), 38, 41
            ),
            pymunk.DampedSpring(
                self.wheel_l_body, self.frame_body, (0, 0), (0, -25.0), 42, 170, 50
            ),
            # Right wheel to bottom frame
            pymunk.SlideJoint(
                self.wheel_r_body, self.frame_body, (0, 0), (0, 0), 40, 42
            ),
            # Right wheel to top frame
            pymunk.SlideJoint(
                self.wheel_r_body, self.frame_body, (0, 0), (26.5, -25.0), 30, 56
            ),
            pymunk.DampedSpring(
                self.wheel_r_body, self.frame_body, (0, 0), (26.5, -25.0), 45, 120, 30
            ),
            # Left to right wheel, only min distance important here, so bike can't
            # fold into itself
            pymunk.SlideJoint(
                self.wheel_r_body, self.wheel_l_body, (0, 0), (0, 0), 60, 500
            ),
        ]
        self.space.add(*self.joints)

    def update(self, game, delta_t):
        if not self.crashed:
            self.handle_left_wheel(game)
            self.check_joint_break(delta_t)

    def handle_left_wheel(self, game):
        if game.accelerating:
            self.wheel_l_body.angular_velocity += self.ACCEL_ANG_VEL
        if game.braking and abs(self.wheel_l_body.angular_velocity) > 0.15:
            self.wheel_l_body.angular_velocity *= self.BRAKE_FACTOR

        if self.wheel_l_body.angular_velocity > self.MAX_ANG_VEL:
            self.wheel_l_body.angular_velocity = self.MAX_ANG_VEL
        elif self.wheel_l_body.angular_velocity < -self.MAX_ANG_VEL:
            self.wheel_l_body.angular_velocity = -self.MAX_ANG_VEL

    def check_joint_break(self, delta_t):
        for joint in self.joints:
            if joint.impulse / delta_t > self.JOINT_BREAK_THRESHOLD:
                self.crashed = True
                self.space.remove(*self.joints)
                self.joints = []
                break
