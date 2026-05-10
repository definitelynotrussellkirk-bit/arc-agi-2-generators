"""Generator for arc_additional_puzzles_21_set8:M53 — Rotate cropped object by command.

Rule: at (0,0) is a command in {1, 2, 3, else}. Crop rest of grid to content
and rotate:
  - cmd 1: identity
  - cmd 2: rotate-cw
  - cmd 3: rotate-180
  - else: rotate-ccw

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, blob_already_rect, blob_in_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "36adc51834d3"
VERSION = "1.1.0"
TASK_ID = "36adc51834d3"
SUMMARY = "Single colored blob + command-cell at (0,0) selecting identity/CW/180/CCW."

INVARIANTS = [
    "(0,0) holds a cmd in {1, 2, 3, 4}",
    "single non-rectangular blob away from (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "blob_already_rect", "blob_in_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "corner_cmd",
                       "valid": "corner_cmd"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "cmd":            {"type": "int", "default": "rng 1..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        size = ctx.draw_int("blob_size", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        size = ctx.draw_int("blob_size", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        size = ctx.draw_int("blob_size", 4, 7)
    cmd = ctx.draw_int("cmd", 1, 4)
    color = ctx.draw_color("blob_color")
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    used = {(0, 0), (0, 1), (1, 0), (1, 1)}
    rng = ctx.draw_rng("blob")
    for _ in range(20):
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        if any(r <= 1 and c <= 1 for r, c in blob): continue
        for r, c in blob: g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # (0,0) is bg → no rotation cmd, rule defaults or fails
        for r, c in [(3, 3), (3, 4), (4, 3), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "blob_already_rect":
        # solid rect → all rotations look identical (2x2 square invariant under 90deg)
        g[0][0] = 2
        for r in range(3, 5):
            for c in range(3, 5):
                g[r][c] = 6
        return g
    if name == "blob_in_corner":
        # blob touches (0,0) area → cmd vs blob decomposition is ambiguous
        g[0][0] = 2
        for r, c in [(0, 1), (1, 0), (1, 1), (2, 1)]:
            g[r][c] = 4
        return g
    return g
