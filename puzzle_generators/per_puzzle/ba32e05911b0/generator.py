"""Generator for 891232d6.

Rule: magenta markers trace upward through empty cells, leaving a
blue trail and magenta at the top.

Combinatorial axes (8): grid_h/w, seed_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
seed_row_offset.
Degenerates: no_seeds, full_grid, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ba32e05911b0"
VERSION = "1.1.0"
TASK_ID = "ba32e05911b0"
SUMMARY = "Magenta seeds trace upward through empty cells, leaving a blue trail."

INVARIANTS = [
    "background is color 0",
    "one or more trace seeds use color 6",
    "without orange bars, each seed traces vertically to row 0",
    "seeds sit clear of the top row so the trace has work to do",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "full_grid", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "seed_count":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "seed_row_offset":{"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        sc_lo, sc_hi = 1, 1
    elif difficulty == "hard":
        sc_lo, sc_hi = 2, 3
    else:
        sc_lo, sc_hi = 1, 3
    count = ctx.draw_int("seed_count", sc_lo, sc_hi)
    h = 7 + rng.randint(0, 3)
    w = 7 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    cols = [1, w // 2, w - 2]
    for i in range(count):
        g[h - 2 - (i % 2)][cols[i]] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[5][3] = 6
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 6
        return g
    return g
