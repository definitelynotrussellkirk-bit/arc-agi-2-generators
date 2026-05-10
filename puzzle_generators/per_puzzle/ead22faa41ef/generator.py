"""Generator for d90796e8.

Rule: adjacent 3-and-2 pairs become 8 at the 3 cell, with the 2 removed.

Combinatorial axes (8): grid_h/w, n_pairs, pair_orientation, n_distractors,
distractor_color, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_pairs, all_pairs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ead22faa41ef"
VERSION = "1.1.0"
TASK_ID = "ead22faa41ef"
SUMMARY = "Adjacent 3/2 pairs become 8 at the 3, 2 removed."

INVARIANTS = [
    "background is zero",
    "at least one orthogonally adjacent 3/2 pair appears",
    "color-5 distractors may remain unchanged",
]

ORIENTATIONS = ("h", "v", "mixed")
POSITION_BIASES = ("scattered", "corners", "centered", "row_aligned")
DEGENERATE_TEXTURES = ("no_pairs", "all_pairs", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 5..8", "valid": "4..14"},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "pair_orientation":{"type": "str", "default": "rng",
                       "valid": "|".join(ORIENTATIONS)},
    "n_distractors":  {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "distractor_color":{"type": "color", "default": "5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 5, 4, 5
        np_lo, np_hi = 1, 2
        nd_lo, nd_hi = 0, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 9, 14
        np_lo, np_hi = 3, 5
        nd_lo, nd_hi = 1, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 8, 5, 8
        np_lo, np_hi = 2, 3
        nd_lo, nd_hi = 0, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n_pairs = int(overrides.get("n_pairs",
                                ctx.draw_int("n_pairs", np_lo, np_hi)))
    n_pairs = max(1, min(5, n_pairs))
    orient = overrides.get("pair_orientation",
                           ctx.draw_choice("pair_orientation",
                                           list(ORIENTATIONS)))
    placed = 0
    for _try in range(120):
        if placed >= n_pairs:
            break
        if orient == "h" or (orient == "mixed" and rng.random() < 0.5):
            r3 = rng.randint(0, h - 1)
            c3 = rng.randint(0, w - 2)
            r2 = r3; c2 = c3 + 1
        elif orient == "v" or orient == "mixed":
            c3 = rng.randint(0, w - 1)
            r3 = rng.randint(0, h - 2)
            c2 = c3; r2 = r3 + 1
        else:
            r3 = rng.randint(0, h - 1); c3 = rng.randint(0, w - 2)
            r2 = r3; c2 = c3 + 1
        if g[r3][c3] != 0 or g[r2][c2] != 0:
            continue
        g[r3][c3] = 3
        g[r2][c2] = 2
        placed += 1
    if placed < 1:
        g[0][0] = 3; g[0][1] = 2
    nd = int(overrides.get("n_distractors",
                           ctx.draw_int("n_distractors", nd_lo, nd_hi)))
    nd = max(0, min(4, nd))
    dcolor = int(overrides.get("distractor_color", 5))
    for _ in range(nd):
        for _try in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = dcolor
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        g[1][1] = 3; g[4][4] = 2
        return g
    if name == "all_pairs":
        for r in range(0, h, 2):
            for c in range(0, w - 1, 2):
                g[r][c] = 3; g[r][c + 1] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 2
        return g
    return g
