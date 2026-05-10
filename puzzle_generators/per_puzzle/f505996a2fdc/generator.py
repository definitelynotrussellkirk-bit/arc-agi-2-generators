"""Generator for arc_additional_puzzles_21_set15_bundle:M100 — Cmd at (0,0) → crop+transform.

Rule: cmd at(0,0) ∈ 1..6: 1=identity, 2=cw, 3=180, 4=transpose, 5=flip-lr,
6=flip-ud. Set (0,0)=0; crop-to-content; apply.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "f505996a2fdc"
VERSION = "1.1.0"
TASK_ID = "f505996a2fdc"
SUMMARY = "Cmd 1-6 at (0,0) + small multicolor blob in lower portion; output crops+transforms."

INVARIANTS = [
    "cmd at (0,0) ∈ 1..6",
    "blob is non-square (so transforms differ)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..6", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "cmd_plus_lower_blob",
                       "valid": "cmd_plus_lower_blob"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        cmd = ctx.draw_int("cmd", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        cmd = ctx.draw_int("cmd", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        cmd = ctx.draw_int("cmd", 1, 6)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    sub_h = rng.randint(2, 3); sub_w = rng.randint(2, 4)
    if sub_h == sub_w: sub_w += 1
    r0 = rng.randint(h // 2, h - sub_h - 1) if h - sub_h - 1 >= h // 2 else h // 2
    c0 = rng.randint(w // 3, w - sub_w - 1) if w - sub_w - 1 >= w // 3 else w // 3
    pat = random_palette(rng, 2, exclude=(1, cmd))
    for r in range(sub_h):
        for c in range(sub_w):
            if rng.random() < 0.7:
                g[r0 + r][c0 + c] = rng.choice(pat)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # blob without (0,0) cmd → no transform specified
        for r, c in [(5, 3), (5, 4), (5, 5), (6, 4)]:
            g[r][c] = 4
        return g
    if name == "no_blob":
        # cmd alone, no blob to transform
        g[0][0] = 2
        return g
    if name == "square_blob":
        # square blob → cw, 180, identity all yield same shape (no signal)
        g[0][0] = 2
        for dr in range(2):
            for dc in range(2):
                g[5 + dr][5 + dc] = 4
        return g
    return g
