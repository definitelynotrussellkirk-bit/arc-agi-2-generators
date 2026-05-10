"""Generator for additional_scaffolded:M2 — Recolor the largest green object to color 8.

Rule: of the green(3) connected components, find the largest by size
and paint its cells with 8. All other objects (including smaller
greens) stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_green,
n_distractor, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_green, no_green.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "b0c53711eaf4"
VERSION = "1.1.0"
TASK_ID = "b0c53711eaf4"
SUMMARY = "Several green-3 blobs of distinct sizes plus distractors; recolor the largest green to 8."

INVARIANTS = [
    "between 2 and 4 green(3) components",
    "the largest green has a UNIQUE size (no tie)",
    "1..2 distractor blobs of other non-green colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_green", "no_green")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_green":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "n_distractor":   {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread_distinct_sizes",
                       "valid": "spread_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        n_green = ctx.draw_int("n_green", 2, 2)
        n_distractor = ctx.draw_int("n_distractor", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_green = ctx.draw_int("n_green", 3, 4)
        n_distractor = ctx.draw_int("n_distractor", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_green = ctx.draw_int("n_green", 2, 4)
        n_distractor = ctx.draw_int("n_distractor", 1, 2)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    sizes = list(range(1, 6))
    rng.shuffle(sizes)
    sizes = sorted(sizes[:n_green])
    for size in sizes:
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = 3
    distract_colors = [c for c in (1, 2, 4, 5, 6, 7, 8, 9)]
    rng.shuffle(distract_colors)
    for i in range(n_distractor):
        if i >= len(distract_colors): break
        size = rng.randint(1, 4)
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = distract_colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two green objects share the maximum size → "uniquely largest" predicate fails, ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 3   # 4 cells
        for (r, c) in [(5, 5), (5, 6), (6, 5), (6, 6)]: g[r][c] = 3   # also 4 cells
        for (r, c) in [(8, 1)]: g[r][c] = 4   # distractor
        return g
    if name == "single_green":
        # only one green → trivially largest, no comparison
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4), (5, 4)]: g[r][c] = 3
        for (r, c) in [(1, 7), (8, 1)]: g[r][c] = 6   # distractors
        return g
    if name == "no_green":
        # no color-3 cells → rule has nothing to recolor, output equals input
        for (r, c) in [(2, 3), (3, 3), (3, 4)]: g[r][c] = 4
        for (r, c) in [(6, 6), (6, 7)]: g[r][c] = 8
        return g
    return g
