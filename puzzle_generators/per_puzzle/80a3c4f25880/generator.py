"""Generator for arc_puzzle_bank_21_more:medium_b03 — Rotate cropped object by key.

Rule: at (0,0) is a key (1, 2, or 3). Crop the rest of the grid to its content,
then rotate by:
  - key 1: clockwise
  - key 2: 180 deg
  - other (3): counter-clockwise

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, blob_already_rect, blob_in_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "80a3c4f25880"
VERSION = "1.1.0"
TASK_ID = "80a3c4f25880"
SUMMARY = "Single colored blob + key-cell at (0,0) selecting CW/180/CCW rotation."

INVARIANTS = [
    "(0,0) holds a key in {1, 2, 3}",
    "exactly one non-touching blob of size 4..7 placed away from (0,0)",
    "blob is not a perfect rectangle (rotation makes a visible difference)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "blob_already_rect", "blob_in_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "corner_key", "valid": "corner_key"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "key":            {"type": "enum", "default": "rng", "valid": "1|2|3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        blob_size = ctx.draw_int("blob_size", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        blob_size = ctx.draw_int("blob_size", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        blob_size = ctx.draw_int("blob_size", 4, 7)
    key = ctx.draw_int("key", 1, 3)
    blob_color = ctx.draw_color("blob_color")

    g = full_grid(h, w, 0)
    g[0][0] = key
    used = {(0, 0), (0, 1), (1, 0), (1, 1)}
    rng = ctx.draw_rng("blob")
    for _ in range(20):
        blob = grow_blob(rng, h, w, used, blob_size)
        if blob is None: continue
        if any(r <= 1 and c <= 1 for r, c in blob): continue
        for r, c in blob: g[r][c] = blob_color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_key":
        # (0,0) is bg → rule has no key, rotation direction is undefined
        for r, c in [(3, 3), (3, 4), (4, 3), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "blob_already_rect":
        # solid rectangle → CW = CCW = 180 visually similar in shape, rotation barely visible
        g[0][0] = 1
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = 6
        return g
    if name == "blob_in_corner":
        # blob touches (0,0) area → key vs blob decomposition is ambiguous
        g[0][0] = 2
        for r, c in [(0, 1), (1, 0), (1, 1), (2, 1)]:
            g[r][c] = 4
        return g
    return g
