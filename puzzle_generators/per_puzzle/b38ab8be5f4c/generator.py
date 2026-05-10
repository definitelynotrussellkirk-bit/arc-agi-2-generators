"""Generator for arc_additional_puzzles_21_set11_bundle:M72 — Crop to bbox of color matching row-0 guide.

Rule: guide = first non-zero value in row 0. Find all cells (r >= 1)
with value == guide. Bbox of those cells. Output = crop to that bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_guide,
n_distract, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide, no_guide_in_body, only_guide_in_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b38ab8be5f4c"
VERSION = "1.1.0"
TASK_ID = "b38ab8be5f4c"
SUMMARY = "Single guide cell in row 0; cells of guide color elsewhere; output crops their bbox."

INVARIANTS = [
    "exactly one non-zero cell in row 0 (the guide)",
    "between 3 and 8 cells of guide color in rows 1+",
    "1..2 distractor cells of other non-guide non-zero colors in rows 1+",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_guide_in_body", "only_guide_in_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "guide":          {"type": "color", "default": "rng", "valid": "1..9"},
    "n_guide":        {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "n_distract":     {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "guide_in_row0_body_below",
                       "valid": "guide_in_row0_body_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_guide = ctx.draw_int("n_guide", 3, 4)
        n_distract = ctx.draw_int("n_distract", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n_guide = ctx.draw_int("n_guide", 6, 7)
        n_distract = ctx.draw_int("n_distract", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        n_guide = ctx.draw_int("n_guide", 4, 7)
        n_distract = ctx.draw_int("n_distract", 1, 2)
    guide = ctx.draw_color("guide")

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][rng.randint(0, w - 1)] = guide
    placed = 0
    while placed < n_guide:
        r = rng.randint(1, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = guide
            placed += 1

    distract_colors = [c for c in range(1, 10) if c != guide]
    rng.shuffle(distract_colors)
    for i in range(n_distract):
        if i >= len(distract_colors): break
        for _ in range(20):
            r = rng.randint(1, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = distract_colors[i]
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # no guide in row 0 → "first nonzero in row 0" is undefined
        g[3][2] = 4; g[5][6] = 4; g[6][3] = 4
        g[2][8] = 6; g[7][1] = 8
        return g
    if name == "no_guide_in_body":
        # guide present in row 0 but no matching cells below → bbox is empty
        g[0][3] = 4   # guide
        g[3][2] = 6; g[5][7] = 8; g[6][1] = 3
        return g
    if name == "only_guide_in_body":
        # guide cells fill the entire body uniformly → bbox is the whole grid
        g[0][3] = 4
        for r in range(1, h):
            for c in range(0, w, 2):
                g[r][c] = 4
        return g
    return g
