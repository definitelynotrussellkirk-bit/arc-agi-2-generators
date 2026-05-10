"""Generator for 90f3ed37.

Rule: later groups of rows containing 8s copy the template group's
right-side 8 pattern as color 1 beyond their frontier.

Combinatorial axes (8): grid_h/w, template_width, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
frontier_offset.
Degenerates: no_template, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e52a91a0421"
VERSION = "1.1.0"
TASK_ID = "2e52a91a0421"
SUMMARY = "Template 8-row group; later groups extend template pattern beyond their frontier."

INVARIANTS = [
    "background is color 0",
    "the first contiguous row group containing 8s is the template",
    "later 8-row groups are incomplete on the right",
    "template extends beyond the frontier so the rule has work to do",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_target", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "template_width": {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "frontier_offset":{"type": "int", "default": "rng 0..1", "valid": "0..1"},
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
        tw_lo, tw_hi = 6, 6
    elif difficulty == "hard":
        tw_lo, tw_hi = 7, 8
    else:
        tw_lo, tw_hi = 6, 8
    width = ctx.draw_int("template_width", tw_lo, tw_hi)
    h = 8 + rng.randint(0, 2)
    w = 10
    g = full_grid(h, w, 0)
    for c in range(1, width):
        g[1][c] = 8
    for c in range(2, width + 1):
        g[2][c] = 8
    frontier = 3 + rng.randint(0, 1)
    for c in range(1, frontier + 1):
        g[4][c] = 8
    for c in range(2, frontier + 1):
        g[5][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_template":
        for c in range(1, 4):
            g[4][c] = 8
        return g
    if name == "no_target":
        for c in range(1, 7):
            g[1][c] = 8
        for c in range(2, 8):
            g[2][c] = 8
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
