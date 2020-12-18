import pyglet.gl as gl


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def project(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glViewport(self.x, self.y, self.width, self.height)
        gl.glOrtho(0, self.width, 0, self.height, -50, 50)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def project_hud(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glViewport(0, 0, 1600, 900)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def update(self, pos):
        self.x = -int(pos.x - self.width / 2)
        self.y = int(pos.y - self.height / 2)
