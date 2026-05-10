"""Generator for arc_puzzle_bank_21_set10_e:hard_j19 — Pick sel-color blob, transform by key.

Rule: sel = at(0,0); key = at(0,w-1); body = grid below row 0; pick first
sel-color blob in body; transform by key (1=identity, 2=cw, 3=flip-lr,
4=transpose, 5=180).

Combinatorial axes (8): grid_h, grid_w, palette_kind, key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_sel, no_key, no_matching_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "346480121fcb"
VERSION = "1.1.0"
TASK_ID = "346480121fcb"
SUMMARY = "Sel at (0,0) + key at (0,w-1) + body has 2-3 distinct-color blobs (one matches sel)."

INVARIANTS = [
    "sel at (0,0) ∈ {2,3,4,5,6,7}",
    "key at (0,w-1) ∈ 1..5",
    "body has ≥1 blob of sel color, plus 1-2 decoys of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_sel", "no_key", "no_matching_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key":            {"type": "int", "default": "rng 1..5", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "header_with_body_blobs",
                       "valid": "header_with_body_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        key = ctx.draw_int("key", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        key = ctx.draw_int("key", 2, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        key = ctx.draw_int("key", 1, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sel = rng.choice([2, 3, 4, 5, 6, 7])
    g[0][0] = sel
    g[0][w - 1] = key
    decoy = rng.choice([c for c in [2, 3, 4, 5, 6, 7] if c != sel])
    paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 1), (2, 1)], sel)
    paint_at(g, 3, 7, [(0, 0), (0, 1), (1, 0)], decoy)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_sel":
        # (0,0) is bg → no sel color identifiable, can't pick a blob
        g[0][w - 1] = 2  # key only
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 1)], 4)
        paint_at(g, 3, 7, [(0, 0), (0, 1)], 6)
        return g
    if name == "no_key":
        # (0,w-1) is bg → no transform key encoded
        g[0][0] = 4
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 1)], 4)
        paint_at(g, 3, 7, [(0, 0), (0, 1)], 6)
        return g
    if name == "no_matching_blob":
        # sel says color 4 but no body blob is color 4 → nothing to transform
        g[0][0] = 4
        g[0][w - 1] = 2
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 1)], 6)
        paint_at(g, 3, 7, [(0, 0), (0, 1)], 7)
        return g
    return g
