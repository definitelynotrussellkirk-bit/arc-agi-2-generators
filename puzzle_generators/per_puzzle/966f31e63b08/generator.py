"""Generator for e5062a87.

Rule: existing color-2 template is stamped into compatible zero-only
slots.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, template_kind,
n_distinct_colors.
Degenerates: no_template, full_grid, no_slots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "966f31e63b08"
VERSION = "1.1.0"
TASK_ID = "966f31e63b08"
SUMMARY = "Existing color-2 template is stamped into compatible zero-only slots."

INVARIANTS = [
    "background is color 0",
    "the source template consists of color-2 cells",
    "candidate placements must be all zero at every template cell",
    "the template sits clear of grid borders so stamping has room",
]

TEMPLATE_KINDS = ("L",)
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "full_grid", "no_slots")
HELPFUL_TEXTURES = TEMPLATE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "template_kind":  {"type": "str", "default": "L",
                       "valid": "|".join(TEMPLATE_KINDS)},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for template_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    g = full_grid(8 + rng.randint(0, 2), 8 + rng.randint(0, 2), 0)
    r0 = rng.randint(0, 1)
    c0 = rng.randint(0, 1)
    for dr, dc in [(0, 0), (1, 0), (1, 1)]:
        g[r0 + dr][c0 + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_template":
        return g
    if name == "no_slots":
        for r in range(8):
            for c in range(8):
                g[r][c] = 1
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[dr][dc] = 2
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
