from pygd.menu.menu import Menu


class PauseMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("Resume", self.resume)
        self.add_menu_item("Restart", self.restart_game)
        self.add_menu_item("Main menu", self.main_menu)

    def resume(self):
        self.game.on_pause()

    def restart_game(self):
        self.game.restart()

    def main_menu(self):
        self.game.show_main_menu()

    def on_menu_back(self):
        self.resume()
