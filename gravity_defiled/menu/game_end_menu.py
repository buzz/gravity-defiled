from gravity_defiled.menu.menu import Menu


class GameEndMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("Restart", self.restart_game)
        self.add_menu_item("Main menu", self.main_menu)

    def restart_game(self):
        self.game.restart()

    def main_menu(self):
        self.game.show_main_menu()

    def on_menu_back(self):
        self.main_menu()
