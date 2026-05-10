"""Generator for arc_additional_puzzle_bank_volume18:E124.

Magenta cells are reflected across a full orange divider as cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_magenta, magenta_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "329f699c3e09"
VERSION = "1.1.0"
TASK_ID = "329f699c3e09"
SUMMARY = "Magenta cells are reflected across a full orange divider as cyan."

INVARIANTS = [
    "background is 0",
    "there is a full orange divider row or column",
    "magenta source cells lie on one side of the divider",
    "reflected cells remain in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_magenta", "magenta_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 5..9", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "magenta_one_side_of_orange_divider",
                       "valid": "magenta_one_side_of_orange_divider"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_cells = ctx.draw_int("n_cells", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_cells = ctx.draw_int("n_cells", 7, 9)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
        n_cells = ctx.draw_int("n_cells", 5, 9)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: set[tuple[int, int]] = set()
    if rng.choice([False, True]):
        div = rng.randint(3, w - 4)
        left_cols = list(range(max(0, 2 * div - (w - 1)), div))
        for r in range(h):
            g[r][div] = 7
        for _ in range(200):
            if len(cells) >= n_cells:
                break
            cells.add((rng.randint(0, h - 1), rng.choice(left_cols)))
    else:
        div = rng.randint(3, h - 4)
        top_rows = list(range(max(0, 2 * div - (h - 1)), div))
        for c in range(w):
            g[div][c] = 7
        for _ in range(200):
            if len(cells) >= n_cells:
                break
            cells.add((rng.choice(top_rows), rng.randint(0, w - 1)))
    for r, c in cells:
        g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # magenta cells but no orange divider → no axis to reflect across
        g[2][2] = 6; g[3][3] = 6; g[5][7] = 6
        return g
    if name == "no_magenta":
        # divider but no magenta → no source cells to reflect
        for r in range(h):
            g[r][5] = 7
        return g
    if name == "magenta_on_divider":
        # magenta cells lie on the divider line itself → reflection is identity
        for r in range(h):
            g[r][5] = 7
        g[2][5] = 6; g[5][5] = 6
        return g
    return g
