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

    def __init__(self, pos, space):
        moment = pymunk.moment_for_circle(
            self.wheel_l_mass, self.wheel_radius_inner, self.wheel_radius
        )
        self.wheel_l_body = pymunk.Body(self.wheel_l_mass, moment)
        wheel_l_shape = pymunk.Circle(self.wheel_l_body, self.wheel_radius)
        wheel_l_shape.friction = self.wheel_friction
        wheel_l_shape.elasticity = self.wheel_elasticity
        wheel_l_shape.color = self.wheel_color
        self.wheel_l_body.position = pos + self.wheel_l_pos
        space.add(self.wheel_l_body, wheel_l_shape)

        moment = pymunk.moment_for_circle(
            self.wheel_r_mass, self.wheel_radius_inner, self.wheel_radius
        )
        wheel_r_body = pymunk.Body(self.wheel_r_mass, moment)
        wheel_r_shape = pymunk.Circle(wheel_r_body, self.wheel_radius)
        wheel_r_shape.friction = self.wheel_friction
        wheel_l_shape.elasticity = self.wheel_elasticity
        wheel_r_shape.color = self.wheel_color
        wheel_r_body.position = pos + self.wheel_r_pos
        space.add(wheel_r_body, wheel_r_shape)

        frame_point_top_l = (-11.7, -13.1)
        frame_point_top_r = (23.1, -31.55)
        frame_point_bottom = (-4.5, 9.55)
        frame_points = (frame_point_top_l, frame_point_top_r, frame_point_bottom)
        frame_mass = 3
        moment = pymunk.moment_for_poly(frame_mass, frame_points)
        frame_body = pymunk.Body(frame_mass, moment)
        frame_shape = pymunk.Poly(frame_body, frame_points)
        frame_shape.friction = 1
        frame_shape.color = 128, 128, 128, 255
        frame_body.position = pos + (0.0, 0.0)
        space.add(frame_body, frame_shape)

        joint_back_top = pymunk.PinJoint(
            self.wheel_l_body, frame_body, (0, 0), frame_point_top_l
        )
        joint_back_bottom = pymunk.PinJoint(
            self.wheel_l_body, frame_body, (0, 0), frame_point_bottom
        )
        joint_front_top = pymunk.DampedSpring(
            wheel_r_body, frame_body, (0, 0), (26.5, -25.0), 42, 170, 50
        )
        joint_front_bottom = pymunk.PinJoint(
            wheel_r_body, frame_body, (0, 0), frame_point_bottom
        )

        space.add(joint_back_top)
        space.add(joint_back_bottom)
        space.add(joint_front_top)
        space.add(joint_front_bottom)

    def update(self, game):
        self.handle_left_wheel(game)
        # self.check_joint_forces()

    def handle_left_wheel(self, game):
        if game.accelerating:
            self.wheel_l_body.angular_velocity += self.accel_ang_vel
        if game.braking and abs(self.wheel_l_body.angular_velocity) > 0.15:
            self.wheel_l_body.angular_velocity *= self.brake_factor

        if self.wheel_l_body.angular_velocity > self.max_ang_vel:
            self.wheel_l_body.angular_velocity = self.max_ang_vel
        elif self.wheel_l_body.angular_velocity < -self.max_ang_vel:
            self.wheel_l_body.angular_velocity = -self.max_ang_vel

    # def check_joint_forces(self):
    #     print()