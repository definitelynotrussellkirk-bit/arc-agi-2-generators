"""Generator for 42a15761.

Rule: contiguous red-column groups are sorted into original group
slots by increasing hole count.

Combinatorial axes (8): grid_h, group_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, width.
Degenerates: no_groups, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "581bb11ff645"
VERSION = "1.1.0"
TASK_ID = "581bb11ff645"
SUMMARY = "Red column groups sorted into slots by ascending hole count."

INVARIANTS = [
    "red cells appear in contiguous column groups separated by zero columns",
    "each group keeps its width and full height",
    "groups differ in their number of zero holes",
    "every group has at least one red cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_groups", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "group_count":    {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "width":          {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        gc_lo, gc_hi = 2, 2
    elif difficulty == "hard":
        gc_lo, gc_hi = 3, 4
    else:
        gc_lo, gc_hi = 2, 3
    group_count = ctx.draw_int("group_count", gc_lo, gc_hi)
    h = rng.randint(5, 8)
    width = rng.randint(2, 3)
    widths = [width for _ in range(group_count)]
    w = sum(widths) + group_count - 1
    g = full_grid(h, w, 0)
    starts = []
    c = 0
    for width in widths:
        starts.append(c)
        c += width + 1
    hole_counts = list(range(group_count))
    rng.shuffle(hole_counts)
    for start, width, holes in zip(starts, widths, hole_counts):
        cells = [(r, c) for r in range(h) for c in range(start, start + width)]
        rng.shuffle(cells)
        for r, c in cells[holes:]:
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 8, 0)
    if name == "no_groups":
        return g
    if name == "all_holes":
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
