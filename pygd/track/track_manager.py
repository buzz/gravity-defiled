import pymunk

from pygd.track import Track
from pygd.track.mrg import MrgFile


class TrackManager:
    def __init__(self, level_filename):
        self.level_filename = level_filename
        self.level_idx = 0
        self.track_idx = 0
        self.current_track = None

        # Current track's pymunk segments
        self.segments = None

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

    def load_mrg_track(self, level=0, track=0):
        mrg_file = MrgFile.from_file(self.level_filename)
        track = mrg_file.read_track_from_file(level, track)
        self.current_track = track
