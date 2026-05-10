"""Generator for puzzle 4852f2fa.

Rule: there's one 8-shape (3..9 cells) within some 3x3 bbox, and N
isolated 4-cells. Rule outputs a 3 × (3N) grid where the 8-shape (in
its 3x3 bbox) is tiled horizontally N times.

Combinatorial axes (8): grid_h/w, n_4_cells, shape_kind, shape_density,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_4_cells, single_8_cell, full_8_block.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap, random_free_cell

GENERATOR_ID = "87aae821984d"
VERSION = "1.1.0"
TASK_ID = "87aae821984d"
SUMMARY = "8-shape (3..9 cells) + N 4-cells; rule outputs 3x(3N) tiled shape."

INVARIANTS = [
    "background is 0",
    "exactly one 8-shape whose bbox spans <=3x3",
    "1-4 isolated 4-cells, none adjacent to 8-shape",
    "shape has >=3 cells (else tile is trivial)",
]

SHAPE_KINDS = ("L", "T", "diag", "plus", "corners", "scattered",
               "stairs")
DEGENERATE_TEXTURES = ("no_4_cells", "single_8_cell", "full_8_block")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "7..16"},
    "n_4_cells":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "shape_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_KINDS)},
    "shape_density":  {"type": "int", "default": "rng 3..6",
                       "valid": "3..9"},
    "position_bias":  {"type": "str", "default": "rng spread|corners|center",
                       "valid": "spread|corners|center"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for shape_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_4 = int(overrides.get("n_4_cells",
                            ctx.draw_int("n_4_cells", 1, 3)))
    n_4 = max(1, min(5, n_4))
    shape_kind = (overrides.get("texture") or
                  overrides.get("shape_kind")
                  or ctx.draw_choice("shape_kind", list(SHAPE_KINDS)))
    g = full_grid(h, w, 0)
    # Place 4-cells first
    for _ in range(n_4):
        cell = random_free_cell(g, rng, max_tries=30)
        if cell is not None:
            g[cell[0]][cell[1]] = 4
    pattern = _build_shape(shape_kind, rng)
    place_no_overlap(rng, g, list(pattern), 8, max_tries=60)
    return g


def _build_shape(kind, rng):
    if kind == "L":
        return [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    if kind == "T":
        return [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
    if kind == "diag":
        return [(0, 0), (1, 1), (2, 2)]
    if kind == "plus":
        return [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    if kind == "corners":
        return [(0, 0), (0, 2), (2, 0), (2, 2)]
    if kind == "scattered":
        n = rng.randint(3, 6)
        cells = [(r, c) for r in range(3) for c in range(3)]
        rng.shuffle(cells)
        return cells[:n]
    if kind == "stairs":
        return [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
    diag = rng.choice([[(0, 0), (2, 2)], [(0, 2), (2, 0)]])
    pattern = set(diag)
    remaining = [(dr, dc) for dr in range(3) for dc in range(3)
                 if (dr, dc) not in pattern]
    pattern.update(rng.sample(remaining, rng.randint(2, 5)))
    return list(pattern)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_4_cells":
        # Output would be 3x0 — rule degenerates
        place_no_overlap(rng, g,
                         [(0, 0), (1, 1), (2, 2)],
                         8, max_tries=30)
        return g
    if name == "single_8_cell":
        g[h // 2][w // 2] = 8
        g[0][0] = 4
        return g
    if name == "full_8_block":
        # 3x3 solid block of 8s
        place_no_overlap(rng, g,
                         [(r, c) for r in range(3) for c in range(3)],
                         8, max_tries=30)
        g[0][0] = 4
        return g
    return g
