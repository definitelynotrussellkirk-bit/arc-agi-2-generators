"""Generator for 14b:hard_97 — cast border rays and mark matching intersections.

Rule: row 0 holds column codes; col 0 holds row codes. For each
interior cell (r, c), if vc = (0, c) equals hc = (r, 0) (both non-bg,
non-5), and the vertical ray (0, c)→(r, c) and horizontal ray
(r, 0)→(r, c) are both clear of color-5, mark cell with vc.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_codes, no_left_codes, no_matching_codes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5f9e7472602"
VERSION = "1.1.0"
TASK_ID = "b5f9e7472602"

SUMMARY = "Top row + left col hold matching color codes; optional 5-walls in interior."

INVARIANTS = [
    "background is 0",
    "row 0 cols 1+ hold 2-3 non-{0,5} codes at distinct columns",
    "col 0 rows 1+ hold 2-3 non-{0,5} codes at distinct rows",
    "at least one (row, col) pair has matching codes (so output has at least one mark)",
    "0-2 interior 5-walls (single cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_codes", "no_left_codes", "no_matching_codes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "row0_col0_codes",
                       "valid": "row0_col0_codes"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    for outer in range(40):
        g = full_grid(h, w, 0)
        n_top = rng.randint(2, 3)
        n_left = rng.randint(2, 3)
        top_codes = [rng.choice(palette) for _ in range(n_top)]
        left_codes = [rng.choice(palette) for _ in range(n_left)]
        if not (set(top_codes) & set(left_codes)):
            continue
        top_cols = rng.sample(range(1, w), n_top)
        left_rows = rng.sample(range(1, h), n_left)
        for c, code in zip(top_cols, top_codes): g[0][c] = code
        for r, code in zip(left_rows, left_codes): g[r][0] = code
        match_found = False
        for c, vc in zip(top_cols, top_codes):
            for r, hc in zip(left_rows, left_codes):
                if vc == hc:
                    match_found = True; break
            if match_found: break
        if match_found:
            return g
    raise ValueError("could not realize matching codes in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_top_codes":
        # Left col codes but row 0 is empty — rule has no column codes
        # to compare against; intersection set is empty.
        g[2][0] = 4; g[5][0] = 6
        return g
    if name == "no_left_codes":
        # Row 0 codes but col 0 is empty — rule has no row codes; no
        # marks produced.
        g[0][2] = 4; g[0][5] = 6
        return g
    if name == "no_matching_codes":
        # Codes on both axes but no overlap — rule's match step finds
        # zero (row, col) pairs.
        g[0][2] = 4; g[0][5] = 6
        g[2][0] = 7; g[5][0] = 8
        return g
    return g
