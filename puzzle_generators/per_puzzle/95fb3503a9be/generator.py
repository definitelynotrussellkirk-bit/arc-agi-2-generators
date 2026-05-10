"""Generator for arc_additional_puzzles_21_set14_bundle:M95 — sort objects by size DESC, paste side-by-side.

Rule: extract every connected non-bg object's bbox crop. Sort by size
descending, with color ascending as tiebreaker. Paste the crops
horizontally with 1-col gap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 objects share a size → "size DESC" tie-break
falls to color, output ambiguous), single_object (only 1 object → no
sort comparison needed, output trivial), no_objects (empty grid → no
crops to pack).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "95fb3503a9be"
VERSION = "1.1.0"
TASK_ID = "95fb3503a9be"
SUMMARY = "2-3 connected non-bg objects with distinct sizes."

INVARIANTS = [
    "background is 0",
    "2-3 4-connected non-bg objects, each a distinct color",
    "each object has a distinct cell-count (so size-sort is unambiguous)",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "n_objs":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_size_objects",
                       "valid": "distinct_size_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES_BY_SIZE = {
    2: [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    3: [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (0, 3)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
        [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]],
    7: [[(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)]],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_objs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 18)
        n = ctx.draw_int("n_objs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 16)
        n = ctx.draw_int("n_objs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample(list(_SHAPES_BY_SIZE.keys()), n)
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for size, color in zip(sizes, palette):
        shape = rng.choice(_SHAPES_BY_SIZE[size])
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two objects share size 4 — "size DESC" sort tie-break
        # falls to color; output ambiguous.
        for dr, dc in _SHAPES_BY_SIZE[4][0]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in _SHAPES_BY_SIZE[4][1]:
            g[1 + dr][7 + dc] = 4
        for dr, dc in _SHAPES_BY_SIZE[6][0]:
            g[5 + dr][2 + dc] = 6
        return g
    if name == "single_object":
        # Only 1 object — no sort comparison; output is trivial.
        for dr, dc in _SHAPES_BY_SIZE[5][0]:
            g[3 + dr][5 + dc] = 4
        return g
    if name == "no_objects":
        # Empty grid — no crops to pack; output empty.
        return g
    return g
