import pyglet
import pymunk
from pymunk.vec2d import Vec2d

from pygd.bike import Bike
from pygd.renderer import Camera, DebugRendererWindow, RendererWindow
from pygd.input_handler import KeyboardInputHandler
from pygd.track import Track, TrackManager


class PyGd:
    FPS = 60
    DAMPING = 0.85
    SCREEN_SIZE = (1600, 900)
    TITLE = "PyGD"

    def __init__(self, debug_render=False):
        self.timestep = 1.0 / self.FPS
        self.space = pymunk.Space()
        self.space.damping = self.DAMPING
        self.space.gravity = 0, 900
        self.space.sleep_time_threshold = 0.3

        pyglet.resource.path = ["res"]
        pyglet.resource.reindex()

        self.track_manager = TrackManager()
        self.bike = None

        self.camera = Camera(*self.SCREEN_SIZE)
        Window = DebugRendererWindow if debug_render else RendererWindow
        caption = f"{self.TITLE}"
        if debug_render:
            caption = f"{caption} - DEBUG RENDER"

        self.renderer = Window(
            game=self,
            camera=self.camera,
            space=self.space,
            width=self.SCREEN_SIZE[0],
            height=self.SCREEN_SIZE[1],
            caption=caption,
        )
        self.key_listener = KeyboardInputHandler(self, self.renderer)

        # input states
        self.accelerating = False
        self.braking = False

    def run(self):
        # self.start_test_level()
        self.load_mrg(0, 9)
        self.bike = Bike(self.track_manager.current.start, self.space)
        self.step(self.timestep)
        self.renderer.update_track(self.track_manager.current.points)
        pyglet.clock.schedule_interval(self.step, self.timestep)
        pyglet.app.run()

    def load_mrg(self, level, track):
        track = TrackManager.load_mrg_track("levels.mrg", level, track)
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
        track = Track(points, Vec2d(100, 560), Vec2d(1500, 860))
        self.track_manager.add(track)
        self.track_manager.current = self.track_manager.tracks[0]
        self.track_manager.add_to_space(self.track_manager.current, self.space)

    def step(self, _):
        self.bike.update(self, self.timestep)
        self.camera.update(self.bike.frame_body.position)
        self.space.step(self.timestep)
