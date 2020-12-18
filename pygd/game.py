import sys

import pygame
import pymunk
import pymunk.pygame_util

from pygd.bike import Bike
from pygd.track import Track


class PyGd:
    FPS = 60
    DAMPING = 0.85

    def __init__(self):
        self.space = pymunk.Space()
        self.space.damping = self.DAMPING
        self.space.gravity = 0, 900
        self.space.sleep_time_threshold = 0.3

        self.clock = pygame.time.Clock()
        self.screen = None
        self.draw_options = None

        # input states
        self.accelerating = False
        self.braking = False

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        points = (
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
        self.track = Track.from_points(points, self.space)
        self.bike = Bike(pymunk.Vec2d(100, 860), self.space)

        self.main_loop()

    def main_loop(self):
        while True:
            self.process_events()
            self.bike.update(self)
            self.space.step(1.0 / self.FPS)
            self.screen.fill(pygame.Color("white"))
            self.space.debug_draw(self.draw_options)
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    sys.exit(0)
                elif event.key == pygame.K_UP:
                    self.accelerating = True
                # elif event.key == pygame.K_RIGHT:
                #     input_states[1] = True
                elif event.key == pygame.K_DOWN:
                    self.braking = True
                # elif event.key == pygame.K_LEFT:
                #     input_states[3] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.accelerating = False
                # elif event.key == pygame.K_RIGHT:
                #     input_states[1] = False
                elif event.key == pygame.K_DOWN:
                    self.braking = False
                # elif event.key == pygame.K_LEFT:
                #     input_states[3] = False
