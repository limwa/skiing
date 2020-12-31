""" Holds all important constants that define the game's behaviour """

import os
import math

from pygame import Vector2, Rect

# EDIT THESE CONSTANTS AT YOUR WILL
# SCREEN CONSTANTS
WIDTH = 800
HEIGHT = 600

# TIME CONSTANTS
TIME_ADJUST = 0.001  # conversion of ms to s
DIFICULTY_MULTIPLIER = 1
assert DIFICULTY_MULTIPLIER > 0

# ENVIRONMENT CONSTANTS
G = 100
PLANE_INCLINATION = 60  # inclination of the plane in degrees
FRICTION_CONSTANT = 0.4  # must be lower than 1
assert G > 0
assert 0 < PLANE_INCLINATION < 90
assert 0 <= FRICTION_CONSTANT < 1

# CAMERA CONSTANTS
CAMERA_PADDING = 50
CAMERA_TRACKING_BOUND = 100
assert CAMERA_TRACKING_BOUND >= CAMERA_PADDING

# FLAG HORIZONTAL CONSTANTS
FLAG_PADDING = 100
FLAG_SPACING_HORIZONTAL = 200

# FLAG VERTICAL CONSTANTS
FLAGS_START = 300
FLAGS_SPACING_VERTICAL = 250



### DON'T EDIT ANYTHING ELSE
TIME_SCALAR = DIFICULTY_MULTIPLIER * TIME_ADJUST
PLANE_ACCELERATION = G * math.sin(math.radians(PLANE_INCLINATION))

# ASSETS
ROOT = os.path.join(os.path.dirname(__file__), '..')
ASSETS = os.path.join(ROOT, 'assets')

# TYPES
COORDINATE = (int, float)
VECTOR = (list, tuple, Vector2, Rect)
###
