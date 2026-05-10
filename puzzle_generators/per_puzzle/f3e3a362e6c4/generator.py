"""Generator for 8b:m51 — keyed component rotate.

Rule: corner key + same-color blob → crop blob, rotate CW.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f3e3a362e6c4"
VERSION = "1.1.0"
TASK_ID = "f3e3a362e6c4"
SUMMARY = "Corner key + same-color non-rectangular blob + 1-2 distractors."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds the key color",
    "≥1 same-color non-rectangular blob away from corner",
    "≥1 distractor blob in different color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "key_corner_blob_body",
                       "valid": "key_corner_blob_body"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    key, distractor = palette
    g[0][0] = key
    used = {(0, 0)}
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None: continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells): continue
        for r, c in cells: g[r][c] = key
        used |= cells
        break
    dist = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=40)
    if dist:
        for r, c in dist: g[r][c] = distractor
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blob present but no corner key → no key color to filter by
        for r, c in [(3, 3), (4, 3), (4, 4)]: g[r][c] = 4
        for r, c in [(2, 6), (3, 6)]: g[r][c] = 6
        return g
    if name == "no_blob":
        # corner key but no same-color blob → nothing to rotate
        g[0][0] = 4
        for r, c in [(3, 5), (4, 5)]: g[r][c] = 6
        return g
    if name == "square_blob":
        # blob is solid 2x2 → rotate-cw produces same shape
        g[0][0] = 4
        for r in range(3, 5):
            for c in range(3, 5):
                g[r][c] = 4
        for r, c in [(6, 6), (6, 7)]: g[r][c] = 6
        return g
    return g
