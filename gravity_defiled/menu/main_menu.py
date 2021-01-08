from gravity_defiled.menu.menu import Menu


class MainMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_menu_item("Play", self.play)
        self.add_menu_item("Level packs", self.level_pack)
        self.add_menu_item("Quit", self.game.quit)

    def play(self):
        self.game.menu_manager.show("play")

    def level_pack(self):
        self.game.menu_manager.show("levels")
