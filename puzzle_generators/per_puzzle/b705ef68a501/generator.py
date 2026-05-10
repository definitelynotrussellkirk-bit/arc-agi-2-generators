"""Generator for arc_additional_puzzles_21_set11_bundle:M75 — Pick k-th smallest object.

Rule: row 0 has k 9-cells. Below: several non-9 objects of distinct
sizes. Output is the k-th smallest object cropped to bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_header, no_objects, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "b705ef68a501"
VERSION = "1.1.0"
TASK_ID = "b705ef68a501"
SUMMARY = "Row 0 with 1-3 9-cells; below: 3-4 objects of distinct sizes (well separated)."

INVARIANTS = [
    "row 0: 1-3 cells of color 9, rest 0",
    "rows 1+: 3-4 objects of distinct sizes, each one color (≠9)",
    "objects are well-separated (≥2 bg cells apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_objects", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "4..5"},
    "position_bias":  {"type": "str", "default": "row0_count_with_objects",
                       "valid": "row0_count_with_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    PLUS_5,
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 15, 18)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_nines = rng.randint(1, 3)
    cols_for_nines = rng.sample(range(w), n_nines)
    for c in cols_for_nines:
        g[0][c] = 9
    n_objs = rng.randint(3, 4)
    chosen_shapes = []
    sizes_used = set()
    while len(chosen_shapes) < n_objs:
        s = rng.choice(SHAPES)
        if len(s) in sizes_used:
            continue
        chosen_shapes.append(s)
        sizes_used.add(len(s))
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8], n_objs)
    placed = []
    for shape, color in zip(chosen_shapes, palette):
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(2, h - sh - 1); c0 = rng.randint(0, w - sw - 1)
            if any(abs(r0 - pr) < (sh + 2) and abs(c0 - pc) < (sw + 2) for pr, pc in placed):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_header":
        # Objects but no row-0 9-cells — rule's k-selector has no
        # input.
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6)]: g[r][c] = 6
        for r, c in [(8, 9), (8, 10), (8, 11), (9, 10)]: g[r][c] = 7
        return g
    if name == "no_objects":
        # Header but no body objects — rule has no candidates.
        g[0][2] = 9; g[0][5] = 9
        return g
    if name == "tied_sizes":
        # Header k=2, body objects all the same size — rule's
        # "k-th smallest" tie-break ambiguous.
        g[0][2] = 9; g[0][5] = 9
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7)]: g[r][c] = 6
        for r, c in [(8, 9), (8, 10)]: g[r][c] = 7
        return g
    return g
