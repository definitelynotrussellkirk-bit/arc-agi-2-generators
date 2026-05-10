"""Generator for arc_additional_puzzles_21_set10_bundle:M68 — recolor components by size rank.

Rule: row 0 carries a legend of N non-zero colors. Below row 0, find
connected (cardinal) non-zero components, sort by size descending
(tiebreak top-row then left-col), and recolor the i-th by legend[i].

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_blobs, texture.
Degenerates: no_legend, no_blobs, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "41a5c2fcf25a"
VERSION = "1.1.0"
TASK_ID = "41a5c2fcf25a"
SUMMARY = "Row-0 legend (N colors) + N distinct-size 8-blobs below; output recolors blobs by rank."

INVARIANTS = [
    "row 0 holds N distinct non-bg colors (the legend)",
    "below row 0: N connected non-bg components, all painted in color 8",
    "all components have distinct sizes (so size-rank is unambiguous)",
    "components are not cardinally adjacent (so they're separate)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_blobs", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "= n_blobs", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "legend_top_blobs_below",
                       "valid": "legend_top_blobs_below"},
    "n_distinct_colors": {"type": "int", "default": "= n_blobs+1", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

BLOB_COLOR = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 16)
        n = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n = ctx.draw_int("n_blobs", 2, 3)
    rng = ctx.draw_rng("layout")
    legend = list(random_palette(rng, n, exclude={BLOB_COLOR}))
    g = full_grid(h, w, 0)
    for i, color in enumerate(legend):
        g[0][i] = color
    sizes = rng.sample(range(2, 8), n)
    used: set[tuple[int, int]] = {(0, c) for c in range(w)}
    for s in sizes:
        blob = grow_blob(rng, h, w, used, s, max_attempts=80)
        if blob is None:
            continue
        for r, c in blob:
            g[r][c] = BLOB_COLOR
        used |= blob
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Blobs present but row-0 legend is empty — rule has no rank-to-color
        # mapping to apply.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = BLOB_COLOR
        for r, c in [(5, 6), (5, 7)]: g[r][c] = BLOB_COLOR
        return g
    if name == "no_blobs":
        # Legend present but no blobs below — rule has nothing to recolor.
        g[0][0] = 3; g[0][1] = 7
        return g
    if name == "all_same_size":
        # Legend + blobs but every blob has the same size — size-rank
        # ordering is ambiguous (no strict tiebreak path defined).
        g[0][0] = 3; g[0][1] = 7
        for r, c in [(2, 2), (2, 3)]: g[r][c] = BLOB_COLOR
        for r, c in [(5, 6), (5, 7)]: g[r][c] = BLOB_COLOR
        return g
    return g
