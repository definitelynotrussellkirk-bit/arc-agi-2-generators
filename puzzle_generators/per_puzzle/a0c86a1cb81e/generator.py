"""Generator for arc_additional_puzzle_bank_volume5:E33.

Green path elbow cells are recolored magenta.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_elbows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_elbows, straight_line, length_4_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a0c86a1cb81e"
VERSION = "1.1.0"
TASK_ID = "a0c86a1cb81e"
SUMMARY = "Green path elbow cells are recolored magenta."

INVARIANTS = [
    "background is 0",
    "green target components are small L-shaped paths",
    "the bend cell has one horizontal and one vertical green neighbor",
    "path components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_elbows", "straight_line", "length_4_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_elbows":       {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_l_paths",
                       "valid": "separated_l_paths"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_elbows = ctx.draw_int("n_elbows", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_elbows = ctx.draw_int("n_elbows", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_elbows = ctx.draw_int("n_elbows", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    shapes = [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    anchors: list[tuple[int, int]] = []
    for _ in range(220):
        if len(anchors) >= n_elbows:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in anchors):
            continue
        for dr, dc in rng.choice(shapes):
            g[r + dr][c + dc] = 3
        anchors.append((r, c))
    if not anchors:
        g[1][1] = 3
        g[2][1] = 3
        g[2][2] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_elbows":
        # blank → no L-paths to recolor at the bend
        return g
    if name == "straight_line":
        # 3-cell straight line → no bend cell, rule won't fire
        for c in range(2, 5): g[3][c] = 3
        return g
    if name == "length_4_path":
        # 4-cell L → multiple bend candidates, ambiguous
        for r, c in [(1, 1), (2, 1), (2, 2), (2, 3)]: g[r][c] = 3
        return g
    return g
