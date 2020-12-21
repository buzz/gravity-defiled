from pyglet.graphics import Batch
import pyglet.gl as gl


class PolyLine:
    def __init__(
        self,
        vertices,
        batch,
        group,
        close=False,
        width=1.0,
        color=(0, 0, 0),
        vertex_usage="dynamic",
    ):
        self._draw_mode = gl.GL_LINE_LOOP if close else gl.GL_LINE_STRIP

        self._width = width
        self._rgb = color

        self._batch = batch or Batch()
        self._group = group

        self._vertex_list = self._batch.add(
            len(vertices),
            self._draw_mode,
            self._group,
            f"v2f/{vertex_usage}",
            "c3B/static",
        )
        self.update(vertices)

    def draw(self):
        self._vertex_list.draw(self._draw_mode)

    def update(self, vertices):
        if self._vertex_list.get_size() != len(vertices):
            self._vertex_list.resize(len(vertices))
        _vertices = []
        for v in vertices:
            _vertices.extend(v)
        self._vertex_list.vertices[:] = _vertices
        self._vertex_list.colors[:] = self._rgb * len(vertices)
