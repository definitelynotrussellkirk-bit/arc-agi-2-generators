"""Generator for arc_additional_puzzles_21_set10_bundle:H68 — XOR two binary panels split by 5-col.

Rule: a 5-filled column splits grid; left/right panels' non-zero
patterns are normalized to bbox crops, OR'd to 1; output = bbox-aligned
XOR painted as 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, empty_panel, identical_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0261c073ae3f"
VERSION = "1.1.0"
TASK_ID = "0261c073ae3f"
SUMMARY = "5-col splits grid into two panels; each contains a non-zero pattern."

INVARIANTS = [
    "exactly one full-height col of 5s",
    "left panel has at least 1 non-zero cell",
    "right panel has at least 1 non-zero cell",
    "the two normalized binary patterns differ",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "empty_panel", "identical_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_panels_5col_split",
                       "valid": "two_panels_5col_split"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 11, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sep = w // 2
    for r in range(h):
        g[r][sep] = 5
    palette_l = rng.choice([2, 3, 4, 6, 7, 8])
    palette_r = rng.choice([2, 3, 4, 6, 7, 8])
    while True:
        cells_l = set()
        cells_r = set()
        for _ in range(rng.randint(3, 5)):
            cells_l.add((rng.randint(0, h - 1), rng.randint(0, sep - 1)))
        for _ in range(rng.randint(3, 5)):
            cells_r.add((rng.randint(0, h - 1), rng.randint(sep + 1, w - 1)))
        if cells_l and cells_r:
            def norm(cells):
                rs = [r for r, _ in cells]; cs = [c for _, c in cells]
                r0, c0 = min(rs), min(cs)
                return frozenset((r - r0, c - c0) for r, c in cells)
            if norm(cells_l) != norm(cells_r):
                break
    for r, c in cells_l:
        g[r][c] = palette_l
    for r, c in cells_r:
        g[r][c] = palette_r
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 13
    g = full_grid(h, w, 0)
    if name == "no_separator":
        # Two sub-patterns but no 5-col split — rule has no panel
        # boundary; left/right partition is undefined.
        g[1][1] = 3; g[2][2] = 3
        g[1][9] = 7; g[2][10] = 7
        return g
    if name == "empty_panel":
        # 5-col present but right panel is empty — rule's XOR with an
        # empty mask just returns the left mask; rule's "panels differ"
        # invariant fails trivially.
        sep = w // 2
        for r in range(h): g[r][sep] = 5
        g[1][1] = 3; g[2][2] = 3; g[3][3] = 3
        return g
    if name == "identical_panels":
        # Both panels normalize to the same pattern — XOR is empty,
        # rule's output is all-bg; "panels differ" invariant fails.
        sep = w // 2
        for r in range(h): g[r][sep] = 5
        cells = [(0, 0), (1, 1), (2, 2)]
        for r, c in cells: g[r][c] = 3
        for r, c in cells: g[r][c + sep + 1] = 7
        return g
    return g
