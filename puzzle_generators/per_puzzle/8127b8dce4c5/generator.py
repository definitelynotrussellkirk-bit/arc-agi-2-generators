"""Generator for puzzle 27a28665.

Rule: 3x3 input. Count non-zero corner cells.
- 0 corners non-zero → output 6
- 4 corners non-zero → output 2
- has 2x2 sub-block all non-zero → output 3
- otherwise → output 1

Combinatorial axes (8): n_cells, color, corner_pattern, has_2x2,
center_filled, anchor_corner, asymmetry_force, palette_kind.
Degenerates: empty_grid, full_grid, single_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8127b8dce4c5"
VERSION = "1.1.0"
TASK_ID = "8127b8dce4c5"
SUMMARY = "3x3 grid with non-zero cells; rule outputs 1-cell by pattern."

INVARIANTS = [
    "h = w = 3",
    "1+ non-zero cells (so rule has input)",
]

CORNER_PATTERNS = ("zero_corners", "all_corners", "two_corners",
                   "diagonal_corners", "anti_diag_corners")
PALETTE_KINDS = ("warm", "cool", "broad")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "single_corner")
HELPFUL_TEXTURES = CORNER_PATTERNS

AXES = {
    "n_cells":        {"type": "int", "default": "rng 2..7", "valid": "1..9"},
    "color":          {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "corner_pattern": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CORNER_PATTERNS)},
    "has_2x2":        {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "center_filled":  {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for corner_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", palette[0]))
    if color == 0:
        color = palette[0] if palette[0] != 0 else 1
    pattern = (overrides.get("texture") or
               overrides.get("corner_pattern")
               or ctx.draw_choice("corner_pattern",
                                  list(CORNER_PATTERNS)))
    has_2x2 = bool(overrides.get("has_2x2", False))
    g = full_grid(3, 3, 0)
    _apply_corner_pattern(g, pattern, color, rng)
    if has_2x2:
        for dr in range(2):
            for dc in range(2):
                g[dr][dc] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _apply_corner_pattern(g, pattern, color, rng):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    if pattern == "zero_corners":
        # Fill non-corners only
        non_corners = [(r, c) for r in range(3) for c in range(3)
                       if (r, c) not in corners]
        rng.shuffle(non_corners)
        for r, c in non_corners[:rng.randint(1, 3)]:
            g[r][c] = color
    elif pattern == "all_corners":
        for r, c in corners:
            g[r][c] = color
    elif pattern == "two_corners":
        for r, c in rng.sample(corners, 2):
            g[r][c] = color
        # Optional: a few non-corner cells
        non_corners = [(r, c) for r in range(3) for c in range(3)
                       if (r, c) not in corners]
        rng.shuffle(non_corners)
        for r, c in non_corners[:rng.randint(0, 2)]:
            g[r][c] = color
    elif pattern == "diagonal_corners":
        for r, c in [(0, 0), (2, 2)]:
            g[r][c] = color
    elif pattern == "anti_diag_corners":
        for r, c in [(0, 2), (2, 0)]:
            g[r][c] = color
    else:
        n = rng.randint(2, 6)
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
        for r, c in cells[:n]:
            g[r][c] = color


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 3, 0)
    if name == "empty_grid":
        return g
    if name == "full_grid":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(3):
            for cc in range(3):
                g[r][cc] = c
        return g
    if name == "single_corner":
        g[0][0] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
