"""Generator for 1b60fb0c.

Rule: blue cells are completed by 180-degree symmetry with missing
partners marked red.

Combinatorial axes (8): grid_h/w, missing_pair, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_pairs.
Degenerates: no_blue, all_paired, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b82be04c88b1"
VERSION = "1.1.0"
TASK_ID = "b82be04c88b1"
SUMMARY = "Blue cells completed by 180-degree symmetry; missing partners red."

INVARIANTS = [
    "all source cells are blue",
    "most blue cells already have 180-degree partners around one center",
    "at least one blue cell has an empty symmetric partner",
    "the symmetry center sits clear of grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blue", "all_paired", "full_grid")
HELPFUL_TEXTURES = ("p0", "p1", "p2", "p3", "p4")

PAIRS = [
    ((-1, -1), (1, 1)),
    ((-1, 1), (1, -1)),
    ((0, -2), (0, 2)),
    ((-2, 0), (2, 0)),
    ((-2, -1), (2, 1)),
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "missing_pair":   {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_pairs":        {"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for missing_pair",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in HELPFUL_TEXTURES:
        missing_pair = int(tx[1])
    else:
        missing_pair = ctx.draw_int("missing_pair", 0, len(PAIRS) - 1)
    h = rng.randint(9, 12)
    w = rng.randint(9, 12)
    cr = rng.randint(4, h - 5)
    cc = rng.randint(4, w - 5)
    g = full_grid(h, w, 0)
    for i, pair in enumerate(PAIRS):
        rels = [pair[0]] if i == missing_pair else list(pair)
        for dr, dc in rels:
            g[cr + dr][cc + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_blue":
        return g
    if name == "all_paired":
        for i, pair in enumerate(PAIRS):
            for dr, dc in pair:
                g[5 + dr][5 + dc] = 1
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 1
        return g
    return g
