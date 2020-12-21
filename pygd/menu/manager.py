from pyglet import resource

from pygd.menu.game_end_menu import GameEndMenu
from pygd.menu.main_menu import MainMenu
from pygd.menu.pause_menu import PauseMenu


MENUS = {
    "game_end": GameEndMenu,
    "main": MainMenu,
    "pause": PauseMenu,
}


class MenuManager:
    def __init__(self, game):
        self.game = game
        self.current = None
        resource.add_font("walter_turncoat.ttf")

    def show(self, menu_name, title):
        menu = MENUS[menu_name]
        if self.current:
            self.delete()
        self.current = menu(self.game, title)
        self.game.user_control.push_handlers(self.current)

    def delete(self):
        self.game.user_control.remove_handlers(self.current)
        self.current.delete()
        self.current = None
