import pymunk
from pymunk.vec2d import Vec2d


class Bike:
    accel_ang_vel = 0.7
    max_ang_vel = 20.0
    brake_factor = 0.8

    wheel_radius = 24.5
    wheel_radius_inner = 20.0
    wheel_color = 90, 200, 20, 255
    wheel_friction = 1.4
    wheel_elasticity = 0.5

    wheel_l_pos = Vec2d(-34.0, 6.0)
    wheel_l_mass = 25

    wheel_r_pos = Vec2d(41.0, 6.0)
    wheel_r_mass = 8

    frame_point_top_l = Vec2d(-11.7, -13.1)
    frame_point_top_r = Vec2d(23.1, -31.55)
    frame_point_bottom = Vec2d(-4.5, 9.55)

    joint_break_threshold = 200000

    def __init__(self, start_pos, space):
        self.space = space
        self.start_pos = start_pos
        self.create_wheels()
        self.create_frame()
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
            self.wheel_l_mass, self.wheel_radius_inner, self.wheel_radius
        )
        self.wheel_l_body = pymunk.Body(self.wheel_l_mass, moment)
        self.wheel_l_shape = pymunk.Circle(self.wheel_l_body, self.wheel_radius)
        self.wheel_l_shape.friction = self.wheel_friction
        self.wheel_l_shape.elasticity = self.wheel_elasticity
        self.wheel_l_shape.color = self.wheel_color
        self.wheel_l_body.position = self.start_pos + self.wheel_l_pos
        self.space.add(self.wheel_l_body, self.wheel_l_shape)

        moment = pymunk.moment_for_circle(
            self.wheel_r_mass, self.wheel_radius_inner, self.wheel_radius
        )
        self.wheel_r_body = pymunk.Body(self.wheel_r_mass, moment)
        self.wheel_r_shape = pymunk.Circle(self.wheel_r_body, self.wheel_radius)
        self.wheel_r_shape.friction = self.wheel_friction
        self.wheel_l_shape.elasticity = self.wheel_elasticity
        self.wheel_r_shape.color = self.wheel_color
        self.wheel_r_body.position = self.start_pos + self.wheel_r_pos
        self.space.add(self.wheel_r_body, self.wheel_r_shape)

    def create_frame(self):
        frame_points = (
            self.frame_point_top_l,
            self.frame_point_top_r,
            self.frame_point_bottom,
        )
        frame_mass = 3
        moment = pymunk.moment_for_poly(frame_mass, frame_points)
        self.frame_body = pymunk.Body(frame_mass, moment)
        self.frame_shape = pymunk.Poly(self.frame_body, frame_points)
        self.frame_shape.friction = 1
        self.frame_shape.color = 128, 128, 128, 255
        self.frame_body.position = self.start_pos
        self.space.add(self.frame_body, self.frame_shape)

    def create_joints(self):
        self.joints = [
            pymunk.PinJoint(
                self.wheel_l_body, self.frame_body, (0, 0), self.frame_point_top_l
            ),
            pymunk.PinJoint(
                self.wheel_l_body, self.frame_body, (0, 0), self.frame_point_bottom
            ),
            pymunk.PinJoint(
                self.wheel_r_body, self.frame_body, (0, 0), self.frame_point_bottom
            ),
            pymunk.DampedSpring(
                self.wheel_r_body, self.frame_body, (0, 0), (26.5, -25.0), 42, 170, 50
            ),
        ]
        self.space.add(*self.joints)

    def update(self, game, delta_t):
        self.handle_left_wheel(game)
        self.check_joint_break(delta_t)

    def handle_left_wheel(self, game):
        if game.accelerating:
            self.wheel_l_body.angular_velocity += self.accel_ang_vel
        if game.braking and abs(self.wheel_l_body.angular_velocity) > 0.15:
            self.wheel_l_body.angular_velocity *= self.brake_factor

        if self.wheel_l_body.angular_velocity > self.max_ang_vel:
            self.wheel_l_body.angular_velocity = self.max_ang_vel
        elif self.wheel_l_body.angular_velocity < -self.max_ang_vel:
            self.wheel_l_body.angular_velocity = -self.max_ang_vel

    def check_joint_break(self, delta_t):
        for joint in self.joints:
            if joint.impulse / delta_t > self.joint_break_threshold:
                self.space.remove(joint)
                self.joints.remove(joint)
