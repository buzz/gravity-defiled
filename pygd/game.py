import pymunk
import pyglet

from pygd.bike import Bike
from pygd.input import UserControl
from pygd.menu import GameEndMenu, MainMenu, PauseMenu
from pygd.window import DebugWindow, MainWindow
from pygd.track import TrackManager, Track


class PyGd:
    FPS = 60
    DAMPING = 0.95
    GRAVITY = (0.0, 450.0)
    SCREEN_SIZE = (1600, 900)
    TITLE = "PyGD"

    def __init__(self, debug_render=False):
        self.debug_render = debug_render

        pyglet.resource.path = ["res"]
        pyglet.resource.reindex()

        self.timestep = 1.0 / self.FPS
        self.playing = False
        self.paused = False

        self.space = None
        self.track_manager = TrackManager("levels.mrg")
        self.bike = None
        self.current_menu = None
        self.win = None
        self.user_control = None

    def show_main_menu(self):
        self.remove_bike()
        self.show_menu(MainMenu(self, self.TITLE))

    def show_pause_menu(self):
        self.show_menu(PauseMenu(self, "Pause"))

    def show_game_end_menu(self, _):
        title = "Crashed!" if self.bike.crashed else "Finish!"
        self.show_menu(GameEndMenu(self, title))

    def show_menu(self, menu):
        if self.current_menu:
            self.hide_menu()
        self.current_menu = menu
        self.user_control.push_handlers(self.current_menu)

    def hide_menu(self):
        self.user_control.remove_handlers(self.current_menu)
        self.current_menu = None

    def create_space(self):
        space = pymunk.Space(threaded=True)
        space.threads = 2
        space.damping = self.DAMPING
        space.gravity = self.GRAVITY
        space.sleep_time_threshold = 0.3

        # Collision handlers
        h = space.add_collision_handler(
            Bike.WHEEL_R_COLLISION_TYPE, Track.COLLISION_TYPE
        )
        h.begin = self.on_wheel_r_ground_collision_begin
        h.separate = self.on_wheel_r_ground_collision_separate
        h = space.add_collision_handler(
            Bike.DRIVER_COLLISION_TYPE, Track.COLLISION_TYPE
        )
        h.begin = self.on_driver_ground_collision_begin

        return space

    def create_window(self):
        Window = DebugWindow if self.debug_render else MainWindow
        caption = f"{self.TITLE}"
        if self.debug_render:
            caption = f"{caption} - DEBUG RENDER"
        win = Window(
            game=self,
            space=self.space,
            width=self.SCREEN_SIZE[0],
            height=self.SCREEN_SIZE[1],
            caption=caption,
        )
        return win

    def run(self):
        self.win = self.create_window()
        self.user_control = UserControl(self.win)
        self.user_control.set_handler("on_pause", self.on_pause)
        self.space = self.create_space()
        self.show_main_menu()
        pyglet.clock.schedule_interval(self.step, self.timestep)
        pyglet.app.run()

    # def start_test_level(self):
    #     points = (
    #         (-200, 880),
    #         (100, 880),
    #         (300, 870),
    #         (350, 865),
    #         (400, 855),
    #         (500, 810),
    #         (600, 760),
    #         (700, 700),
    #         (750, 820),
    #         (800, 810),
    #         (850, 800),
    #         (900, 790),
    #         (1800, 780),
    #     )
    #     track = Track(points, Vec2d(0, 860), Vec2d(1500, 860))
    #     self.track_manager.add(track)
    #     self.track_manager.current = self.track_manager.tracks[0]
    #     self.track_manager.add_to_space(self.track_manager.current, self.space)

    def start_track(self, level, track):
        # self.start_test_level()
        self.track_manager.load_mrg_track(level, track)
        self.track_manager.add_to_space(self.track_manager.current_track, self.space)
        self.win.update_track(self.track_manager.current_track.points)
        self.restart()

    def restart(self):
        self.reset_bike()
        self.hide_menu()
        self.playing = True
        self.paused = False
        self.win.show_message(self.track_manager.current_track.name)

    def remove_bike(self):
        if self.bike:
            self.bike.remove()
            self.bike = None

    def reset_bike(self):
        self.remove_bike()
        self.bike = Bike(self, self.space)

    def quit(self):
        self.win.close()

    def step(self, _):
        if self.bike:
            if self.bike.crashed and self.playing:
                self.playing = False
                pyglet.clock.schedule_once(self.show_game_end_menu, 0.8)
            elif self.playing and not self.paused:
                self.bike.update(self, self.timestep)
        if not self.paused:
            self.space.step(self.timestep)

    # Events

    def on_pause(self):
        if self.playing:
            if self.paused:
                self.paused = False
                self.hide_menu()
            else:
                self.paused = True
                self.show_pause_menu()

    # Physics events

    def on_wheel_r_ground_collision_begin(self, *_):
        if self.bike:
            self.bike.on_wheel_r_ground_collision_begin()
        return True

    def on_wheel_r_ground_collision_separate(self, *_):
        if self.bike:
            self.bike.on_wheel_r_ground_collision_separate()

    def on_driver_ground_collision_begin(self, *_):
        if self.bike:
            self.bike.on_driver_ground_collision_begin()
        return True
