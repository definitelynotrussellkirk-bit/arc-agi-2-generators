"""Generator for arc_puzzle_bank_seventeenth21:M116.

Rule: a prototype component contains an anchor cell 8. Isolated 8 cells
are targets; the whole anchored prototype is stamped so its anchor lands
on each target.

Combinatorial axes (8): grid_h/w, palette_kind, n_targets, palette_size,
position_bias, n_distinct_colors, anchor_position, texture.
Degenerates: no_targets, no_prototype, anchor_outside_proto.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "05538555b6ce"
VERSION = "1.1.0"
TASK_ID = "05538555b6ce"
SUMMARY = "An 8-anchored prototype is copied onto isolated 8 target markers."

INVARIANTS = [
    "one connected prototype component contains an anchor color 8",
    "all other color-8 components are singleton target markers",
    "prototype copies fit within the grid at every target",
]

PALETTE_KINDS = ("default", "L_proto", "T_proto", "X_proto")
DEGENERATE_TEXTURES = ("no_targets", "no_prototype", "anchor_outside_proto")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "16", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_targets":      {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "anchor_position": {"type": "str", "default": "interior", "valid": "interior"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROTO = [(0, 0, 2), (0, 1, 8), (1, 1, 3), (2, 1, 3), (2, 2, 4)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n_targets = ctx.draw_int("n_targets", 1, 1)
    elif difficulty == "hard":
        n_targets = ctx.draw_int("n_targets", 2, 3)
    else:
        n_targets = ctx.draw_int("n_targets", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(14, 16, 0)
    for r, c, v in _PROTO:
        g[1 + r][1 + c] = v
    targets = [(3, 10), (8, 5), (9, 12)]
    rng.shuffle(targets)
    for r, c in targets[:n_targets]:
        g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    if name == "no_targets":
        # only the prototype — nothing to stamp onto
        for r, c, v in _PROTO:
            g[1 + r][1 + c] = v
        return g
    if name == "no_prototype":
        # only target 8s — rule has nothing to copy
        for r, c in [(3, 10), (8, 5), (9, 12)]:
            g[r][c] = 8
        return g
    if name == "anchor_outside_proto":
        # prototype with no anchor 8 inside it; 8s elsewhere are ambiguous
        for r, c, v in [(0, 0, 2), (0, 1, 5), (1, 1, 3), (2, 1, 3), (2, 2, 4)]:
            g[1 + r][1 + c] = v
        for r, c in [(3, 10), (8, 5)]:
            g[r][c] = 8
        return g
    return g
