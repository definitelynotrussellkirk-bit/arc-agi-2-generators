"""Generator for arc_additional_puzzles_21_set16_bundle:M109 — cmd at (0,0) → crop+transform.

Rule: cmd ∈ 1..8: 1=id, 2=cw, 3=180, 4=transpose, 5=flip-lr, 6=flip-ud,
7=transpose, else=anti-transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e69a3b575440"
VERSION = "1.1.0"
TASK_ID = "e69a3b575440"
SUMMARY = "Cmd 1-8 at (0,0) + small blob in interior."

INVARIANTS = [
    "cmd at (0,0) ∈ 1..8",
    "blob is non-square multicolor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..8", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "tl_cmd_with_interior_blob",
                       "valid": "tl_cmd_with_interior_blob"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        cmd = ctx.draw_int("cmd", 1, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        cmd = ctx.draw_int("cmd", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        cmd = ctx.draw_int("cmd", 1, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    sub_h = rng.randint(2, 3); sub_w = rng.randint(2, 3)
    if sub_h == sub_w: sub_w += 1
    r0 = rng.randint(2, h - sub_h - 1)
    c0 = rng.randint(2, w - sub_w - 1)
    palette = [c for c in range(2, 10) if c != cmd]
    rng.shuffle(palette); pat = palette[:2]
    for r in range(sub_h):
        for c in range(sub_w):
            if rng.random() < 0.7:
                g[r0 + r][c0 + c] = rng.choice(pat)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # blob in interior but (0,0) is bg → no transform code
        g[3][3] = 4; g[3][4] = 6; g[4][3] = 7
        return g
    if name == "no_blob":
        # cmd at (0,0) but no interior blob → nothing to transform
        g[0][0] = 2
        return g
    if name == "square_blob":
        # blob is N×N square → transpose / cw / id all visually identical
        g[0][0] = 4
        g[3][3] = 6; g[3][4] = 6
        g[4][3] = 6; g[4][4] = 6
        return g
    return g
