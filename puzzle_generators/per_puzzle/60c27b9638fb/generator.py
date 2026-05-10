"""Generator for arc_additional_puzzles_21_set20_bundle:M137 — Crop + transform by command.

Rule: (0,0) is cmd. Crop the rest of the grid to its content. Apply
based on cmd: 1=cw, 2=180, 3=lr, else=transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blob, blob_at_command, blob_is_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "60c27b9638fb"
VERSION = "1.1.0"
TASK_ID = "60c27b9638fb"
SUMMARY = "Single colored shape + cmd at (0,0); rule crops + transforms by cmd."

INVARIANTS = [
    "(0,0) holds cmd in {1, 2, 3, 4}",
    "single multi-color shape away from (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blob", "blob_at_command", "blob_is_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "command_with_blob",
                       "valid": "command_with_blob"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..9"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    cmd = ctx.draw_int("cmd", 1, 4)
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    rng = ctx.draw_rng("blob")
    used = {(0, 0), (0, 1), (1, 0), (1, 1)}
    n_cells = rng.randint(3, 5)
    color_rng = ctx.draw_rng("colors")
    blob = grow_blob(rng, h, w, used, n_cells)
    if blob is None:
        blob = set()
        for _ in range(n_cells):
            for _ in range(20):
                r = rng.randint(2, h - 1); c = rng.randint(2, w - 1)
                if (r, c) not in used:
                    used.add((r, c)); blob.add((r, c)); break
    if any(r <= 1 and c <= 1 for r, c in blob):
        return g
    for r, c in blob:
        g[r][c] = color_rng.randint(1, 9)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    g[0][0] = 1   # cmd = cw
    if name == "no_blob":
        # cmd present but no shape → nothing to crop and transform
        return g
    if name == "blob_at_command":
        # blob extends into (0,0)/(0,1)/(1,0)/(1,1) → cmd ambiguously part of the shape
        for (r, c) in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]: g[r][c] = 4
        return g
    if name == "blob_is_symmetric":
        # blob is rotationally symmetric → cw rotation produces same shape, rule effect invisible
        # 2x2 solid square is invariant under 90/180/transpose
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4)]: g[r][c] = 6
        return g
    return g
