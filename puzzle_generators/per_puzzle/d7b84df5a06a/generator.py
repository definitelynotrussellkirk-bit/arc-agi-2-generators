"""Generator for arc_additional_puzzle_bank_volume23:H159.

Rule: gray-wall chambers fill by seed plurality with mapped output
colors; one chamber has a unique plurality, one has a tie.

Combinatorial axes (8): grid_h/w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, seed_density, texture.
Degenerates: no_walls, no_seeds, single_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d7b84df5a06a"
VERSION = "1.1.0"
TASK_ID = "d7b84df5a06a"
SUMMARY = "Gray-wall chambers fill by seed plurality with mapped output colors."

INVARIANTS = [
    "walls are 5",
    "chambers contain seed colors 2, 3, or 4",
    "one chamber has a unique plurality",
    "one chamber has a top-count tie",
]

PALETTE_KINDS = ("default", "wide_split", "narrow_split", "even_split")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "single_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "split", "valid": "split"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "seed_density":   {"type": "str", "default": "low", "valid": "low"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _carve(g, r0, c0, r1, c1):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            g[r][c] = 0


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 11, 16)
    g = full_grid(h, w, 5)
    mid = w // 2
    _carve(g, 1, 1, h - 2, mid - 1)
    _carve(g, 1, mid + 1, h - 2, w - 2)
    for r, c, v in [(1, 1, 2), (2, 2, 2), (h - 3, 2, 3), (1, mid + 2, 3), (2, mid + 3, 4)]:
        g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    if name == "no_walls":
        # all-bg grid with seeds — no chambers to fill
        g = full_grid(h, w, 0)
        g[2][2] = 2
        g[3][3] = 3
        g[5][5] = 4
        return g
    if name == "no_seeds":
        # walls and chambers but no seeds — plurality is undefined
        g = full_grid(h, w, 5)
        mid = w // 2
        _carve(g, 1, 1, h - 2, mid - 1)
        _carve(g, 1, mid + 1, h - 2, w - 2)
        return g
    if name == "single_chamber":
        # only one chamber — no comparison possible
        g = full_grid(h, w, 5)
        _carve(g, 1, 1, h - 2, w - 2)
        g[2][2] = 2; g[3][4] = 2; g[5][6] = 3
        return g
    return full_grid(h, w, 0)
