"""Generator for arc_additional_puzzles_21_set7:M45 — Crop-by-content + rotate by command.

Rule: cmd at (0,0); crop the rest; rotate by cmd value.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, blob_at_command, blob_is_rectangle.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "3748d6a4e74f"
VERSION = "1.1.0"
TASK_ID = "3748d6a4e74f"
SUMMARY = "Single colored blob + cmd at (0,0); rule crops + rotates by cmd."

INVARIANTS = [
    "(0,0) holds cmd in {1, 2, 3, 4}",
    "single non-rectangular blob away from (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "blob_at_command", "blob_is_rectangle")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..4", "valid": "1..9"},
    "blob_size":      {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "blob_color":     {"type": "color", "default": "rng", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "command_corner_with_blob",
                       "valid": "command_corner_with_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 8)
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
    g[0][0] = 1   # cmd=cw90
    if name == "no_blob":
        # cmd present but no blob → nothing to crop and rotate, output is empty/trivial
        return g
    if name == "blob_at_command":
        # blob extends into (0,0) cell → cmd is ambiguously part of the blob
        for (r, c) in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]: g[r][c] = 4
        return g
    if name == "blob_is_rectangle":
        # blob is a perfect rectangle → rotation is visually identical (or only differs by aspect)
        for r in range(2, 5):
            for c in range(3, 7): g[r][c] = 6
        return g
    return g
