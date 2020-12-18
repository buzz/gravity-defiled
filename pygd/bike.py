import pymunk


class Bike:
    accel_ang_vel = 0.7
    max_ang_vel = 20.0
    brake_factor = 0.8

    wheel_radius = 24.5
    wheel_radius_inner = 20.0
    wheel_color = 90, 200, 20, 255
    wheel_friction = 1.4
    wheel_elasticity = 0.5

    wheel_l_pos = (-34.0, 6.0)
    wheel_l_mass = 25

    wheel_r_pos = (41.0, 6.0)
    wheel_r_mass = 8

    frame_point_top_l = (-11.7, -13.1)
    frame_point_top_r = (23.1, -31.55)
    frame_point_bottom = (-4.5, 9.55)

    joint_break_threshold = 200000

    def __init__(self, pos, space):
        self.space = space
        self.create_wheels(pos)
        self.create_frame(pos)
        self.create_joints()

    def create_wheels(self, pos):
        moment = pymunk.moment_for_circle(
            self.wheel_l_mass, self.wheel_radius_inner, self.wheel_radius
        )
        self.wheel_l_body = pymunk.Body(self.wheel_l_mass, moment)
        wheel_l_shape = pymunk.Circle(self.wheel_l_body, self.wheel_radius)
        wheel_l_shape.friction = self.wheel_friction
        wheel_l_shape.elasticity = self.wheel_elasticity
        wheel_l_shape.color = self.wheel_color
        self.wheel_l_body.position = pos + self.wheel_l_pos
        self.space.add(self.wheel_l_body, wheel_l_shape)

        moment = pymunk.moment_for_circle(
            self.wheel_r_mass, self.wheel_radius_inner, self.wheel_radius
        )
        self.wheel_r_body = pymunk.Body(self.wheel_r_mass, moment)
        wheel_r_shape = pymunk.Circle(self.wheel_r_body, self.wheel_radius)
        wheel_r_shape.friction = self.wheel_friction
        wheel_l_shape.elasticity = self.wheel_elasticity
        wheel_r_shape.color = self.wheel_color
        self.wheel_r_body.position = pos + self.wheel_r_pos
        self.space.add(self.wheel_r_body, wheel_r_shape)

    def create_frame(self, pos):
        frame_points = (
            self.frame_point_top_l,
            self.frame_point_top_r,
            self.frame_point_bottom,
        )
        frame_mass = 3
        moment = pymunk.moment_for_poly(frame_mass, frame_points)
        self.frame_body = pymunk.Body(frame_mass, moment)
        frame_shape = pymunk.Poly(self.frame_body, frame_points)
        frame_shape.friction = 1
        frame_shape.color = 128, 128, 128, 255
        self.frame_body.position = pos + (0.0, 0.0)
        self.space.add(self.frame_body, frame_shape)

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

    def update(self, game, dt):
        self.handle_left_wheel(game)
        self.check_joint_break(dt)

    def handle_left_wheel(self, game):
        if game.accelerating:
            self.wheel_l_body.angular_velocity += self.accel_ang_vel
        if game.braking and abs(self.wheel_l_body.angular_velocity) > 0.15:
            self.wheel_l_body.angular_velocity *= self.brake_factor

        if self.wheel_l_body.angular_velocity > self.max_ang_vel:
            self.wheel_l_body.angular_velocity = self.max_ang_vel
        elif self.wheel_l_body.angular_velocity < -self.max_ang_vel:
            self.wheel_l_body.angular_velocity = -self.max_ang_vel

    def check_joint_break(self, dt):
        for joint in self.joints:
            if joint.impulse / dt > self.joint_break_threshold:
                self.space.remove(joint)
                self.joints.remove(joint)
