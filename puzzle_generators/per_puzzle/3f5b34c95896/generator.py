"""Generator for 5ad4f10b.

Rule: a blocky shape's bbox is downscaled to a 3x3 mask using a separate
dot color for occupied blocks.

Combinatorial axes (8): block_size, n_occupied, palette_kind, dot_pos,
shape_pattern, anchor_corner, asymmetry_force, palette_size.
Degenerates: empty_shape, full_shape, no_dot.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f5b34c95896"
VERSION = "1.1.0"
TASK_ID = "3f5b34c95896"
SUMMARY = "Blocky shape bbox downscaled to 3x3 mask using separate dot color."

INVARIANTS = [
    "background is color 0",
    "the largest object has one shape color and a bbox divisible into a 3x3 block grid",
    "a smaller non-shape-color dot supplies the output color",
    "each output cell is the dot color iff the corresponding source block contains shape-color cells",
]

PATTERNS = ("L_shape", "T_shape", "diagonal", "scattered", "checker")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_shape", "full_shape", "no_dot")
HELPFUL_TEXTURES = PATTERNS

AXES = {
    "block_size":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "n_occupied":     {"type": "int", "default": "rng 4..6", "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "dot_pos":        {"type": "str", "default": "rng",
                       "valid": "tl|tr|bl|br|center"},
    "shape_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATTERNS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for shape_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        block_lo, block_hi = 1, 2
        no_lo, no_hi = 4, 5
    elif difficulty == "hard":
        block_lo, block_hi = 4, 6
        no_lo, no_hi = 3, 8
    else:
        block_lo, block_hi = 2, 4
        no_lo, no_hi = 4, 6
    block = int(overrides.get("block_size",
                              ctx.draw_int("block_size", block_lo, block_hi)))
    block = max(1, min(6, block))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    if len(pal) < 2:
        pal = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        rng.shuffle(pal)
    shape_color, dot_color = pal[0], pal[1]
    pattern = (overrides.get("texture") or
               overrides.get("shape_pattern")
               or ctx.draw_choice("shape_pattern", list(PATTERNS)))
    occupied = _make_occupied(pattern, no_lo, no_hi, rng)
    h = 3 * block + 6
    w = 3 * block + 6
    g = full_grid(h, w, 0)
    r0 = c0 = 2
    for br, bc in occupied:
        for r in range(block):
            for c in range(block):
                g[r0 + br * block + r][c0 + bc * block + c] = shape_color
    dot_pos = overrides.get("dot_pos",
                            ctx.draw_choice("dot_pos",
                                            ["tl", "tr", "bl", "br", "center"]))
    if dot_pos == "tl":
        g[1][1] = dot_color
    elif dot_pos == "tr":
        g[1][w - 2] = dot_color
    elif dot_pos == "bl":
        g[h - 2][1] = dot_color
    elif dot_pos == "center":
        g[h // 2][w - 2] = dot_color
    else:
        g[h - 2][w - 2] = dot_color
    return g


def _make_occupied(pattern, no_lo, no_hi, rng):
    if pattern == "L_shape":
        cells = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    elif pattern == "T_shape":
        cells = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
    elif pattern == "diagonal":
        cells = [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0)]
    elif pattern == "checker":
        cells = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
    else:
        cells = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 1)]
    rng.shuffle(cells)
    n = rng.randint(no_lo, min(no_hi, len(cells)))
    return cells[:n]


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "empty_shape":
        g[h - 2][w - 2] = 4
        return g
    if name == "full_shape":
        for r in range(2, 8):
            for c in range(2, 8):
                g[r][c] = 2
        g[h - 2][w - 2] = 4
        return g
    if name == "no_dot":
        for r in range(2, 8):
            for c in range(2, 8):
                if rng.random() < 0.5:
                    g[r][c] = 2
        return g
    return g
