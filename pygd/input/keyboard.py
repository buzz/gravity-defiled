from pyglet.window import key

from pygd.input.base import BaseInput


class KeyboardInput(BaseInput):
    def __init__(self, user_control, win):
        super().__init__(user_control)
        self.win = win

        self.win.set_handler("on_key_press", self.on_key_press)
        self.win.set_handler("on_key_release", self.on_key_release)

    def on_key_press(self, symbol, _):
        if symbol == key.UP:
            self.user_control.accelerating = 1.0
        elif symbol == key.DOWN:
            self.user_control.braking_l = 0.6
        elif symbol == key.LEFT:
            self.user_control.leaning = -1.0
        elif symbol == key.RIGHT:
            self.user_control.leaning = 1.0

    def on_key_release(self, symbol, _):
        if symbol == key.UP:
            self.user_control.accelerating = 0.0
            self.user_control.menu_up()
        elif symbol == key.DOWN:
            self.user_control.braking_l = 0.0
            self.user_control.menu_down()
        elif symbol in (key.LEFT, key.RIGHT):
            self.user_control.leaning = 0.0
        elif symbol == key.ENTER:
            self.user_control.menu_confirm()
        elif symbol == key.P:
            self.user_control.pause()
        elif symbol == key.ESCAPE:
            self.user_control.pause()
            self.user_control.menu_back()
