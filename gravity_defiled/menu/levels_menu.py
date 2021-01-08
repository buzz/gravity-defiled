from gravity_defiled.menu.menu import Menu


class LevelsMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, title="Level packs", **kwargs)

        self.add_menu_item("Original tracks", self.original_tracks)
        self.add_menu_item("Community packs", self.choose_levels)
        self.add_menu_item("back", self.main_menu)

    def original_tracks(self):
        self.game.show_main_menu()

    def choose_levels(self):
        self.game.show_main_menu()

    def main_menu(self):
        self.game.show_main_menu()

    def on_menu_back(self):
        self.main_menu()
