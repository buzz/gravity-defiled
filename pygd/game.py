import pymunk
import pyglet

from pygd.bike import Bike
from pygd.input import UserControl
from pygd.menu import MenuManager
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
        self.finished = False
        self.paused = False

        self.bike = None
        self.menu_manager = MenuManager(self)
        self.space = None
        self.track_manager = TrackManager("levels.mrg")
        self.user_control = None
        self.win = None

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
        self.user_control = UserControl(self)
        self.user_control.set_handler("on_pause", self.on_pause)
        self.space = self.create_space()
        self.show_main_menu()
        pyglet.clock.schedule_interval(self.step, self.timestep)
        pyglet.app.run()

    def start_track(self, level, track):
        self.track_manager.load_mrg_track(level, track)
        self.track_manager.add_to_space(self.track_manager.current, self.space)
        self.win.update_track(self.track_manager.current)
        self.restart()

    def restart(self):
        self.reset_bike()
        self.menu_manager.hide()
        self.playing = True
        self.finished = False
        self.paused = False
        self.win.show_message(self.track_manager.current.name, timeout=2.5)

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
                timeout = 0.8
                text = "Crashed!"
                self.win.show_message(text, timeout=timeout)
                pyglet.clock.schedule_once(self.show_game_end_menu, 0.8, text)
            elif self.playing and not self.paused:
                if self.track_manager.current.is_finished(self.bike):
                    self.playing = False
                    self.finished = True
                    timeout = 2.0
                    text = "Finished!"
                    self.win.show_message(text, timeout=timeout)
                    pyglet.clock.schedule_once(self.show_game_end_menu, timeout, text)
                self.bike.update(self, self.timestep)
            elif self.finished:
                self.bike.update_when_finished(self.timestep)
        if not self.paused:
            self.space.step(self.timestep)

    # Menus

    def show_main_menu(self):
        self.remove_bike()
        self.menu_manager.show("main", self.TITLE)

    def show_game_end_menu(self, _, title):
        self.menu_manager.show("game_end", title)

    # Events

    def on_pause(self):
        if self.playing:
            if self.paused:
                self.paused = False
                self.menu_manager.hide()
            else:
                self.paused = True
                self.menu_manager.show("pause", "Pause")

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
