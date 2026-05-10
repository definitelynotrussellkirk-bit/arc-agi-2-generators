"""Generator for arc_additional_puzzles_21_set7:M47 — sort solid rectangles by size ASC, paste side-by-side.

Rule: only solid rectangles are kept. Sort by size ascending (color
tiebreak). Paste crops horizontally with 1-col gap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_rects, texture.
Degenerates: no_rectangles, all_same_size, non_rectangular_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "cb40e9cd0cca"
VERSION = "1.1.0"
TASK_ID = "cb40e9cd0cca"
SUMMARY = "2-3 solid rectangles with distinct cell counts."

INVARIANTS = [
    "background is 0",
    "2-3 solid (filled) rectangles, each a distinct color",
    "each rectangle has a distinct cell-count (h*w)",
    "rectangles don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "all_same_size", "non_rectangular_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "= n_rects", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "scattered_solid_rects",
                       "valid": "scattered_solid_rects"},
    "n_distinct_colors": {"type": "int", "default": "= n_rects", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
        n = ctx.draw_int("n_rects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 16)
        n = ctx.draw_int("n_rects", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    candidate_dims = [(2, 1), (1, 3), (2, 2), (2, 3), (3, 3), (3, 4), (4, 3)]
    rng.shuffle(candidate_dims)
    chosen: list = []
    seen_sizes: set = set()
    for rh, rw in candidate_dims:
        sz = rh * rw
        if sz in seen_sizes: continue
        chosen.append((rh, rw)); seen_sizes.add(sz)
        if len(chosen) >= n: break
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for (rh, rw), color in zip(chosen, palette):
        for _ in range(80):
            r0 = rng.randint(0, h - rh)
            c0 = rng.randint(0, w - rw)
            bb_pad = (r0 - 1, c0 - 1, r0 + rh, c0 + rw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            fill_box(g, r0, c0, r0 + rh - 1, c0 + rw - 1, color)
            placed.append((r0, c0, r0 + rh - 1, c0 + rw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # Empty grid — rule has no rectangles to sort and paste.
        return g
    if name == "all_same_size":
        # All rectangles have the same cell count — sort-by-size
        # ordering is ambiguous; rule's tiebreak by color is the
        # only signal.
        fill_box(g, 1, 1, 2, 2, 4)
        fill_box(g, 5, 5, 6, 6, 6)
        return g
    if name == "non_rectangular_blob":
        # Components are not solid rectangles — rule's
        # "only-solid-rectangles" filter excludes them all; output is
        # an empty paste.
        for r, c in [(2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]: g[r][c] = 4
        for r, c in [(6, 7), (6, 8), (7, 7)]: g[r][c] = 6
        return g
    return g
