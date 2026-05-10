"""Generator for 11b:m77 — border rays until block.

Rule: each non-zero cell on the grid border emits a ray inward in the
cardinal direction perpendicular to its border. The ray paints itself
in the same color until hitting a non-zero cell or the opposite border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_emitters,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_blockers, all_emitters_one_side.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7a832ade60d"
VERSION = "1.1.0"
TASK_ID = "b7a832ade60d"
SUMMARY = "2-3 border emitters + 1-2 interior blocks (ray stoppers)."

INVARIANTS = [
    "background is 0",
    "≥2 distinct-color cells on the grid border (emitters)",
    "≥1 non-emitter cell in the interior (acts as ray-block)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_blockers", "all_emitters_one_side")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_emitters":     {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "border_emitters_plus_blocker",
                       "valid": "border_emitters_plus_blocker"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g[0][rng.randint(2, w - 3)] = palette[0]
    g[h - 1][rng.randint(2, w - 3)] = palette[1]
    g[rng.randint(2, h - 3)][0] = palette[2]
    for _ in range(40):
        r = rng.randint(2, h - 3)
        c = rng.randint(2, w - 3)
        if g[r][c] == 0:
            g[r][c] = palette[3]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # only an interior cell, no border emitters → no rays to draw
        g[3][4] = 4
        return g
    if name == "no_blockers":
        # border emitters with no interior block → rays cross the whole grid
        g[0][3] = 4
        g[h - 1][5] = 6
        g[3][0] = 7
        return g
    if name == "all_emitters_one_side":
        # all emitters on top edge → only downward rays, no contrast for direction
        g[0][2] = 4
        g[0][4] = 6
        g[0][6] = 7
        g[3][3] = 9  # blocker
        return g
    return g
