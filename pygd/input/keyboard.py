from pyglet.window import key

from pygd.input.base import BaseInput


class KeyboardInput(BaseInput):
    def __init__(self, game, win):
        super().__init__(game)
        self.win = win

        self._accelerating = 0.0
        self._braking = 0.0
        self._leaning_l = False
        self._leaning_r = False

        self.win.set_handler("on_key_press", self.on_key_press)
        self.win.set_handler("on_key_release", self.on_key_release)

    def __del__(self):
        self.win.remove_handler("on_key_press", self.on_key_press)
        self.win.remove_handler("on_key_release", self.on_key_press)

    def on_key_press(self, symbol, _):
        # Driver control
        if symbol == key.UP:
            self._accelerating = 1.0
        elif symbol == key.DOWN:
            self._braking = 0.6
        elif symbol == key.LEFT:
            self._leaning_l = True
        elif symbol == key.RIGHT:
            self._leaning_r = True

    def on_key_release(self, symbol, _):
        # Driver control
        if symbol == key.UP:
            self._accelerating = 0.0
        elif symbol == key.DOWN:
            self._braking = 0.0
        elif symbol == key.LEFT:
            self._leaning_l = False
        elif symbol == key.RIGHT:
            self._leaning_r = False

        # Other
        elif symbol in (key.Q, key.ESCAPE):
            self.win.close()

    @property
    def accelerating(self):
        return self._accelerating

    @property
    def braking_l(self):
        return self._braking

    @property
    def braking_r(self):
        return self._braking

    @property
    def leaning(self):
        if self._leaning_r:
            return 1.0
        elif self._leaning_l:
            return -1.0
        return 0.0
