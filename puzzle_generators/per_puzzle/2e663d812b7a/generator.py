"""Generator for 9356391f.

Rule: row-0 color key paints clipped Chebyshev rings around the first
lower seed pixel.

Combinatorial axes (8): grid_h/w, key_len, palette_kind, seed_position,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_key, no_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e663d812b7a"
VERSION = "1.1.0"
TASK_ID = "2e663d812b7a"
SUMMARY = "Row-0 color key paints clipped Chebyshev rings around lower seed."

INVARIANTS = [
    "background is color 0",
    "row 0 contains a contiguous nonzero color key from column 0",
    "there is one nonzero seed pixel at row 2 or below",
    "cells within key length of the seed are recolored by Chebyshev distance",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "key_len":        {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_position":  {"type": "str", "default": "rng",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..6"},
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
        h_lo, h_hi = 9, 11
        kl_lo, kl_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        kl_lo, kl_hi = 5, 8
    else:
        h_lo, h_hi = 11, 14
        kl_lo, kl_hi = 3, 5
    key_len = ctx.draw_int("key_len", kl_lo, kl_hi)
    key_len = max(1, min(8, key_len))
    colors = ctx.draw_distinct_colors("key_colors", n=key_len, exclude={0, 5})
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    for c, color in enumerate(colors):
        if c < w:
            g[0][c] = color
    seed_pos = overrides.get("seed_position",
                             ctx.draw_choice("seed_position",
                                             ["centered", "rng"]))
    if seed_pos == "centered":
        seed_r = h // 2
        seed_c = w // 2
    else:
        seed_r = rng.randint(4, h - 4)
        seed_c = rng.randint(3, w - 4)
    g[seed_r][seed_c] = colors[0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_key":
        g[6][6] = 2
        return g
    if name == "no_seed":
        for c in range(4):
            g[0][c] = c + 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
