from pyglet.event import EventDispatcher

from gravity_defiled.input.gamepad import GamepadInput
from gravity_defiled.input.keyboard import KeyboardInput


class UserControl(EventDispatcher):
    def __init__(self, game):
        self.keyboard_input = KeyboardInput(self, game)
        self.gamepad_input = GamepadInput(self)

        self.accelerating = 0.0
        self.braking_l = 0.0
        self.braking_r = 0.0
        self.leaning = 0.0

    def pause(self):
        self.dispatch_event("on_pause")

    def menu_up(self):
        self.dispatch_event("on_menu_up")

    def menu_down(self):
        self.dispatch_event("on_menu_down")

    def menu_confirm(self):
        self.dispatch_event("on_menu_confirm")

    def menu_back(self):
        self.dispatch_event("on_menu_back")


UserControl.register_event_type("on_pause")
UserControl.register_event_type("on_menu_up")
UserControl.register_event_type("on_menu_down")
UserControl.register_event_type("on_menu_confirm")
UserControl.register_event_type("on_menu_back")
