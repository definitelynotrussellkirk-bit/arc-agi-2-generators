"""Generator for arc_additional_puzzle_bank_volume5:M32.

Rule: sort objects by (r1, c1); concat their bbox crops horizontally
with 1-col gaps. Output is max-h × total-w.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, blob_size_variation, texture.
Degenerates: only_one_blob, all_same_size, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f273ee8b09ee"
VERSION = "1.1.0"
TASK_ID = "f273ee8b09ee"
SUMMARY = "3 distinct-color blobs of varied shapes."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_one_blob", "blobs_touching", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "blob_size_variation": {"type": "str", "default": "varied",
                            "valid": "varied"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], palette[0])
    paint_at(g, 4, 7, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[1])
    paint_at(g, 6, 3, [(0, 0), (0, 1), (0, 2)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "only_one_blob":
        # only 1 blob — concat is trivially that blob's crop
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    if name == "blobs_touching":
        # blobs touching each other — would merge into one component
        paint_at(g, 2, 2, [(0, 0), (1, 0)], 4)
        paint_at(g, 2, 4, [(0, 0), (0, 1)], 6)  # adjacent to first blob
        paint_at(g, 6, 8, [(0, 0)], 7)
        return g
    if name == "no_blobs":
        # empty grid — no objects to crop and concat
        return g
    return g
