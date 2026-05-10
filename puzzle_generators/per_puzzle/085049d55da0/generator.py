"""Generator for arc_additional_puzzles_21_set11_bundle:H76 — chamber ownership fill.

Rule: color 9 is impassable wall. For each 4-connected open region (non-9
cells), if it contains exactly one distinct non-zero marker color, fill
all 0-cells in that region with that color. Walls and other markers
unchanged.

Combinatorial axes (8): ch_h, ch_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, empty_chamber, multiple_markers_same_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "085049d55da0"
VERSION = "1.1.0"
TASK_ID = "085049d55da0"

SUMMARY = "9-walls form 2x2 chambers; each chamber holds exactly one marker color."

INVARIANTS = [
    "background is 0",
    "9-walls form a 2x2 chamber layout (outer frame + 1 horizontal + 1 vertical divider)",
    "each chamber has exactly one isolated marker cell (non-{0, 9})",
    "marker colors are sampled from {1..8}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "empty_chamber", "multiple_markers_same_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "ch_w":           {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "4", "valid": "4..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "2x2_chamber_grid",
                       "valid": "2x2_chamber_grid"},
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
        ch = ctx.draw_int("ch_h", 3, 3)
        cw = ctx.draw_int("ch_w", 3, 3)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 4, 4)
        cw = ctx.draw_int("ch_w", 4, 4)
    else:
        ch = ctx.draw_int("ch_h", 3, 4)
        cw = ctx.draw_int("ch_w", 3, 4)
    rng = ctx.draw_rng("layout")
    h = 2 * ch + 3
    w = 2 * cw + 3

    g = full_grid(h, w, 0)
    # outer frame + horizontal divider at row ch+1 + vertical divider at col cw+1
    for c in range(w):
        g[0][c] = 9
        g[ch + 1][c] = 9
        g[h - 1][c] = 9
    for r in range(h):
        g[r][0] = 9
        g[r][cw + 1] = 9
        g[r][w - 1] = 9
    chambers = [(1, 1), (1, cw + 2), (ch + 2, 1), (ch + 2, cw + 2)]
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 4)
    for (rr, cc), color in zip(chambers, colors):
        cells = [(r, c) for r in range(rr, rr + ch) for c in range(cc, cc + cw)]
        r, c = rng.choice(cells)
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 3, 3
    h, w = 2 * ch + 3, 2 * cw + 3
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # markers but no 9-walls → single open region, all markers compete
        g[2][2] = 4; g[2][6] = 6; g[6][2] = 7; g[6][6] = 8
        return g
    if name == "empty_chamber":
        # one chamber has no marker → no fill color defined for that region
        for c in range(w): g[0][c] = 9; g[ch + 1][c] = 9; g[h - 1][c] = 9
        for r in range(h): g[r][0] = 9; g[r][cw + 1] = 9; g[r][w - 1] = 9
        # only fill 3 of 4 chambers
        g[2][2] = 4
        g[2][6] = 6
        g[6][2] = 7
        return g
    if name == "multiple_markers_same_chamber":
        # one chamber has 2 distinct markers → ambiguous fill color
        for c in range(w): g[0][c] = 9; g[ch + 1][c] = 9; g[h - 1][c] = 9
        for r in range(h): g[r][0] = 9; g[r][cw + 1] = 9; g[r][w - 1] = 9
        g[1][1] = 4; g[3][3] = 6  # both in chamber (1,1)
        g[2][6] = 7
        g[6][2] = 8
        return g
    return g
