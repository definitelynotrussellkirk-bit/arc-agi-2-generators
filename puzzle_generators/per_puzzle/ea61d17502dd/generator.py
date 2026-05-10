"""Generator for f3e14006.

Rule: a dominant horizontal and vertical strand define a woven rectangle.

Combinatorial axes (8): grid_h/w, primary, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_strands, single_strand, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ea61d17502dd"
VERSION = "1.1.0"
TASK_ID = "ea61d17502dd"
SUMMARY = "Dominant horizontal and vertical strand define a woven rectangle."

INVARIANTS = [
    "one row has the most non-background cells and carries a horizontal base color",
    "one column has the most non-background cells and carries a vertical base color",
    "minority colors on the dominant row and column mark the woven span",
    "the crossing cell selects which strand takes priority",
]

PRIMARIES = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_strands", "single_strand", "full_grid")
HELPFUL_TEXTURES = PRIMARIES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "primary":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PRIMARIES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for primary",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    primary = (overrides.get("texture") if overrides.get("texture") in PRIMARIES else None) or \
              overrides.get("primary") or \
              ctx.draw_choice("primary", list(PRIMARIES))
    hbase, hspec, vbase, vspec = ctx.draw_distinct_colors(
        "strand_colors", n=4, exclude={0})
    row = ctx.draw_choice("row", [5, 6])
    col = ctx.draw_choice("col", [5, 6])
    g = full_grid(12, 12, 0)

    for c in range(1, 11):
        g[row][c] = hbase
    for c in [2, 8]:
        g[row][c] = hspec
    for r in range(1, 11):
        g[r][col] = vbase
    for r in [2, 8]:
        g[r][col] = vspec
    g[row][col] = hbase if primary == "horizontal" else vbase
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_strands":
        return g
    if name == "single_strand":
        for c in range(1, 11):
            g[6][c] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
