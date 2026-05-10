"""Generator for arc_additional_puzzles_21_set7:M43 — Crop to bbox of selector-color cells (excluding (0,0)).

Rule: selector = value at (0,0). Find all cells of the selector color
EXCEPT (0,0). Crop the grid to that bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, selector,
n_target, n_distract, palette_size, position_bias, n_distinct_colors,
density, texture.
Degenerates: no_target_in_body, target_at_corners, only_target_in_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d03b34a04be3"
VERSION = "1.1.0"
TASK_ID = "d03b34a04be3"
SUMMARY = "Selector cell at (0,0) sets target color; crop to bbox of that color elsewhere."

INVARIANTS = [
    "selector at (0,0) is non-zero",
    "between 3 and 7 cells of selector color in rows 1+ or cols 1+",
    "1..2 distractor cells of other non-selector non-zero colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target_in_body", "target_at_corners", "only_target_in_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selector":       {"type": "color", "default": "rng", "valid": "1..9"},
    "n_target":       {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "n_distract":     {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "selector_corner_with_target_body",
                       "valid": "selector_corner_with_target_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        n_target = ctx.draw_int("n_target", 3, 4)
        n_distract = ctx.draw_int("n_distract", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
        n_target = ctx.draw_int("n_target", 6, 7)
        n_distract = ctx.draw_int("n_distract", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 14)
        n_target = ctx.draw_int("n_target", 4, 7)
        n_distract = ctx.draw_int("n_distract", 1, 2)
    selector = ctx.draw_color("selector")

    g = full_grid(h, w, 0)
    g[0][0] = selector
    rng = ctx.draw_rng("placement")

    placed = 0
    while placed < n_target:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) == (0, 0): continue
        if g[r][c] != 0: continue
        g[r][c] = selector
        placed += 1

    distract_colors = [c for c in range(1, 10) if c != selector]
    rng.shuffle(distract_colors)
    for i in range(n_distract):
        if i >= len(distract_colors): break
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if (r, c) == (0, 0): continue
            if g[r][c] != 0: continue
            g[r][c] = distract_colors[i]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    g[0][0] = 4   # selector
    if name == "no_target_in_body":
        # selector at (0,0) but no matching cells elsewhere → bbox is empty
        g[3][2] = 6; g[5][7] = 8; g[6][3] = 3
        return g
    if name == "target_at_corners":
        # target cells at all four corners → bbox spans almost the whole grid; crop is trivial
        g[0][w - 1] = 4
        g[h - 1][0] = 4
        g[h - 1][w - 1] = 4
        return g
    if name == "only_target_in_body":
        # body filled densely with the selector color → bbox is huge, crop nearly identity
        for r in range(1, h):
            for c in range(0, w, 2):
                g[r][c] = 4
        return g
    return g
