"""Generator for d304284e.

Rule: small color-7 mask is repeated on a stepped lattice; every third
horizontal copy recolored to 6.

Combinatorial axes (8): mask_shape, grid_h, grid_w, mask_position,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_mask, full_mask, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "443eebb271d9"
VERSION = "1.1.0"
TASK_ID = "443eebb271d9"
SUMMARY = "Small color-7 mask repeated on a stepped lattice with every-3rd recolor to 6."

INVARIANTS = [
    "background is color 0",
    "the source mask uses color 7",
    "the mask bounding box defines both the local pattern and the repeat stride",
    "copies in every third horizontal slot use color 6",
]

MASK_SHAPES = ("ell", "bar", "corner", "tee")
DEGENERATE_TEXTURES = ("no_mask", "full_mask", "full_grid")
HELPFUL_TEXTURES = MASK_SHAPES

AXES = {
    "mask_shape":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MASK_SHAPES)},
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..22"},
    "mask_position":  {"type": "str", "default": "rng",
                       "valid": "tl|center|rng"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for mask_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

MASKS = {
    "ell": [(0, 0), (1, 0), (1, 1)],
    "bar": [(0, 0), (0, 1), (0, 2)],
    "corner": [(0, 0), (0, 1), (1, 0)],
    "tee": [(0, 0), (0, 1), (0, 2), (1, 1)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 10, 13
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 14, 18, 18, 22
        rng.choice  # placeholder
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 14, 13, 18
    shape = (overrides.get("texture") or
             overrides.get("mask_shape")
             or ctx.draw_choice("mask_shape", list(MASK_SHAPES)))
    h = h_lo + rng.randint(0, h_hi - h_lo)
    w = w_lo + rng.randint(0, w_hi - w_lo)
    g = full_grid(h, w, 0)
    pos = overrides.get("mask_position",
                        ctx.draw_choice("mask_position",
                                        ["tl", "center", "rng"]))
    if pos == "center":
        r0 = max(1, h // 2 - 1)
        c0 = max(1, w // 2 - 1)
    elif pos == "rng":
        r0 = rng.randint(1, max(1, h - 4))
        c0 = rng.randint(1, max(1, w - 4))
    else:
        r0 = 1 + rng.randint(0, 1)
        c0 = 1 + rng.randint(0, 1)
    for dr, dc in MASKS[shape]:
        if r0 + dr < h and c0 + dc < w:
            g[r0 + dr][c0 + dc] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_mask":
        return g
    if name == "full_mask":
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 7
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 7
        return g
    return g
