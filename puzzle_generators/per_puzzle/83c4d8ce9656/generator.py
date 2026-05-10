"""Generator for arc_puzzle_bank_21_set5_e:easy_e05.

Keep only the endpoints of each horizontal nonzero run.

Combinatorial axes (8): grid_h, grid_w, palette_kind, runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, length_2_runs, vertical_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "83c4d8ce9656"
VERSION = "1.1.0"
TASK_ID = "83c4d8ce9656"

SUMMARY = "Keep only the endpoints of each horizontal nonzero run."

INVARIANTS = [
    "background is 0",
    "active rows contain same-color horizontal runs",
    "runs are separated by at least one zero",
    "runs of length at least three show the endpoint-erasing behavior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "length_2_runs", "vertical_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "runs":           {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "horizontal_runs",
                       "valid": "horizontal_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("runs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("runs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("runs", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        run_len = rng.randint(2, min(5, w))
        r = rng.randrange(h)
        c = rng.randint(0, w - run_len)
        if any(g[r][cc] != 0 for cc in range(max(0, c - 1), min(w, c + run_len + 1))):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for cc in range(c, c + run_len):
            g[r][cc] = color
        placed += 1
    if not any(
        c + 2 < w and g[r][c] != 0 and g[r][c] == g[r][c + 1] == g[r][c + 2]
        for r in range(h)
        for c in range(w - 2)
    ):
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[h // 2][1:4] = [color, color, color]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no horizontal runs to erase interiors of
        return g
    if name == "length_2_runs":
        # length-2 runs → all cells are endpoints, rule is identity
        for c in range(2, 4): g[1][c] = 4
        for c in range(5, 7): g[3][c] = 6
        return g
    if name == "vertical_only":
        # vertical runs only → "horizontal" precondition fails
        for r in range(1, 5): g[r][2] = 4
        return g
    return g
