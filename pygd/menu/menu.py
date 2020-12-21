import pyglet


FONT_COLOR = (60, 60, 60, 255)
FONT_COLOR_SELECTED = (200, 0, 0, 255)
FONT_NAME = "Walter Turncoat"
FONT_SIZE = 20
FONT_SIZE_BIG = 36
MENU_ITEM_PADDING = 20


def points_to_px(pt):
    return pt * 4 / 3


class MenuItem:
    pointer_color = (0.46, 0, 1.0)
    inverted_pointers = False

    def __init__(self, menu, text, y, activate_func):
        self.menu = menu
        self.y = y
        self.text = pyglet.text.Label(
            text,
            color=FONT_COLOR,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            x=self.menu.game.win.width // 2,
            y=y,
            anchor_x="center",
            anchor_y="center",
            batch=self.menu.game.win.batch_menu,
        )
        self.activate_func = activate_func

    def delete(self):
        self.text.delete()

    def set_selected(self, selected):
        self.text.color = FONT_COLOR_SELECTED if selected else FONT_COLOR


class Menu:
    def __init__(self, game, title):
        self.game = game
        self.selected_idx = 0
        self.items = []
        self.y_pos = self.game.win.height - self.game.win.height // 5
        self.title_text = pyglet.text.Label(
            title,
            color=FONT_COLOR,
            font_name=FONT_NAME,
            font_size=FONT_SIZE_BIG,
            x=self.game.win.width // 2,
            y=self.y_pos,
            anchor_x="center",
            anchor_y="center",
            batch=self.game.win.batch_menu,
        )
        self.y_pos -= points_to_px(FONT_SIZE)
        self.select()

    def delete(self):
        self.title_text.delete()
        for item in self.items:
            item.delete()

    def add_menu_item(self, text, activate_func):
        self.y_pos -= points_to_px(FONT_SIZE) + MENU_ITEM_PADDING
        self.items.append(MenuItem(self, text, self.y_pos, activate_func))
        self.select()

    def menu_up_down(self, inc):
        idx = self.selected_idx + inc
        idx = min(max(idx, 0), len(self.items) - 1)
        self.select(idx)

    def select(self, idx=None):
        if idx is None:
            try:
                self.items[self.selected_idx].set_selected(True)
            except IndexError:
                pass
        else:
            self.items[self.selected_idx].set_selected(False)
            self.selected_idx = idx
            self.items[self.selected_idx].set_selected(True)

    # Events

    def on_menu_up(self):
        self.menu_up_down(-1)

    def on_menu_down(self):
        self.menu_up_down(1)

    def on_menu_confirm(self):
        self.items[self.selected_idx].activate_func()
