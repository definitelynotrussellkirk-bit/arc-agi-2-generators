"""Generator for arc_additional_puzzles_21_set17_bundle:M114 — Cmd-cell at (0,0) controls crop+transform.

Rule: cmd = at (0,0). Set (0,0)=0; crop-to-content; apply transform
(0=identity, 1=rotate-cw, 2=rotate-180, 3=transpose, 4=flip-lr,
else=flip-ud).

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_blob, symmetric_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d552baa9e49e"
VERSION = "1.1.0"
TASK_ID = "d552baa9e49e"
SUMMARY = "Cmd 1-5 at (0,0) + small multicolor blob away from corner; output crops+transforms."

INVARIANTS = [
    "cmd at (0,0) is between 1 and 5",
    "blob is in lower-right region, not touching (0,0)",
    "blob has 2-3 distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_blob", "symmetric_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..5",  "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "cmd_at_origin_with_blob",
                       "valid": "cmd_at_origin_with_blob"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        cmd = ctx.draw_int("cmd", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        cmd = ctx.draw_int("cmd", 1, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        cmd = ctx.draw_int("cmd", 1, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    sub_h = rng.randint(3, 4)
    sub_w = rng.randint(3, 4)
    r0 = rng.randint(h // 2, h - sub_h - 1)
    c0 = rng.randint(w // 2, w - sub_w - 1)
    colors = rng.sample(range(1, 10), 3)
    if cmd in colors: colors.remove(cmd); colors.append(rng.choice([x for x in range(1, 10) if x != cmd and x not in colors]))
    for r in range(sub_h):
        for c in range(sub_w):
            if rng.random() < 0.6:
                g[r0 + r][c0 + c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # missing cmd at (0,0) → rule has no instruction to apply
        for r in range(5, 8):
            for c in range(6, 9):
                if (r + c) % 2 == 0: g[r][c] = 4
        return g
    if name == "no_blob":
        # cmd present but no content blob → rule has nothing to crop+transform
        g[0][0] = 3
        return g
    if name == "symmetric_blob":
        # solid 3x3 square → all transforms (rotate/transpose/flip) produce identity
        g[0][0] = 2
        for r in range(5, 8):
            for c in range(6, 9): g[r][c] = 4
        return g
    return g
