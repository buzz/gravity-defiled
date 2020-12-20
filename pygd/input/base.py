class BaseInput:
    def __init__(self, game):
        self.game = game

    @property
    def accelerating(self):
        raise NotImplementedError

    @property
    def braking_l(self):
        raise NotImplementedError

    @property
    def braking_r(self):
        raise NotImplementedError

    @property
    def leaning(self):
        raise NotImplementedError
