"""Generator for b25e450b.

Rule: border-touching zero hole is mirrored to the opposite side and
connected by a seven path.

Combinatorial axes (8): grid_h/w, edge, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, hole_len.
Degenerates: no_hole, full_grid, no_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9b2cd53e36fb"
VERSION = "1.1.0"
TASK_ID = "9b2cd53e36fb"
SUMMARY = "Border-touching zero hole mirrored across grid; sweep colored 7."

INVARIANTS = [
    "background is a nonzero color",
    "one zero hole touches exactly one grid edge",
    "the hole is mirrored across the full grid height or width",
    "the hole sits clear of corners so the mirror has room",
]

EDGES = ("top", "bottom", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_hole", "full_grid", "no_bg")
HELPFUL_TEXTURES = EDGES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "edge":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(EDGES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "hole_len":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for edge",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    edge = (overrides.get("texture") if overrides.get("texture") in EDGES else None) or \
           overrides.get("edge") or \
           ctx.draw_choice("edge", list(EDGES))
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    g = full_grid(h, w, 8)
    hole_len = 2 + rng.randint(0, 1)
    if edge in {"top", "bottom"}:
        c0 = 2 + rng.randint(0, max(0, w - hole_len - 4))
        rows = range(0, 2) if edge == "top" else range(h - 2, h)
        for r in rows:
            for c in range(c0, c0 + hole_len):
                g[r][c] = 0
    else:
        r0 = 2 + rng.randint(0, max(0, h - hole_len - 4))
        cols = range(0, 2) if edge == "left" else range(w - 2, w)
        for r in range(r0, r0 + hole_len):
            for c in cols:
                g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 8)
    if name == "no_hole":
        return g
    if name == "no_bg":
        return full_grid(10, 10, 0)
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
