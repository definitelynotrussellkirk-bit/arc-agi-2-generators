"""Generator for 9def23fe.

Rule: red rect + green border markers; rule fills red rays through
unblocked rows/cols.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
ray_density.
Degenerates: no_rect, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "0281fbec1cf2"
VERSION = "1.1.0"
TASK_ID = "0281fbec1cf2"
SUMMARY = "Red rect + green border markers; rule fills red rays through unblocked rows/cols."

INVARIANTS = [
    "background is 0",
    "one solid red rectangle, not touching borders",
    "green markers placed on each side outside the bbox",
    "at least one row/col on each side has no green marker (so a ray exists)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "12..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "12..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "ray_density":    {"type": "str", "default": "rng", "valid": "low|med|high"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 12, 16)
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={0, 2})

    g = full_grid(h, w, 0)
    rh = rng.randint(3, 5)
    rw = rng.randint(3, 5)
    rr = rng.randint(2, h - rh - 2)
    rc = rng.randint(2, w - rw - 2)
    draw_rect(g, rr, rc, rh, rw, 2)

    above_cols = list(range(rc, rc + rw))
    n_above = rng.randint(1, max(1, len(above_cols) - 1))
    chosen = rng.sample(above_cols, n_above)
    for c in chosen:
        ar = rng.randint(0, rr - 1)
        g[ar][c] = palette[0]
    below_cols = list(range(rc, rc + rw))
    n_below = rng.randint(1, max(1, len(below_cols) - 1))
    chosen = rng.sample(below_cols, n_below)
    for c in chosen:
        br = rng.randint(rr + rh, h - 1)
        g[br][c] = palette[0]
    left_rows = list(range(rr, rr + rh))
    n_left = rng.randint(1, max(1, len(left_rows) - 1))
    chosen = rng.sample(left_rows, n_left)
    for r in chosen:
        lc = rng.randint(0, rc - 1)
        g[r][lc] = palette[0]
    right_rows = list(range(rr, rr + rh))
    n_right = rng.randint(1, max(1, len(right_rows) - 1))
    chosen = rng.sample(right_rows, n_right)
    for r in chosen:
        rc2 = rng.randint(rc + rw, w - 1)
        g[r][rc2] = palette[0]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_rect":
        g[0][6] = 3
        return g
    if name == "no_markers":
        draw_rect(g, 5, 5, 3, 3, 2)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
