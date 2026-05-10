"""Generator for arc_additional_puzzles_21_set19_bundle:M131 — recolor nested 8-frames per palette.

Rule: bottom row holds the palette (one non-zero color per nesting
depth). The rest contains nested 8-frames; output replaces the i-th
frame's 8s with palette[i].

Combinatorial axes (8): n_depths, palette_kind, inner_size, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_frames, single_depth.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "4a1526f51fb4"
VERSION = "1.1.0"
TASK_ID = "4a1526f51fb4"
SUMMARY = "Bottom-row palette (N colors) + N nested 8-frames spaced 2 apart."

INVARIANTS = [
    "background is 0",
    "the bottom row holds N non-zero palette colors at columns 0..N-1",
    "above it: N concentric 8-frames, each step inward shrinks by 2 on every side",
    "innermost frame is at least 1 cell wide/tall",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_frames", "single_depth")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_depths":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "inner_size":     {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_depths", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "concentric_frames",
                       "valid": "concentric_frames"},
    "n_distinct_colors": {"type": "int", "default": "= n_depths", "valid": "1..4"},
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
        n = ctx.draw_int("n_depths", 2, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("n_depths", 3, 4)
    else:
        n = ctx.draw_int("n_depths", 2, 3)
    rng = ctx.draw_rng("layout")
    inner_size = rng.randint(1, 3)
    out_h = inner_size + 4 * (n - 1) + 2 * (n > 0)
    out_w = inner_size + 4 * (n - 1) + 2 * (n > 0)
    if n == 0:
        out_h = out_w = 3
    h = out_h + 3  # plus padding + bottom palette row
    w = max(out_w + 4, 12)
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, n, exclude={8}))
    for i, c in enumerate(palette):
        g[h - 1][i] = c
    r0 = 1
    c0 = 2
    r1 = r0 + out_h - 1
    c1 = c0 + out_w - 1
    for d in range(n):
        rr0 = r0 + 2 * d
        cc0 = c0 + 2 * d
        rr1 = r1 - 2 * d
        cc1 = c1 - 2 * d
        if rr1 < rr0 or cc1 < cc0: break
        if rr1 == rr0 and cc1 == cc0:
            g[rr0][cc0] = 8
        else:
            draw_frame(g, rr0, cc0, rr1, cc1, 8)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # Frames present but bottom row is empty — no palette to drive
        # the recolor mapping.
        draw_frame(g, 1, 2, 5, 8, 8)
        draw_frame(g, 3, 4, 5, 6, 8)
        return g
    if name == "no_frames":
        # Palette present but no 8-frames above — rule has nothing to recolor.
        for i, c in enumerate([1, 2, 3]):
            g[h - 1][i] = c
        return g
    if name == "single_depth":
        # One frame and one palette color — the rule's nesting story has
        # only one layer, removing the depth-vs-palette mapping signal.
        draw_frame(g, 1, 2, 5, 8, 8)
        g[h - 1][0] = 4
        return g
    return g
