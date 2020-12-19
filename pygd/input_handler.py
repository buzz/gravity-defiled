from pyglet.window import key


class KeyboardInputHandler:
    def __init__(self, game, win):
        self.game = game
        self.win = win
        self.win.set_handler("on_key_press", self.on_key_press)
        self.win.set_handler("on_key_release", self.on_key_release)

    def __del__(self):
        self.win.remove_handler("on_key_press", self.on_key_press)
        self.win.remove_handler("on_key_release", self.on_key_press)

    def on_key_press(self, symbol, _):
        # Driver control
        if symbol == key.UP:
            self.game.accelerating = True
        elif symbol == key.DOWN:
            self.game.braking = True
        elif symbol == key.LEFT:
            self.game.leaning_l = True
        elif symbol == key.RIGHT:
            self.game.leaning_r = True

    def on_key_release(self, symbol, _):
        # Driver control
        if symbol == key.UP:
            self.game.accelerating = False
        elif symbol == key.DOWN:
            self.game.braking = False
        elif symbol == key.LEFT:
            self.game.leaning_l = False
        elif symbol == key.RIGHT:
            self.game.leaning_r = False

        # Other
        elif symbol in (key.Q, key.ESCAPE):
            self.win.close()
