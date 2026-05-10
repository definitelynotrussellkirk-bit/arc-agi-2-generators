"""Generator for puzzle 93b581b8.

Rule: 2x2 block. Stamp each cell diagonally outward to opposite-far
2x2 corner.

Combinatorial axes (8): grid_h/w, block_position, palette_kind,
palette_size, anchor_corner, asymmetry_force, include_decoy,
margin_size.
Degenerates: too_close_to_edge, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf8910eef99b"
VERSION = "1.1.0"
TASK_ID = "bf8910eef99b"
SUMMARY = "2x2 block; rule stamps each cell to far corner."

INVARIANTS = [
    "background is 0",
    "exactly 4 non-zero cells forming solid 2x2 block",
    "block uses 4 distinct colors",
    ">=2 cells of room around block to all sides",
]

POSITION_BIASES = ("centered", "upper_left", "upper_right", "lower_left",
                   "lower_right", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("too_close_to_edge", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "block_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..4"},
    "margin_size":    {"type": "int", "default": "2", "valid": "1..3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for block_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pos = (overrides.get("texture") or
           overrides.get("block_position")
           or ctx.draw_choice("block_position",
                              list(POSITION_BIASES)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size", 4))
    palette_size = max(2, min(4, palette_size))
    palette = _build_palette(palette_kind, palette_size, rng)
    margin = int(overrides.get("margin_size", 2))
    margin = max(1, min(3, margin))
    g = full_grid(h, w, 0)
    if pos == "centered":
        br = h // 2 - 1; bc = w // 2 - 1
    elif pos == "upper_left":
        br = margin; bc = margin
    elif pos == "upper_right":
        br = margin; bc = w - 2 - margin
    elif pos == "lower_left":
        br = h - 2 - margin; bc = margin
    elif pos == "lower_right":
        br = h - 2 - margin; bc = w - 2 - margin
    else:
        br = rng.randint(margin, max(margin, h - 2 - margin))
        bc = rng.randint(margin, max(margin, w - 2 - margin))
    br = max(0, min(h - 2, br))
    bc = max(0, min(w - 2, bc))
    # 4 cells, possibly fewer distinct colors
    if palette_size >= 4:
        g[br][bc] = palette[0]
        g[br][bc + 1] = palette[1]
        g[br + 1][bc] = palette[2]
        g[br + 1][bc + 1] = palette[3]
    else:
        cells = [palette[i % palette_size] for i in range(4)]
        rng.shuffle(cells)
        g[br][bc] = cells[0]
        g[br][bc + 1] = cells[1]
        g[br + 1][bc] = cells[2]
        g[br + 1][bc + 1] = cells[3]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "too_close_to_edge":
        g[0][0] = 1; g[0][1] = 2; g[1][0] = 3; g[1][1] = 4
        return g
    if name == "single_color":
        c = 3
        g[h // 2 - 1][w // 2 - 1] = c
        g[h // 2 - 1][w // 2] = c
        g[h // 2][w // 2 - 1] = c
        g[h // 2][w // 2] = c
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 9 + 1
        return g
    return g
