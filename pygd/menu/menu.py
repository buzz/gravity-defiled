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
        )
        self.activate_func = activate_func

    def draw(self):
        self.text.draw()


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
        )
        self.y_pos -= points_to_px(FONT_SIZE)
        self.selected_idx = 0

    def add_menu_item(self, text, activate_func):
        self.y_pos -= points_to_px(FONT_SIZE) + MENU_ITEM_PADDING
        self.items.append(MenuItem(self, text, self.y_pos, activate_func))

    def menu_up_down(self, inc):
        new_idx = self.selected_idx + inc
        self.selected_idx = min(max(new_idx, 0), len(self.items) - 1)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            if i == self.selected_idx:
                item.text.color = FONT_COLOR_SELECTED
                item.draw()
                item.text.color = FONT_COLOR
            else:
                item.draw()

    # Events

    def on_menu_up(self):
        self.menu_up_down(-1)

    def on_menu_down(self):
        self.menu_up_down(1)

    def on_menu_confirm(self):
        self.items[self.selected_idx].activate_func()
