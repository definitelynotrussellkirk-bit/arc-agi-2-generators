"""Generator for 995c5fa3.

Rule: three 4x4 sections separated by columns are classified by their
zero pattern into fixed colors.

Combinatorial axes (8): section_height, fill_color, hole_pattern,
palette_kind, anchor_corner, asymmetry_force, palette_size, n_sections.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "71e2e99645f4"
VERSION = "1.1.0"
TASK_ID = "71e2e99645f4"
SUMMARY = "Three 4x4 sections classified by their zero pattern."

INVARIANTS = [
    "the input contains three 4-column sections at starts 0, 5, and 10",
    "section zero positions define the class",
    "no-zero sections map to color 2",
    "center-column holes map to 8 and left/right-edge holes map to 3",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
HOLE_PATTERNS = ("center_hole", "edge_hole", "no_hole", "mixed")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = HOLE_PATTERNS

AXES = {
    "section_height": {"type": "int", "default": "4", "valid": "4"},
    "fill_color":     {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "hole_pattern":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HOLE_PATTERNS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "n_sections":     {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for hole_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("fill_color",
                              ctx.draw_color("fill_color", exclude={0})))
    if color in (0,):
        color = pal[0] if pal else 1
    g = full_grid(4, 14, color)
    pattern = (overrides.get("texture") or
               overrides.get("hole_pattern")
               or ctx.draw_choice("hole_pattern", list(HOLE_PATTERNS)))
    if pattern == "center_hole":
        for r, c in [(1, 6), (1, 7), (2, 6), (2, 7)]:
            g[r][c] = 0
        for r in range(4):
            g[r][10] = 0
            g[r][13] = 0
    elif pattern == "edge_hole":
        for r in range(4):
            g[r][1] = 0
            g[r][3] = 0
        for r, c in [(1, 6), (1, 7), (2, 6), (2, 7)]:
            g[r][c] = 0
        for r in range(4):
            g[r][10] = 0
            g[r][13] = 0
    elif pattern == "no_hole":
        for r in range(4):
            g[r][10] = 0
            g[r][13] = 0
        for r, c in [(1, 6), (1, 7), (2, 6), (2, 7)]:
            g[r][c] = 0
    else:
        for r, c in [(1, 6), (1, 7), (2, 6), (2, 7)]:
            g[r][c] = 0
        for r in range(4):
            g[r][10] = 0
            g[r][13] = 0
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    if name == "no_holes":
        return g
    if name == "all_holes":
        for r in range(4):
            for c in range(14):
                g[r][c] = 0
        return g
    if name == "full_grid":
        for r in range(4):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
