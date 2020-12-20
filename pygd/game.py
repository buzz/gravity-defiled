import pyglet
import pymunk

from pygd.bike import Bike
from pygd.menu import GameEndMenu, MainMenu
from pygd.window import DebugWindow, MainWindow
from pygd.input import GamepadInput, KeyboardInput
from pygd.track import TrackManager


class PyGd:
    FPS = 60
    DAMPING = 0.95
    GRAVITY = (0.0, 450.0)
    SCREEN_SIZE = (1600, 900)
    TITLE = "PyGD"

    def __init__(self, debug_render=False):
        pyglet.resource.path = ["res"]
        pyglet.resource.reindex()

        self.timestep = 1.0 / self.FPS
        self.playing = False

        self.space = None
        self.track_manager = TrackManager("levels.mrg")
        self.bike = None
        self.current_menu = None

        Window = DebugWindow if debug_render else MainWindow
        caption = f"{self.TITLE}"
        if debug_render:
            caption = f"{caption} - DEBUG RENDER"

        self.win = Window(
            game=self,
            space=self.space,
            width=self.SCREEN_SIZE[0],
            height=self.SCREEN_SIZE[1],
            caption=caption,
        )
        self.keyboard_input = KeyboardInput(self, self.win)
        self.controls = self.keyboard_input
        self.gamepad_input = GamepadInput(self)
        # self.controls = self.gamepad_input

    def show_main_menu(self):
        del self.bike
        self.bike = None
        self.show_menu(MainMenu(self.win, self.TITLE))

    def show_game_end_menu(self, _):
        title = "Crashed!" if self.bike.crashed else "Finish!"
        self.show_menu(GameEndMenu(self.win, title))

    def show_menu(self, menu):
        if self.current_menu:
            self.hide_menu()
        self.win.push_handlers(menu)
        self.current_menu = menu

    def hide_menu(self):
        self.win.remove_handlers(self.current_menu)
        del self.current_menu
        self.current_menu = None

    def create_space(self):
        space = pymunk.Space(threaded=True)
        space.threads = 2
        space.damping = self.DAMPING
        space.gravity = self.GRAVITY
        space.sleep_time_threshold = 0.3
        return space

    def run(self):
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
        self.bike = Bike(self, self.track_manager.current_track.start, self.space)
        self.win.game.hide_menu()
        self.step(self.timestep)  # Initialize positions, so first frame is good
        self.win.update_track(self.track_manager.current_track.points)
        self.win.show_message(self.track_manager.current_track.name)
        self.playing = True

    def step(self, _):
        if self.bike:
            if not self.bike.crashed:
                self.bike.update(self, self.timestep)
            elif self.playing:
                self.playing = False
                self.win.show_message("Crashed!", auto_clear=False)
                pyglet.clock.schedule_once(self.show_game_end_menu, 2.0)
        self.space.step(self.timestep)
