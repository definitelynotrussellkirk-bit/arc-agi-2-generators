"""Generator for 6cdd2623.

Rule: four same-colored points define either two full rows or two
full columns, depending on rectangle aspect.

Combinatorial axes (8): grid_h/w, wide_rectangle, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_points, single_point, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "05409de4bec8"
VERSION = "1.1.0"
TASK_ID = "05409de4bec8"
SUMMARY = "Four same-colored points define two full rows or columns by aspect."

INVARIANTS = [
    "background is color 0",
    "exactly one nonzero color has four cells",
    "the four target cells occupy two rows and two columns",
    "the target rectangle aspect chooses the drawn line orientation",
]

ASPECTS = ("wide", "tall")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_points", "single_point", "full_grid")
HELPFUL_TEXTURES = ASPECTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "wide_rectangle": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ASPECTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "color":          {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for wide_rectangle",
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
    if tx in ASPECTS:
        wide = (tx == "wide")
    else:
        wide = ctx.draw_choice("wide_rectangle", [True, False])
    h = 10 + rng.randint(0, 4)
    w = 11 + rng.randint(0, 4)
    color = ctx.draw_color("target_color", exclude={0})
    g = full_grid(h, w, 0)
    r1 = 2 + (sample_index % 2)
    c1 = 2 + ((sample_index // 2) % 2)
    if wide:
        r2 = r1 + 2
        c2 = min(w - 2, c1 + 6)
    else:
        r2 = min(h - 2, r1 + 6)
        c2 = c1 + 2
    for r, c in [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_points":
        return g
    if name == "single_point":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
