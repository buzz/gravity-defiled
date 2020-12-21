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
    DEAD_ZONE = 0.05

    def __init__(self, user_control, gamepad_num=0):
        super().__init__(user_control)

        gamepads = get_joysticks()  # pylint: disable=assignment-from-no-return
        if not gamepads:
            raise RuntimeError("No gamepad found!")

        self.gamepad = gamepads[gamepad_num]
        self.gamepad.open()
        self.gamepad.set_handler("on_joybutton_press", self.on_joybutton_press)
        self.gamepad.set_handler("on_joyaxis_motion", self.on_joyaxis_motion)

    def on_joybutton_press(self, _, button):
        if button == 0:
            self.user_control.menu_confirm()
        if button == 1:
            self.user_control.menu_back()
        elif button == 7:
            self.user_control.pause()

    def on_joyaxis_motion(self, _, axis, val):
        if axis == "x":
            self.user_control.leaning = val
        elif axis == "ry":
            self.user_control.accelerating = max(0.0, -val)
        elif axis == "z":
            self.user_control.braking_l = (val + 1.0) / 2.0
        elif axis == "rz":
            self.user_control.braking_r = (val + 1.0) / 2.0
        elif axis == "hat_x":
            self.user_control.leaning = val
        elif axis == "hat_y":
            if val > self.DEAD_ZONE:
                self.user_control.accelerating = max(0.0, val)
                self.user_control.menu_up()
            elif val < -self.DEAD_ZONE:
                self.user_control.braking_l = max(0.0, val)
                self.user_control.menu_down()
