from pyglet import resource

from gravity_defiled.menu.game_end_menu import GameEndMenu
from gravity_defiled.menu.levels_menu import LevelsMenu
from gravity_defiled.menu.main_menu import MainMenu
from gravity_defiled.menu.pause_menu import PauseMenu
from gravity_defiled.menu.play_menu import PlayMenu


MENUS = {
    "game_end": GameEndMenu,
    "levels": LevelsMenu,
    "main": MainMenu,
    "pause": PauseMenu,
    "play": PlayMenu,
}


class MenuManager:
    def __init__(self, game):
        self.game = game
        self.current = None
        resource.add_font("walter_turncoat.ttf")

    def show(self, menu_name, title=None):
        if self.game.debug_render:
            return
        self.delete()
        self.current = MENUS[menu_name](self.game)
        if title is not None:
            self.current.set_title(title)
        self.game.user_control.push_handlers(self.current)

    def delete(self):
        try:
            self.game.user_control.remove_handlers(self.current)
            self.current.delete()
            self.current = None
        except AttributeError:
            pass
