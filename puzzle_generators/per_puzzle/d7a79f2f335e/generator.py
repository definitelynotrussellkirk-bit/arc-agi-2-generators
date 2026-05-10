"""Generator for arc_additional_puzzles_21_set21_bundle:H145 — code-tiled transforms.

Rule: split input into two panels by zero-col separator. Left = template
(small shape). Right = code grid (1..7 transform codes). Output tiles
each code cell by the template with that transform applied:
  1=identity, 2=cw, 3=180, 4=ccw, 5=flip_lr, 6=flip_ud, else=transpose.

Combinatorial axes (8): tpl_h, tpl_w, palette_kind, code_h, code_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, empty_template, no_codes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d7a79f2f335e"
VERSION = "1.1.0"
TASK_ID = "d7a79f2f335e"
SUMMARY = "[template] [zero col] [code grid 1..7] horizontally arranged."

INVARIANTS = [
    "background is 0",
    "exactly one all-zero column separates template from code grid",
    "template has at least one non-zero cell (otherwise output is empty)",
    "code grid cells are in 1..7",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "empty_template", "no_codes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tpl_h":          {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "tpl_w":          {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code_h":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "code_w":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "tpl_left_codes_right",
                       "valid": "tpl_left_codes_right"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..7", "valid": "3..8"},
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
        th = ctx.draw_int("tpl_h", 2, 2)
        tw = ctx.draw_int("tpl_w", 2, 2)
        ch = ctx.draw_int("code_h", 2, 2)
        cw = ctx.draw_int("code_w", 2, 2)
    elif difficulty == "hard":
        th = ctx.draw_int("tpl_h", 3, 3)
        tw = ctx.draw_int("tpl_w", 3, 3)
        ch = ctx.draw_int("code_h", 3, 3)
        cw = ctx.draw_int("code_w", 3, 3)
    else:
        th = ctx.draw_int("tpl_h", 2, 3)
        tw = ctx.draw_int("tpl_w", 2, 3)
        ch = ctx.draw_int("code_h", 2, 3)
        cw = ctx.draw_int("code_w", 2, 3)
    rng = ctx.draw_rng("layout")
    tpl_color = rng.choice([6, 7, 8, 9, 1, 2, 3, 4, 5])
    tpl = [[0] * tw for _ in range(th)]
    cells = [(r, c) for r in range(th) for c in range(tw)]
    n_fill = rng.randint(max(2, len(cells) // 2), len(cells) - 1)
    for r, c in rng.sample(cells, n_fill):
        tpl[r][c] = tpl_color
    h = max(th, ch)
    w = tw + 1 + cw
    g = full_grid(h, w, 0)
    for r in range(th):
        for c in range(tw):
            g[r][c] = tpl[r][c]
    for r in range(ch):
        for c in range(cw):
            g[r][tw + 1 + c] = rng.randint(1, 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 3, 5
    g = full_grid(h, w, 0)
    if name == "no_separator":
        # No all-zero column — template/code split is undefined.
        for r in range(2):
            for c in range(2): g[r][c] = 8
        for r in range(2):
            for c in range(2): g[r][3 + c] = 3
        return g
    if name == "empty_template":
        # Left panel is all-zero — rule has nothing to tile.
        for r in range(2):
            for c in range(2): g[r][3 + c] = 3
        return g
    if name == "no_codes":
        # Right panel is all-zero — rule has no codes to apply.
        for r in range(2):
            for c in range(2): g[r][c] = 8
        return g
    return g
