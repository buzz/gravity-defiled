import pyglet.gl as gl


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def project(self):
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, 0, self.height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def update(self, pos):
        self.x = -int(pos.x - self.width / 2)
        self.y = -int(pos.y - self.height / 2)
