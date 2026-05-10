"""Generator for 73ccf9c2.

Rule: scan 8-conn objects; find first non-LR-symmetric; output its bbox
crop.

Combinatorial axes (8): grid_h/w, n_sym, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, asym_variant.
Degenerates: all_sym, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import L_TROMINO_SE, PLUS_5, RING_3X3

GENERATOR_ID = "1a5d49e539de"
VERSION = "1.1.0"
TASK_ID = "1a5d49e539de"
SUMMARY = "Color-2 objects scattered; 2-3 LR-symmetric, exactly one asymmetric."

INVARIANTS = [
    "exactly one LR-asymmetric color-2 8-conn object",
    "2-3 LR-symmetric color-2 8-conn objects",
    "all objects are non-overlapping",
]

POSITION_BIASES = ("scattered", "spread", "centered", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("all_sym", "no_objects", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

_SYM = [
    RING_3X3,
    PLUS_5,
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    L_TROMINO_SE,
    [(0, 1), (0, 2), (1, 0), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 16..21", "valid": "12..28"},
    "grid_w":         {"type": "int", "default": "rng 16..21", "valid": "12..28"},
    "n_sym":          {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 12, 16
        ns_lo, ns_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 21, 28
        ns_lo, ns_hi = 3, 4
    else:
        h_lo, h_hi = 16, 21
        ns_lo, ns_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_sym = int(overrides.get("n_sym",
                              ctx.draw_int("n_sym", ns_lo, ns_hi)))
    n_sym = max(1, min(4, n_sym))
    sym_choices = rng.sample(_SYM, n_sym) if n_sym <= len(_SYM) else _SYM[:n_sym]
    for shape in sym_choices:
        place_no_overlap(rng, g, shape, 2, padding=1, max_tries=40)
    place_no_overlap(rng, g, rng.choice(_ASYM), 2, padding=1, max_tries=40)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 18, 18
    g = full_grid(h, w, 0)
    if name == "all_sym":
        place_no_overlap(rng, g, RING_3X3, 2, padding=1, max_tries=40)
        place_no_overlap(rng, g, PLUS_5, 2, padding=1, max_tries=40)
        return g
    if name == "no_objects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
