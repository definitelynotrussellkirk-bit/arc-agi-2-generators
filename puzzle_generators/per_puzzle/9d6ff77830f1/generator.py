"""Generator for arc_puzzle_bank_21_set3:S3_H2.

Rule: top-row 1-marker count selects the green object with that hole count;
clear markers, recolor to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_objects, all_zero_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9d6ff77830f1"
VERSION = "1.1.0"
TASK_ID = "9d6ff77830f1"
SUMMARY = "Top-row marker count selects the green object with that hole count."

INVARIANTS = [
    "top-row color-1 cells encode a hole count",
    "all candidate objects are color 3 and below row 0",
    "exactly one candidate has the encoded number of enclosed zero holes",
    "the selected object is recolored to 2 while top markers are cleared",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_objects", "all_zero_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_w":         {"type": "int", "default": "rng 18..20", "valid": "14..24"},
    "target_holes":   {"type": "int", "default": "rng choice 1|2", "valid": "1 or 2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "header_with_objects",
                       "valid": "header_with_objects"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_frame(g, top, left, color=3):
    for c in range(left, left + 4):
        g[top][c] = color
        g[top + 3][c] = color
    for r in range(top + 1, top + 3):
        g[r][left] = color
        g[r][left + 3] = color


def _draw_solid_box(g, top, left, color=3):
    for r in range(top, top + 3):
        for c in range(left, left + 3):
            g[r][c] = color


def _draw_double_frame(g, top, left, color=3):
    _draw_frame(g, top, left, color)
    _draw_frame(g, top, left + 5, color)
    g[top + 1][left + 4] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        w = ctx.draw_int("grid_w", 18, 18)
    elif difficulty == "hard":
        w = ctx.draw_int("grid_w", 20, 23)
    else:
        w = ctx.draw_int("grid_w", 18, 20)
    target_holes = ctx.draw_choice("target_holes", [1, 2])
    g = full_grid(9, w, 0)

    marker_start = rng.randint(1, 4)
    for c in range(marker_start, marker_start + target_holes):
        g[0][c] = 1

    shift = rng.randint(0, max(0, w - 18))
    if target_holes == 1:
        _draw_frame(g, 2, 2 + shift)
        _draw_solid_box(g, 3, 11 + shift)
    else:
        _draw_double_frame(g, 2, 1 + shift)
        _draw_frame(g, 3, 14 + shift)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 18, 0)
    if name == "no_markers":
        # Objects but no top-row markers — rule's hole-count
        # selector has no input.
        _draw_frame(g, 2, 2)
        _draw_solid_box(g, 3, 11)
        return g
    if name == "no_objects":
        # Markers but no body objects — rule has no candidates
        # to select from.
        g[0][2] = 1; g[0][3] = 1
        return g
    if name == "all_zero_holes":
        # Markers say "1 hole" but all candidates are solid
        # (zero holes) — no candidate matches; selection undefined.
        g[0][2] = 1
        _draw_solid_box(g, 3, 2)
        _draw_solid_box(g, 3, 11)
        return g
    return g
