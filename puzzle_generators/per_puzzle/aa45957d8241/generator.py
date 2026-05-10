"""Generator for arc_puzzle_bank_21_more:hard_b04 — Pack shapes by row-0 color order.

Rule: row 0 has color codes; below are non-zero shapes. Pack shapes
side-by-side in the order specified by row 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_codes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes, no_shapes, missing_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aa45957d8241"
VERSION = "1.1.0"
TASK_ID = "aa45957d8241"
SUMMARY = "Row 0 with 2-3 color codes (separated by 0s); below: 1 shape per code at unique positions."

INVARIANTS = [
    "row 0: 2-3 non-zero cells (the order)",
    "below row 0: one connected shape per color in row 0, well-separated",
    "each shape ≥3 cells and ≤6 cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_shapes", "missing_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_codes":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "= n_codes", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "codes_top_shapes_below",
                       "valid": "codes_top_shapes_below"},
    "n_distinct_colors": {"type": "int", "default": "= n_codes", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 18)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_codes = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_codes)
    code_cols = sorted(rng.sample(range(w), n_codes))
    for c, color in zip(code_cols, palette):
        g[0][c] = color
    placed = []
    for color in palette:
        shape = rng.choice(SHAPES)
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(2, h - sh - 1); c0 = rng.randint(0, w - sw - 1)
            if any(abs(r0 - pr) < (sh + 2) and abs(c0 - pc) < (sw + 2) for pr, pc in placed):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # Shapes below but row 0 is empty — rule has no order
        # specification, packing direction undefined.
        for dr, dc in SHAPES[0]:
            g[3 + dr][1 + dc] = 4
        for dr, dc in SHAPES[1]:
            g[3 + dr][6 + dc] = 6
        return g
    if name == "no_shapes":
        # Codes in row 0 but no shapes below — rule has nothing
        # to pack.
        g[0][2] = 4; g[0][6] = 6; g[0][9] = 7
        return g
    if name == "missing_shape":
        # Codes mention 3 colors but only 2 shapes drawn — one code
        # has no corresponding shape, rule's pack list is incomplete.
        g[0][2] = 4; g[0][6] = 6; g[0][9] = 7
        for dr, dc in SHAPES[0]:
            g[3 + dr][1 + dc] = 4
        for dr, dc in SHAPES[1]:
            g[3 + dr][6 + dc] = 6
        return g
    return g
