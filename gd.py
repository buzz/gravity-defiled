import sys

import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

fps = 144
accel_ang_vel = 0.4
max_ang_vel = 20.0
brake_factor = 0.8

clock = pygame.time.Clock()
space = pymunk.Space()
space.damping = 0.85
motor = None
screen = pygame.display.set_mode((1600, 900))

draw_options = pymunk.pygame_util.DrawOptions(screen)

# input states
accelerating = False
braking = False


def check_keys():
    global accelerating, braking

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                sys.exit(0)
            elif event.key == pygame.K_UP:
                accelerating = True
            # elif event.key == pygame.K_RIGHT:
            #     input_states[1] = True
            elif event.key == pygame.K_DOWN:
                braking = True
            # elif event.key == pygame.K_LEFT:
            #     input_states[3] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                accelerating = False
            # elif event.key == pygame.K_RIGHT:
            #     input_states[1] = False
            elif event.key == pygame.K_DOWN:
                braking = False
            # elif event.key == pygame.K_LEFT:
            #     input_states[3] = False


def add_floor(space):
    friction = 1.0
    width = 0.0
    segments = (
        (-200, 900),
        (100, 900),
        (200, 890),
        (300, 870),
        (400, 850),
        (500, 810),
        (600, 700),
        (700, 600),
        (750, 550),
        (800, 750),
        (850, 745),
        (900, 735),
        (1800, 725),
    )

    for idx in range(len(segments) - 1):
        p1 = segments[idx]
        p2 = segments[idx + 1]
        floor = pymunk.Segment(space.static_body, p1, p2, width)
        floor.elasticity = 0.5
        floor.friction = friction
        space.add(floor)


def add_bike(space, pos):
    global wheel_l_body

    wheel_radius = 24.5
    wheel_radius_inner = 20.0
    wheel_color = 52, 219, 119, 255
    wheel_friction = 1.4
    wheel_elasticity = 0.5

    wheel_l_pos = (-34.0, 6.0)
    wheel_l_mass = 25
    moment = pymunk.moment_for_circle(wheel_l_mass, wheel_radius_inner, wheel_radius)
    wheel_l_body = pymunk.Body(wheel_l_mass, moment)
    wheel_l_shape = pymunk.Circle(wheel_l_body, wheel_radius)
    wheel_l_shape.friction = wheel_friction
    wheel_l_shape.elasticity = wheel_elasticity
    wheel_l_shape.color = wheel_color
    wheel_l_body.position = pos + wheel_l_pos
    space.add(wheel_l_body, wheel_l_shape)

    wheel_r_pos = (41.0, 6.0)
    wheel_r_mass = 8
    moment = pymunk.moment_for_circle(wheel_r_mass, wheel_radius_inner, wheel_radius)
    wheel_r_body = pymunk.Body(wheel_r_mass, moment)
    wheel_r_shape = pymunk.Circle(wheel_r_body, wheel_radius)
    wheel_r_shape.friction = wheel_friction
    wheel_l_shape.elasticity = wheel_elasticity
    wheel_r_shape.color = wheel_color
    wheel_r_body.position = pos + wheel_r_pos
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
        wheel_l_body, frame_body, (0, 0), frame_point_top_l
    )
    joint_back_bottom = pymunk.PinJoint(
        wheel_l_body, frame_body, (0, 0), frame_point_bottom
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


def main_loop():
    global accelerating, braking, wheel_l_body

    check_keys()
    if accelerating:
        wheel_l_body.angular_velocity += accel_ang_vel
    if braking and abs(wheel_l_body.angular_velocity) > 0.15:
        wheel_l_body.angular_velocity *= brake_factor
    if wheel_l_body.angular_velocity > max_ang_vel:
        wheel_l_body.angular_velocity = max_ang_vel
    elif wheel_l_body.angular_velocity < -max_ang_vel:
        wheel_l_body.angular_velocity = -max_ang_vel

    space.step(1.0 / fps)
    screen.fill(pygame.Color("white"))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(fps)


def main():
    pygame.init()

    space.gravity = 0, 900
    space.sleep_time_threshold = 0.3

    add_floor(space)
    add_bike(space, Vec2d(100, 860))

    moment = pymunk.moment_for_circle(3, 0, 8)
    b = pymunk.Body(3, moment)
    c = pymunk.Circle(b, 8)
    c.friction = 1
    b.position = 200, 0
    space.add(b, c)

    while True:
        main_loop()


if __name__ == "__main__":
    main()
