import numpy as np
import json
from typing import Dict


class GPSClassifier:
    def __init__(self, config_path: str):
        # Loading an external JSON configuration.
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.region_a = self.config['regions']['A']
        self.region_b = self.config['regions']['B']
        self.current_pos = np.array([0.0, 0.0])

    def _calculate_shortest_dist(self, point: np.ndarray, region: Dict) -> float:
        """
        Calculates the shortest distance to the rectangle boundary.
        Returns negative if inside, positive if outside.
        """

        center = np.array(region['center'])
        dimensions = np.array([region['width'], region['height']])

        # Transform point to local rectangle space
        # Center the point and use symmetry (absolute values)
        p = np.abs(point - center) - (dimensions / 2.0)

        # Distance calculation
        # Distance if outside, vector to the nearest edge
        p_pos = np.maximum(p, 0.0)
        outside_dist = np.sqrt(np.sum(p_pos**2))
        # Distance if inside (distance to the closest edge, which is the max component of p)
        inside_dist = np.minimum(np.max(p), 0.0)

        return outside_dist + inside_dist

    def dist_a(self) -> float:
        # Get shortest-distance value for A.
        return self._calculate_shortest_dist(self.current_pos, self.region_a)

    def dist_b(self) -> float:
        # Get shortest-distance value for B.
        return self._calculate_shortest_dist(self.current_pos, self.region_b)

    def classify(self) -> str:
        # Run-time region selection and return status.
        da = self.dist_a()
        db = self.dist_b()

        if da <= 0:
            return "IN_REGION_A"
        elif db <= 0:
            return "IN_REGION_B"
        else:
            return "OUTSIDE"

    def update_position(self, x: float, y: float):
        # Updates the sensor's current 2D coordinates.
        self.current_pos = np.array([float(x), float(y)])
