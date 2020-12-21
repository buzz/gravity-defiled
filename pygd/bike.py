import math

import pymunk
from pymunk.vec2d import Vec2d


class Bike:
    JOINT_BREAK_THRESHOLD = 700000
    ACCEL_ANG_VEL = 2.0
    MAX_ANG_VEL = 20.0
    BRAKE_FACTOR = 0.4
    LEAN_SPEED_FORWARD = 0.4
    LEAN_SPEED_BACKWARD = 0.05

    WHEEL_RADIUS = 20.5
    WHEEL_RADIUS_INNER = 14.1
    WHEEL_FRICTION = 3.4
    WHEEL_ELASTICITY = 0.5

    WHEEL_L_POS = Vec2d(-34.0, 6.0)
    WHEEL_L_MASS = 20

    WHEEL_R_POS = Vec2d(41.0, 6.0)
    WHEEL_R_MASS = 8
    WHEEL_R_COLLISION_TYPE = 1

    FRAME_FRICTION = 0.1
    FRAME_MASS = 10
    FRAME_POINTS = (
        Vec2d(31, -36),
        Vec2d(10, 3.55),
        Vec2d(-18, 0.55),
    )

    DRIVER_RADIUS = 11
    DRIVER_FRICTION = 2
    DRIVER_MASS = 15
    DRIVER_POS = Vec2d(0, -75)
    DRIVER_JOINT_DIST_L = 100.0
    DRIVER_JOINT_DIST_R = 90.0
    DRIVER_COLLISION_TYPE = 2

    CONTROLS_DEAD_ZONE = 0.05

    def __init__(self, game, space):
        self.game = game
        self.space = space
        self.bike_broken = False
        self.driver_crash = False
        self.wheel_r_coll = 0  # collision counter

        self.filter_group = pymunk.ShapeFilter(group=1)
        self.frame_body = None
        self.frame_shape = None
        self.driver_body = None
        self.driver_shape = None
        self.wheels_body = []
        self.wheels_shape = []
        self.frame_joints = []
        self.driver_joints = []

        self.create_wheels()
        self.create_frame()
        self.create_driver()
        self.create_frame_joints()
        self.create_driver_joints()

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

        self.wheels_shape[1].collision_type = self.WHEEL_R_COLLISION_TYPE

    def create_frame(self):
        moment = pymunk.moment_for_poly(self.FRAME_MASS, self.FRAME_POINTS)
        self.frame_body = pymunk.Body(self.FRAME_MASS, moment)
        self.frame_shape = pymunk.Poly(self.frame_body, self.FRAME_POINTS)
        self.frame_shape.friction = self.FRAME_FRICTION
        self.frame_body.position = self.start_pos
        self.frame_shape.filter = self.filter_group
        self.space.add(self.frame_body, self.frame_shape)

    def create_driver(self):
        moment = pymunk.moment_for_circle(self.DRIVER_MASS, 0, self.DRIVER_RADIUS)
        self.driver_body = pymunk.Body(self.DRIVER_MASS, moment)
        self.driver_shape = pymunk.Circle(self.driver_body, self.DRIVER_RADIUS)
        self.driver_shape.friction = self.DRIVER_FRICTION
        self.driver_body.position = self.start_pos + self.DRIVER_POS
        self.driver_shape.filter = self.filter_group
        self.driver_shape.collision_type = self.DRIVER_COLLISION_TYPE
        self.space.add(self.driver_body, self.driver_shape)

    def create_frame_joints(self):
        self.frame_joints = [
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
                self.wheels_body[1], self.frame_body, (0, 0), (26.5, -25.0), 31, 40
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
        self.space.add(*self.frame_joints)

    def create_driver_joints(self):
        self.driver_joints = [
            # Frame to driver left
            pymunk.PinJoint(
                self.frame_body,
                self.driver_body,
                (-50, 0),
                (0, 0),
            ),
            # Frame to driver right
            pymunk.PinJoint(
                self.frame_body,
                self.driver_body,
                (50, 0),
                (0, 0),
            ),
        ]
        self.space.add(*self.driver_joints)

    def remove(self):
        self.space.remove(
            *self.wheels_body,
            *self.wheels_shape,
            self.frame_body,
            self.frame_shape,
            self.driver_body,
            self.driver_shape,
            *self.frame_joints,
            *self.driver_joints,
        )

    def update(self, game, delta_t):
        self.apply_control_inputs(game)
        self.apply_lean()
        self.check_joint_break(delta_t)

    def update_when_finished(self, delta_t):
        """Relax and gently stop bike when finished."""
        self.wheels_body[0].angular_velocity *= 0.95
        self.wheels_body[1].angular_velocity *= 0.95
        self.apply_lean(0.0)
        self.check_joint_break(delta_t)

    def apply_control_inputs(self, game):
        accel = game.user_control.accelerating
        braking_l = game.user_control.braking_l
        braking_r = game.user_control.braking_r

        # Accelerate/braking
        if accel > self.CONTROLS_DEAD_ZONE:
            self.wheels_body[0].angular_velocity += accel * self.ACCEL_ANG_VEL
        if (
            braking_l > self.CONTROLS_DEAD_ZONE
            and abs(self.wheels_body[0].angular_velocity) > 0.15
        ):
            self.wheels_body[0].angular_velocity *= 1.0 - braking_l * (
                1.0 - self.BRAKE_FACTOR
            )
        if (
            braking_r > self.CONTROLS_DEAD_ZONE
            and abs(self.wheels_body[1].angular_velocity) > 0.15
        ):
            self.wheels_body[1].angular_velocity *= 1.0 - braking_r * (
                1.0 - self.BRAKE_FACTOR
            )
        # Limit max. wheel velocity
        if self.wheels_body[0].angular_velocity > self.MAX_ANG_VEL:
            self.wheels_body[0].angular_velocity = self.MAX_ANG_VEL
        elif self.wheels_body[0].angular_velocity < -self.MAX_ANG_VEL:
            self.wheels_body[0].angular_velocity = -self.MAX_ANG_VEL

    def apply_lean(self, l=None):
        if l is None:
            l = self.driver_lean

        if l > 0.0:
            self.driver_joints[0].distance = self.DRIVER_JOINT_DIST_L - l * 1.0
            self.driver_joints[1].distance = self.DRIVER_JOINT_DIST_R - l * 36.0
            # Bike tilting to make it easier to counter back flipping (e.g. in
            # wheelie or in air)
            if self.wheel_r_coll == 0:  # only when front wheel doesn't touch ground
                self.tilt(10.0)
        elif l < 0.0:
            self.driver_joints[0].distance = self.DRIVER_JOINT_DIST_L + l * 22.0
            self.driver_joints[1].distance = self.DRIVER_JOINT_DIST_R - l * 2.0
            self.tilt(-10.0)
        else:
            self.driver_joints[0].distance = self.DRIVER_JOINT_DIST_L
            self.driver_joints[1].distance = self.DRIVER_JOINT_DIST_R

    def check_joint_break(self, delta_t):
        for joint in self.frame_joints:
            if joint.impulse / delta_t > self.JOINT_BREAK_THRESHOLD:
                self.bike_broken = True
                self.space.remove(*self.frame_joints)
                self.frame_joints = []
                break

    def tilt(self, amount):
        """Tilt bike forward (pos. amount) or backward (neg. amount)."""
        self.frame_body.angular_velocity += 0.15 * amount
        wheel_l = self.wheels_body[1]
        force = Vec2d(3.5 * amount, 0.0)
        force = force.rotated(-self.angle)
        wheel_l.apply_impulse_at_world_point(force, wheel_l.local_to_world((0.0, 0.0)))

    @property
    def driver_lean(self):
        return self.game.user_control.leaning

    @property
    def crashed(self):
        return self.driver_crash or self.bike_broken

    @property
    def angle(self):
        return self.frame_body.angle

    @property
    def angle_mod2pi(self):
        return self.angle % (-2.0 * math.pi)

    @property
    def start_pos(self):
        return self.game.track_manager.current_track.start

    @property
    def bike_right(self):
        """The outmost right edge x coord."""
        wheels_right = map(
            lambda w: w.position[0] + self.WHEEL_RADIUS, self.wheels_body
        )
        driver_right = self.driver_body.position[0] + self.DRIVER_RADIUS
        return max((*wheels_right, driver_right))

    def on_wheel_r_ground_collision_begin(self):
        self.wheel_r_coll += 1

    def on_wheel_r_ground_collision_separate(self):
        self.wheel_r_coll -= 1

    def on_driver_ground_collision_begin(self):
        self.driver_crash = True
