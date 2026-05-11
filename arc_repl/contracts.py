"""
Contract system — type checking and validation for REPL builtins.

Every primitive has a contract that defines:
  - Expected parameter types
  - Validation checks (bounds, range, size matching)
  - Return type
  - Error messages

Contracts are enforced at call time. Clear error messages name
the builtin and describe what went wrong.
"""

from .types import Grid, Pos, Dir, Region, unwrap


class ContractError(Exception):
    """Base class for contract violations."""
    pass


class TypeErr(ContractError):
    """Wrong argument type."""
    pass


class SizeErr(ContractError):
    """Grid size mismatch."""
    pass


class RangeErr(ContractError):
    """Value out of valid range."""
    pass


class BoundsErr(ContractError):
    """Position out of grid bounds."""
    pass


# ============================================================
# Validators — call these in builtins before operating
# ============================================================

def check_grid(val, name=""):
    """Ensure val is a Grid. Coerce list-of-lists."""
    if isinstance(val, Grid):
        return val
    if isinstance(val, list) and val and isinstance(val[0], list):
        return Grid(val)
    raise TypeErr(f"{name}: expected Grid, got {type(val).__name__}")


def check_color(val, name=""):
    """Ensure val is int 0-9."""
    if isinstance(val, int) and 0 <= val <= 9:
        return val
    raise RangeErr(f"{name}: color must be int 0-9, got {val}")


def check_bounds(grid, r, c, name=""):
    """Ensure (r, c) is within grid."""
    if hasattr(grid, 'height'):
        h, w = grid.height, grid.width
    else:
        h = len(grid)
        w = len(grid[0]) if grid else 0
    if not (0 <= r < h and 0 <= c < w):
        raise BoundsErr(f"{name}: ({r},{c}) out of bounds for {h}x{w}")


def check_same_size(a, b, name=""):
    """Ensure two grids have matching dimensions."""
    ga, gb = unwrap(a), unwrap(b)
    ha, wa = len(ga), len(ga[0]) if ga else 0
    hb, wb = len(gb), len(gb[0]) if gb else 0
    if ha != hb or wa != wb:
        raise SizeErr(f"{name}: size mismatch ({ha}x{wa}) vs ({hb}x{wb}) — use broadcast")


def check_mask(val, name=""):
    """Ensure val is a valid mask (all values 0 or 1)."""
    g = unwrap(val) if isinstance(val, Grid) else val
    for row in g:
        for v in row:
            if v not in (0, 1):
                raise TypeErr(f"{name}: mask must contain only 0 and 1, found {v}")
    return val


def clamp_color(val):
    """Clamp an int to [0, 9]."""
    return max(0, min(9, int(val)))
