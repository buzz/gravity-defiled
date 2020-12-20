from pyglet.input import get_joysticks

from pygd.input.base import BaseInput

# XBOX generic
# Stick   L x gamepad.x    lean
# Stick   L y gamepad.y
# Trigger L   gamepad.z    back brake
# Stick   R x gamepad.rx
# Stick   R y gamepad.ry   accel
# Trigger R   gamepad.rz   front brake


class GamepadInput(BaseInput):
    def __init__(self, game, gamepad_num=0):
        super().__init__(game)

        self._accelerating = 0.0
        self._braking_l = 0.0
        self._braking_r = 0.0
        self._leaning = 0.0

        gamepads = get_joysticks()
        if not gamepads:
            raise RuntimeError("No gamepad found!")

        self.gamepad = gamepads[gamepad_num]
        self.gamepad.open()
        self.gamepad.set_handler("on_joybutton_press", self.on_joybutton_press)
        self.gamepad.set_handler("on_joybutton_release", self.on_joybutton_release)
        self.gamepad.set_handler("on_joyaxis_motion", self.on_joyaxis_motion)

    def __del__(self):
        self.gamepad.remove_handler("on_joybutton_press", self.on_joybutton_press)
        self.gamepad.remove_handler("on_joybutton_release", self.on_joybutton_release)
        self.gamepad.set_handler("on_joyaxis_motion", self.on_joyaxis_motion)

    def on_joybutton_press(self, _, button):
        # print("button press:", button)
        pass

    def on_joybutton_release(self, _, button):
        # print("button release:", button)
        if button == 6:
            self.game.reset()

    def on_joyaxis_motion(self, _, axis, value):
        if axis == "ry":
            self._accelerating = max(0.0, -value)
        elif axis == "z":
            self._braking_l = (value + 1.0) / 2.0
        elif axis == "rz":
            self._braking_r = (value + 1.0) / 2.0
        elif axis == "x":
            self._leaning = value

    @property
    def accelerating(self):
        return self._accelerating

    @property
    def braking_l(self):
        return self._braking_l

    @property
    def braking_r(self):
        return self._braking_r

    @property
    def leaning(self):
        return self._leaning
