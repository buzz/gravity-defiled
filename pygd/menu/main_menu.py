from pygd.menu.menu import Menu


class MainMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("New Game", self.new_game)
        self.add_menu_item("Quit", self.game.quit)

    def new_game(self):
        self.game.start_track()
