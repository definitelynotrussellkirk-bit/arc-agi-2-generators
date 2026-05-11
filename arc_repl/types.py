"""
ARC REPL Type System — all primitive types in one place.

Types:
  Grid          2D array of ints 0-9
  Mask          2D array of {0, 1} (subtype of Grid conceptually)
  Shape         Portable pattern with center point
  Object        Connected component with properties
  Pos           (r, c) position
  Dir           (dr, dc) direction vector
  Region        (r1, c1, r2, c2) bounding box
  Color         int 0-9
  LayeredGrid   10-layer binary representation

All types are self-evaluating in the S-expression evaluator.
"""

import numpy as np


# ============================================================
# Grid
# ============================================================

class Grid:
    """2D matrix of ints 0-9. The fundamental ARC value."""
    __slots__ = ('data', 'height', 'width')

    def __init__(self, data):
        if isinstance(data, np.ndarray):
            data = data.tolist()
        self.data = data
        self.height = len(data)
        self.width = len(data[0]) if data else 0

    def __repr__(self):
        return f"Grid({self.height}x{self.width})"

    def __eq__(self, other):
        if isinstance(other, Grid):
            return self.data == other.data
        if isinstance(other, list):
            return self.data == other
        return False

    def __hash__(self):
        return id(self)


# ============================================================
# Position and Direction
# ============================================================

class Pos:
    """(r, c) grid position."""
    __slots__ = ('r', 'c')

    def __init__(self, r, c):
        self.r = int(r)
        self.c = int(c)

    def __repr__(self):
        return f"Pos({self.r},{self.c})"

    def __eq__(self, other):
        return isinstance(other, Pos) and self.r == other.r and self.c == other.c

    def __hash__(self):
        return hash((self.r, self.c))

    def __add__(self, other):
        if isinstance(other, Dir):
            return Pos(self.r + other.dr, self.c + other.dc)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Pos):
            return Dir(self.r - other.r, self.c - other.c)
        return NotImplemented

    def to_list(self):
        return [self.r, self.c]


class Dir:
    """(dr, dc) direction vector."""
    __slots__ = ('dr', 'dc')

    def __init__(self, dr, dc):
        self.dr = int(dr)
        self.dc = int(dc)

    def __repr__(self):
        return f"Dir({self.dr},{self.dc})"

    def __eq__(self, other):
        return isinstance(other, Dir) and self.dr == other.dr and self.dc == other.dc

    def __hash__(self):
        return hash((self.dr, self.dc))

    def __mul__(self, scalar):
        return Dir(self.dr * scalar, self.dc * scalar)

    def __neg__(self):
        return Dir(-self.dr, -self.dc)

    def to_list(self):
        return [self.dr, self.dc]


# ============================================================
# Region
# ============================================================

class Region:
    """(r1, c1, r2, c2) bounding box."""
    __slots__ = ('r1', 'c1', 'r2', 'c2')

    def __init__(self, r1, c1, r2, c2):
        self.r1, self.c1 = int(r1), int(c1)
        self.r2, self.c2 = int(r2), int(c2)

    @property
    def height(self):
        return self.r2 - self.r1 + 1

    @property
    def width(self):
        return self.c2 - self.c1 + 1

    @property
    def area(self):
        return self.height * self.width

    def contains(self, r, c):
        return self.r1 <= r <= self.r2 and self.c1 <= c <= self.c2

    def __repr__(self):
        return f"Region({self.r1},{self.c1},{self.r2},{self.c2})"

    def __eq__(self, other):
        return (isinstance(other, Region) and
                self.r1 == other.r1 and self.c1 == other.c1 and
                self.r2 == other.r2 and self.c2 == other.c2)

    def to_list(self):
        return [self.r1, self.c1, self.r2, self.c2]


# ============================================================
# Helpers
# ============================================================

def unwrap(val):
    """Convert Grid to list-of-lists. Pass through anything else."""
    if isinstance(val, Grid):
        return val.data
    return val


def wrap(val):
    """Wrap list-of-lists result back to Grid if it looks like one."""
    if isinstance(val, list) and val and isinstance(val[0], list):
        return Grid(val)
    return val


def is_grid(val):
    return isinstance(val, Grid)

def is_pos(val):
    return isinstance(val, Pos)

def is_dir(val):
    return isinstance(val, Dir)

def is_region(val):
    return isinstance(val, Region)

def is_color(val):
    return isinstance(val, int) and 0 <= val <= 9


# Standard directions
UP = Dir(-1, 0)
DOWN = Dir(1, 0)
LEFT = Dir(0, -1)
RIGHT = Dir(0, 1)
DIRS_4 = [UP, DOWN, LEFT, RIGHT]
DIRS_8 = [Dir(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
DIRS_DIAG = [Dir(-1, -1), Dir(-1, 1), Dir(1, -1), Dir(1, 1)]
