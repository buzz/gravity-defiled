from gravity_defiled.menu.menu import Menu


class PlayMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("Start", self.start)
        self.add_menu_item("Choose track", self.choose_track)
        self.add_menu_item("back", self.main_menu)

    def start(self):
        self.game.start_track()

    def choose_track(self):
        # TODO
        pass

    def main_menu(self):
        self.game.show_main_menu()

    def on_menu_back(self):
        self.main_menu()
