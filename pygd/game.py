import pyglet
import pymunk
from pymunk.vec2d import Vec2d

from pygd.bike import Bike
from pygd.camera import Camera
from pygd.debug_renderer import DebugRendererWindow
from pygd.input_handler import KeyboardInputHandler
from pygd.track import Track, TrackManager


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

        self.track_manager = TrackManager()
        self.bike = None

        self.camera = Camera(*self.SCREEN_SIZE)
        self.renderer = DebugRendererWindow(self.SCREEN_SIZE, self.camera, self.space)
        self.key_listener = KeyboardInputHandler(self, self.renderer)

        # input states
        self.accelerating = False
        self.braking = False

    def run(self):
        # self.start_test_level()
        self.load_mrg()
        self.bike = Bike(self.track_manager.current.start, self.space)
        self.step(self.timestep)
        pyglet.clock.schedule_interval(self.step, self.timestep)
        pyglet.app.run()

    def load_mrg(self):
        track = TrackManager.load_mrg_track("levels.mrg", 0, 1)
        self.track_manager.add(track)
        self.track_manager.current = self.track_manager.tracks[0]
        self.track_manager.add_to_space(self.track_manager.current, self.space)

    def start_test_level(self):
        points = (
            (-200, 880),
            (100, 880),
            (300, 870),
            (350, 865),
            (400, 855),
            (500, 810),
            (600, 760),
            (700, 700),
            (750, 820),
            (800, 810),
            (850, 800),
            (900, 790),
            (1800, 780),
        )
        track = Track(points, Vec2d(100, 860), Vec2d(1500, 860))
        self.track_manager.add(track)
        self.track_manager.current = self.track_manager.tracks[0]
        self.track_manager.add_to_space(self.track_manager.current, self.space)

    def step(self, _):
        self.bike.update(self, self.timestep)
        self.camera.update(self.bike.frame_body.position)
        self.space.step(self.timestep)
