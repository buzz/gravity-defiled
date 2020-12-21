"""
MRG file reader.

See:
http://gdtr.net/handbook/mrg/
https://wiki.gdmod.ru/Структура_файла_levels.mrg (Russian)
"""

import struct
import os

from pymunk.vec2d import Vec2d

from pygd.track import Track


class MrgHeader:
    MAX_VALID_TRACKS = 16384

    def __init__(self):
        self.pointers = [[] for _ in range(3)]
        self.names = [[] for _ in range(3)]
        self.counts = [0 for _ in range(3)]

    def init_lists(self, level, count):
        self.pointers[level] = [0 for _ in range(count)]
        self.names[level] = ["" for _ in range(count)]
        self.counts[level] = count

    def get_count(self, level):
        return self.counts[level]

    def __repr__(self):
        counts = f"({self.counts[0]}, {self.counts[1]}, {self.counts[2]})"
        return f"<MrgHeader counts={counts}>"

    @classmethod
    def from_file(cls, filepath):
        header = cls()
        with open(filepath, "rb") as fin:
            for i in range(3):
                (t_count,) = struct.unpack(">i", fin.read(4))
                if t_count > cls.MAX_VALID_TRACKS:
                    fin.close()
                    raise ValueError("Invalid level file: Too many tracks")
                header.init_lists(i, t_count)

                for j in range(header.get_count(i)):
                    (t_pointer,) = struct.unpack(">i", fin.read(4))
                    header.pointers[i][j] = t_pointer
                    buf = b""
                    while True:
                        (byte_read,) = struct.unpack(">s", fin.read(1))
                        if byte_read == b"\x00":
                            name = buf.decode("cp1251").replace("_", " ")
                            header.names[i][j] = name
                            break
                        buf += byte_read

            return header


class MrgFile:
    SCALE_FACTOR = 0.00034

    def __init__(self, filepath):
        self.filepath = filepath
        self.header = None

    @classmethod
    def from_file(cls, filepath):
        mrg_file = cls(filepath)
        mrg_file.header = MrgHeader.from_file(filepath)
        return mrg_file

    def read_track_from_file(self, level, track_num):
        with open(self.filepath, "rb") as fin:
            points = []
            pos = self.header.pointers[level][track_num]
            fin.seek(pos)
            byte_read = struct.unpack("b", fin.read(1))[0]
            if byte_read == 50:
                fin.seek(20, os.SEEK_CUR)
            start_x = struct.unpack(">i", fin.read(4))[0]
            start_y = -struct.unpack(">i", fin.read(4))[0]
            finish_x = struct.unpack(">i", fin.read(4))[0]
            _ = struct.unpack(">i", fin.read(4))[0]
            points_to_read = struct.unpack(">h", fin.read(2))[0]
            point_0_x = struct.unpack(">i", fin.read(4))[0]
            point_0_y = struct.unpack(">i", fin.read(4))[0]
            points.append(self.scale_point(self.unpack_int(point_0_x, point_0_y)))

            k1 = point_0_x
            l1 = point_0_y
            i = 0
            while i < points_to_read:
                byte0 = struct.unpack("b", fin.read(1))[0]
                if byte0 == -1:
                    k1 = l1 = 0
                    x = struct.unpack(">i", fin.read(4))[0]
                    y = struct.unpack(">i", fin.read(4))[0]
                else:
                    x = byte0
                    y = struct.unpack("b", fin.read(1))[0]
                k1 += x
                l1 += y
                points.append(self.scale_point(self.unpack_int(k1, l1)))
                i += 1

            return Track(
                self.header.names[level][track_num],
                points,
                self.scale_point(Vec2d(start_x, start_y)),
                self.scale_point(finish_x),
            )

    @classmethod
    def scale_point(cls, point):
        return point * cls.SCALE_FACTOR

    @staticmethod
    def unpack_int(x, y):
        return Vec2d((x << 16) >> 3, -((y << 16) >> 3))
