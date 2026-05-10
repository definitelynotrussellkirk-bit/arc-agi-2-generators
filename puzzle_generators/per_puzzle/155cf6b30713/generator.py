"""Generator for arc_puzzle_bank_nineteenth21:H127.

The first two panels show a shape transform plus a consistent color map. The
third panel is transformed and recolored by the learned relation.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers (no color-5 separator columns → rule
cannot identify panels); identity_transform (panel 2 == panel 1
→ t = identity, output = query unchanged); identity_recolor
(target_colors == source_colors → no recolor mapping, output
shape only).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "155cf6b30713"
VERSION = "1.1.0"
TASK_ID = "155cf6b30713"
SUMMARY = "Infer a panel transform and color mapping, then apply both to query."

INVARIANTS = [
    "the input has three 4x4 panels separated by color-5 columns",
    "panel 2 is a dihedral transform of panel 1 with a consistent recolor",
    "the query panel uses only colors seen in the example input panel",
    "the output is the transformed query with the learned color mapping",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_transform", "identity_recolor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":         {"type": "enum", "default": "rng", "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "position_bias":     {"type": "str", "default": "three_4x4_panels",
                          "valid": "three_4x4_panels"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_EXAMPLE_CELLS = [
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 2),
    (2, 1, 2),
    (2, 2, 3),
]
_QUERY_CELLS = [
    (0, 1, 1),
    (1, 1, 1),
    (1, 2, 2),
    (2, 2, 3),
]


def _grid_from_cells(cells, colors):
    g = full_grid(4, 4, 0)
    for r, c, slot in cells:
        g[r][c] = colors[slot - 1]
    return g


def _xform_grid(grid, code):
    h = len(grid)
    w = len(grid[0])
    if code == "r1":
        return [[grid[h - 1 - r][c] for r in range(h)] for c in range(w)]
    if code == "r2":
        return [[grid[h - 1 - r][w - 1 - c] for c in range(w)] for r in range(h)]
    if code == "r3":
        return [[grid[r][w - 1 - c] for r in range(h)] for c in range(w - 1, -1, -1)]
    if code == "fh":
        return [list(reversed(row)) for row in grid]
    if code == "fv":
        return list(reversed([row[:] for row in grid]))
    if code == "tr":
        return [[grid[r][c] for r in range(h)] for c in range(w)]
    return [[grid[h - 1 - r][w - 1 - c] for r in range(h - 1, -1, -1)] for c in range(w - 1, -1, -1)]


def _recolor(grid, mapping):
    return [[mapping.get(v, v) for v in row] for row in grid]


def _paste_panel(out, panel, grid):
    left = panel * 5
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            out[r][left + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        codes = ["fh", "fv", "tr"]
    elif difficulty == "hard":
        codes = _CODES
    else:
        codes = _CODES
    code = ctx.draw_choice("transform", codes)
    source_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    target_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    if target_colors == source_colors:
        target_colors = target_colors[1:] + target_colors[:1]
    mapping = dict(zip(source_colors, target_colors))

    ex_in = _grid_from_cells(_EXAMPLE_CELLS, source_colors)
    ex_out = _recolor(_xform_grid(ex_in, code), mapping)
    query = _grid_from_cells(_QUERY_CELLS, source_colors)

    g = full_grid(4, 14, 0)
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 5
    _paste_panel(g, 0, ex_in)
    _paste_panel(g, 1, ex_out)
    _paste_panel(g, 2, query)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    if name == "no_dividers":
        # No color-5 separators — rule cannot identify panels.
        g[0][0] = 4; g[1][0] = 4; g[1][1] = 5
        g[0][6] = 4; g[1][6] = 4
        g[0][11] = 6; g[1][12] = 7
        return g
    if name == "identity_transform":
        # Panel 2 == panel 1 (no transform) — output = query unchanged.
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 5
        for (r, c, _slot), color in zip(_EXAMPLE_CELLS, [4, 4, 6, 6, 7]):
            g[r][c] = color
            g[r][5 + c] = color
        for (r, c, _slot), color in zip(_QUERY_CELLS, [4, 4, 6, 7]):
            g[r][10 + c] = color
        return g
    if name == "identity_recolor":
        # Source == target colors — no recolor effect.
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 5
        for (r, c, _slot), color in zip(_EXAMPLE_CELLS, [4, 4, 6, 6, 7]):
            g[r][c] = color
            g[r][5 + c] = color
        for (r, c, _slot), color in zip(_QUERY_CELLS, [4, 4, 6, 7]):
            g[r][10 + c] = color
        return g
    return g
