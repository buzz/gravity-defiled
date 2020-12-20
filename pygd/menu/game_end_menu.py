from pygd.menu.menu import Menu


class GameEndMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("Restart", self.restart_game)
        self.add_menu_item("Main menu", self.goto_main_menu)

    def restart_game(self):
        print("restart")

    def goto_main_menu(self):
        self.win.game.show_main_menu()
