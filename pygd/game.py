import pyglet
import pymunk

from pygd.bike import Bike
from pygd.camera import Camera
from pygd.debug_renderer import DebugRendererWindow
from pygd.input_handler import KeyboardInputHandler
from pygd.track import Track


class PyGd:
    FPS = 60
    DAMPING = 0.85
    SCREEN_SIZE = (1600, 900)

    def __init__(self):
        self.timestep = 1.0 / self.FPS
        self.space = pymunk.Space()
        self.space.damping = self.DAMPING
        self.space.gravity = 0, 900
        self.space.sleep_time_threshold = 0.3

        self.camera = Camera(*self.SCREEN_SIZE)
        self.renderer = DebugRendererWindow(self.SCREEN_SIZE, self.camera, self.space)
        self.key_listener = KeyboardInputHandler(self, self.renderer)

        # input states
        self.accelerating = False
        self.braking = False

    def run(self):
        pyglet.clock.schedule_interval(self.step, self.timestep)

        points = (
            (-200, 880),
            (100, 880),
            (300, 870),
            (350, 865),
            (400, 855),
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

        self.step(self.timestep)
        pyglet.app.run()

    def step(self, _):
        self.bike.update(self, self.timestep)
        self.camera.update(self.bike.frame_body.position)
        self.space.step(self.timestep)
