"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_47_keep_most_frequent_color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, winner_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: monochrome, tied_winners, no_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "45f08b9a5f47"
VERSION = "1.1.0"
TASK_ID = "45f08b9a5f47"

SUMMARY = "The unique most frequent nonzero color is kept and all others are cleared."

INVARIANTS = [
    "background is 0",
    "there are at least three nonzero colors",
    "one nonzero color has a strictly largest frequency",
    "distractor colors appear fewer times",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("monochrome", "tied_winners", "no_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "winner_cells":   {"type": "int", "default": "rng 9..16", "valid": "3..60"},
    "distractor_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "winner_plus_distractors",
                       "valid": "winner_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        winner_n = min(ctx.draw_int("winner_cells", 9, 12), h * w // 2)
        distractor_k = min(ctx.draw_int("distractor_colors", 2, 2), 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        winner_n = min(ctx.draw_int("winner_cells", 12, 16), h * w // 2)
        distractor_k = min(ctx.draw_int("distractor_colors", 3, 4), 8)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        winner_n = min(ctx.draw_int("winner_cells", 9, 16), h * w // 2)
        distractor_k = min(ctx.draw_int("distractor_colors", 2, 4), 8)
    rng = ctx.draw_rng("layout")
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(palette)
    winner = palette[0]
    distractors = palette[1:1 + distractor_k]
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    cursor = 0
    for r, c in cells[cursor:cursor + winner_n]:
        g[r][c] = winner
    cursor += winner_n
    max_each = max(1, winner_n - 2)
    for color in distractors:
        n = rng.randint(1, min(max_each, max(1, winner_n // 2)))
        for r, c in cells[cursor:cursor + n]:
            g[r][c] = color
        cursor += n
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "monochrome":
        # only one nonzero color → "most frequent" is trivially that, rule is identity
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        return g
    if name == "tied_winners":
        # two colors with equal counts → no strictly-largest frequency, ambiguous
        for c in range(2, 5): g[2][c] = 4
        for c in range(2, 5): g[5][c] = 6
        return g
    if name == "no_distractors":
        # winner + 0 distractors → only one color present, rule is identity
        for c in range(2, 6): g[3][c] = 7
        return g
    return g
