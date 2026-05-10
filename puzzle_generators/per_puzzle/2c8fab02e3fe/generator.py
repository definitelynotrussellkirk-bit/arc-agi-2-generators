"""Generator for arc_puzzle_bank_next_21_bundle:easy_10_fill_single_frame_by_key.

Combinatorial axes (8): grid_h, grid_w, palette_kind, key_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_key, key_inside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "2c8fab02e3fe"
VERSION = "1.1.0"
TASK_ID = "2c8fab02e3fe"
SUMMARY = "One 8-frame plus a singleton key color that fills the frame interior."

INVARIANTS = [
    "background is 0",
    "exactly one hollow rectangular frame of color 8",
    "exactly one non-8 singleton key color appears outside the frame",
    "the frame has a nonempty interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_key", "key_inside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key_color":      {"type": "color", "default": "rng", "valid": "1..9 != 8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "frame_plus_outside_key",
                       "valid": "frame_plus_outside_key"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    key = ctx.draw_color("key_color", exclude={0, 8})
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rh = rng.randint(4, min(6, h - 2))
    rw = rng.randint(4, min(7, w - 2))
    rr = rng.randint(1, h - rh - 1)
    rc = rng.randint(1, w - rw - 1)
    draw_rect_outline(g, rr, rc, rh, rw, 8)
    candidates = [
        (r, c)
        for r in range(h)
        for c in range(w)
        if not (rr <= r < rr + rh and rc <= c < rc + rw)
    ]
    kr, kc = candidates[rng.randint(0, len(candidates) - 1)]
    g[kr][kc] = key
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # key alone, no frame → no interior to fill
        g[3][7] = 4
        return g
    if name == "no_key":
        # frame alone, no key → no fill color specified
        draw_rect_outline(g, 1, 1, 5, 6, 8)
        return g
    if name == "key_inside_frame":
        # key inside the frame → "outside" precondition fails (ambiguous)
        draw_rect_outline(g, 1, 1, 5, 6, 8)
        g[3][3] = 4  # inside the frame
        return g
    return g
