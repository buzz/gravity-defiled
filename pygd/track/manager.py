import pymunk

from pygd.track import Track
from pygd.track.mrg import MrgFile


class TrackManager:
    def __init__(self, level_filename, level_idx=None, track_idx=None):
        self.level_filename = level_filename
        self.level_idx = 0 if level_idx is None else level_idx
        self.track_idx = 0 if track_idx is None else track_idx
        self.current = None

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

    def load_mrg_track(self, level_idx=None, track_idx=None):
        if level_idx is not None:
            self.level_idx = level_idx
        if track_idx is not None:
            self.track_idx = track_idx
        mrg_file = MrgFile.from_file(self.level_filename)
        track = mrg_file.read_track_from_file(self.level_idx, self.track_idx)
        self.current = track
