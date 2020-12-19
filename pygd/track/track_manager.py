import pymunk

from pygd.track import Track
from pygd.track.mrg import MrgFile


class TrackManager:
    def __init__(self):
        self.tracks = []
        self.current = None

        # Current track's pymunk segments
        self.segments = None

    def add(self, track):
        self.tracks.append(track)
        return track

    def add_to_space(self, track, space):
        # Remove previous segments
        if self.segments:
            for segment in self.segments:
                space.remove(segment)
        self.segments = []

        # Generate segments from points
        for idx in range(len(track.points) - 1):
            point_1 = track.points[idx]
            point_2 = track.points[idx + 1]
            segment = pymunk.Segment(space.static_body, point_1, point_2, Track.WIDTH)
            segment.collision_type = Track.COLLISION_TYPE
            segment.elasticity = Track.ELASTICITY
            segment.friction = Track.FRICTION
            self.segments.append(segment)
            space.add(segment)

    @staticmethod
    def load_mrg_track(filepath, level=0, track=0):
        mrg_file = MrgFile.from_file(filepath)
        return mrg_file.read_track_from_file(level, track)
