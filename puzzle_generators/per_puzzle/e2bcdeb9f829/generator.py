"""Generator for arc_additional_puzzles_21_set22_bundle:M154 — stamp template into matching 8-frame.

Rule: non-0/non-8 cells form a template (cropped to bbox). Find an
8-color rectangle frame whose interior dimensions equal the template's
dimensions, and stamp the template into that frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_frame, frame_dim_mismatch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "e2bcdeb9f829"
VERSION = "1.1.0"
TASK_ID = "e2bcdeb9f829"
SUMMARY = "Small template (non-0/non-8) at top-left + an 8-frame whose interior matches the template's bbox."

INVARIANTS = [
    "background is 0",
    "the non-0, non-8 cells form one small connected template (2-3 colors)",
    "exactly one 8-color rectangle frame; its interior dims match the template's bbox",
    "template and frame don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frame", "frame_dim_mismatch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "template_left_8frame_right",
                       "valid": "template_left_8frame_right"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (0, 1), (1, 0), (1, 2)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 17, 19)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 14, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_TEMPLATES)
    th = max(c[0] for c in template) + 1
    tw = max(c[1] for c in template) + 1
    palette = list(random_palette(rng, 2, exclude={8}))
    cells_with_color = [(dr, dc, palette[i % 2]) for i, (dr, dc) in enumerate(template)]
    paint_at(g, 1, 1, cells_with_color)
    fr_h = th + 2
    fr_w = tw + 2
    fr_r1 = rng.randint(1, h - fr_h - 1)
    fr_c1 = rng.randint(w - fr_w - 2, w - fr_w - 1)
    fr_r2 = fr_r1 + fr_h - 1
    fr_c2 = fr_c1 + fr_w - 1
    draw_frame(g, fr_r1, fr_c1, fr_r2, fr_c2, 8)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 15
    g = full_grid(h, w, 0)
    if name == "no_template":
        # 8-frame but no template cells — rule has no shape to stamp.
        draw_frame(g, 2, 9, 5, 13, 8)
        return g
    if name == "no_frame":
        # Template but no 8-frame — rule has no destination interior
        # to stamp into.
        cells = [(0, 0, 3), (0, 1, 4), (1, 0, 3), (1, 2, 4)]
        paint_at(g, 1, 1, cells)
        return g
    if name == "frame_dim_mismatch":
        # Template + 8-frame whose interior dims do NOT match the
        # template bbox — rule's match-by-dim picker finds no
        # candidate.
        cells = [(0, 0, 3), (0, 1, 4), (1, 0, 3), (1, 2, 4)]
        paint_at(g, 1, 1, cells)
        draw_frame(g, 2, 9, 7, 13, 8)
        return g
    return g
