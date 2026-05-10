"""Generator for arc_additional_puzzles_21_set3:M19 — Recolor 8-blobs by size rank.

Rule: sort 8-blobs by size asc; recolor 1st→2, 2nd→3, 3rd→4. Output starts
from empty grid (only the recolored blobs remain).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "2c4317f69f0a"
VERSION = "1.1.0"
TASK_ID = "2c4317f69f0a"
SUMMARY = "3 non-touching 8-blobs of distinct sizes; output recolors by size rank to 2,3,4."

INVARIANTS = [
    "exactly 3 non-touching 8-blobs",
    "all distinct sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "non_touching",
                       "valid": "non_touching"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = list(range(2, 7)); rng.shuffle(sizes); sizes = sorted(sizes[:3])
    used = set()
    for size in sizes:
        for _ in range(15):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = 8
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # two 8-blobs same size → rank tie, which becomes 2 vs 3 ambiguous
        for r, c in [(1, 1), (2, 1)]: g[r][c] = 8
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 8
        for r, c in [(7, 1), (7, 2), (8, 1)]: g[r][c] = 8
        return g
    if name == "single_blob":
        # only one 8-blob → no rank-ordering, smallest=largest
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 8
        return g
    if name == "no_blobs":
        # empty grid → no blobs to recolor by rank
        return g
    return g
