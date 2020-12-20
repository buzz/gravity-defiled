import pyglet
from pyglet.window import key


FONT_COLOR = (0, 0, 0, 255)
FONT_COLOR_SELECTED = (255, 0, 0, 255)
FONT_NAME = ("Verdana", "Helvetica", "Arial")
FONT_SIZE = 20
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
            x=self.menu.win.width // 2,
            y=y,
            anchor_x="center",
            anchor_y="center",
        )
        self.activate_func = activate_func

    def draw(self):
        self.text.draw()

    def on_key_release(self, symbol, _):
        if symbol == key.ENTER and self.activate_func:
            self.activate_func()


class Menu:
    def __init__(self, win, title):
        self.win = win
        self.selected_idx = 0
        self.items = []
        self.y_pos = self.win.height - self.win.height // 5
        self.title_text = pyglet.text.Label(
            title,
            color=FONT_COLOR,
            font_name=FONT_NAME,
            font_size=FONT_SIZE * 1.8,
            x=self.win.width // 2,
            y=self.y_pos,
            anchor_x="center",
            anchor_y="center",
        )
        self.y_pos -= points_to_px(FONT_SIZE)
        self.selected_idx = 0

    def add_menu_item(self, text, activate_func):
        self.y_pos -= points_to_px(FONT_SIZE) + MENU_ITEM_PADDING
        self.items.append(MenuItem(self, text, self.y_pos, activate_func))

    def on_key_press(self, symbol, _):
        if symbol == key.DOWN:
            self.selected_idx += 1
        elif symbol == key.UP:
            self.selected_idx -= 1
        self.selected_idx = min(max(self.selected_idx, 0), len(self.items) - 1)

    def on_key_release(self, symbol, modifiers):
        self.items[self.selected_idx].on_key_release(symbol, modifiers)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            if i == self.selected_idx:
                item.text.color = FONT_COLOR_SELECTED
                item.draw()
                item.text.color = FONT_COLOR
            else:
                item.draw()
