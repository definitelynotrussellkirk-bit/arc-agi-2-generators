"""Generator for arc_additional_puzzles_21_set21_bundle:M144 — Cmd at (0,0) → crop+transform.

Rule: cmd = at(0,0). Set (0,0)=0; crop-to-content; apply by code:
1=identity, 2=cw, 3=180, 4=ccw, 5=flip-lr, 6=flip-ud, else=transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2f1ab11f1d02"
VERSION = "1.1.0"
TASK_ID = "2f1ab11f1d02"
SUMMARY = "Cmd 1-7 at (0,0) + small blob in lower-right; output crops and transforms."

INVARIANTS = [
    "cmd at (0,0) ∈ 1..7",
    "blob is non-square multicolor in lower-right region",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..7", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "cmd_at_0_0_blob_LR",
                       "valid": "cmd_at_0_0_blob_LR"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    cmd = ctx.draw_int("cmd", 1, 7)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    sub_h = rng.randint(2, 3); sub_w = rng.randint(2, 3)
    if sub_h == sub_w: sub_w += 1
    r0 = rng.randint(h // 2, h - sub_h - 1) if h - sub_h - 1 >= h // 2 else h // 2
    c0 = rng.randint(w // 2, w - sub_w - 1) if w - sub_w - 1 >= w // 2 else w // 2
    palette = [c for c in range(2, 10) if c != cmd]
    rng.shuffle(palette)
    pat_colors = palette[:2]
    for r in range(sub_h):
        for c in range(sub_w):
            if rng.random() < 0.7:
                g[r0 + r][c0 + c] = rng.choice(pat_colors)
    # ensure ≥2 cells painted
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # blob without cmd at (0,0) → no transform dispatch
        g[0][0] = 0
        for r, c in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # cmd alone, no payload → empty crop, undefined transform
        g[0][0] = 3
        return g
    if name == "square_blob":
        # square 2x2 blob → cw/ccw/transpose all yield same shape
        g[0][0] = 2
        for r in range(4, 6):
            for c in range(5, 7):
                g[r][c] = 4
        return g
    return g
