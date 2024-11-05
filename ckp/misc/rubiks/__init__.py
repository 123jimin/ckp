"""
    Data structures and algorithms related to Rubik's cube.

    ## Cube State

    This package supports two methods for representing a Rubik's cube.

    1. Using face colors
    2. Using corner/edge permutations and orientations

    Internally, the second method is used.

    ## Cube Move

    A move consists of an integer.
    - Bits 0-1: Amount of quarter turns.
      - Clockwise (w.r.t. layer direction) when layer number is even, counter-clockwise when layer number is odd
    - Bits 2-3: Layer direction.
      - 0=U, 1=F, 2=R
    - Rest bits: Layer number.
      - For example, when layer direction is 0, layer 0 is U, and layer 1 is D.

    U, D, F, B, R, L are 1, 17, 5, 21, 9, 25 respectively.
    U', D', F', B', R', L' are 3, 19, 7, 23, 11, 27 respectively.
"""

from .corner import *
from .edge import *
from .move import *