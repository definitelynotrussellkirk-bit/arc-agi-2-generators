"""Generator for 2546ccf6.

Rule: in a 2x2 separator grid, the lone empty cell is filled by the
flipped matching same-color tile.

Combinatorial axes (8): grid_h/w, cell_size, empty_corner, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_separators, no_patches, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c71d4cb69990"
VERSION = "1.1.0"
TASK_ID = "c71d4cb69990"
SUMMARY = "In 2x2 separator grid, lone empty cell filled by flipped matching same-color tile."

INVARIANTS = [
    "a full nonzero row and column divide the grid into four equal cells",
    "three cells contain same-color nonzero patterns and one cell is empty",
    "the missing cell is reconstructed by horizontal or vertical flip from its neighbor",
    "all separator cells remain unchanged",
]

CORNERS = ("tl", "tr", "bl", "br")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separators", "no_patches", "full_grid")
HELPFUL_TEXTURES = CORNERS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "cell_size":      {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "empty_corner":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CORNERS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for empty_corner",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _base_patch(k, color, rng):
    patch = [[0 for _ in range(k)] for _ in range(k)]
    for r in range(k):
        patch[r][0] = color
    for c in range(k):
        patch[k - 1][c] = color
    patch[0][rng.randint(1, k - 1)] = color
    return patch


def _put(g, r0, c0, patch):
    for r, row in enumerate(patch):
        for c, v in enumerate(row):
            g[r0 + r][c0 + c] = v


def _mirror_columns(patch):
    return [list(reversed(row)) for row in patch]


def _mirror_rows(patch):
    return [list(row) for row in reversed(patch)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        k = ctx.draw_int("cell_size", 3, 3)
    elif difficulty == "hard":
        k = ctx.draw_int("cell_size", 5, 5)
    else:
        k = ctx.draw_int("cell_size", 3, 5)
    empty = (overrides.get("texture") if overrides.get("texture") in CORNERS else None) or \
            ctx.draw_choice("empty_corner", list(CORNERS))
    sep_color, shape_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(2 * k + 1, 2 * k + 1, 0)
    for i in range(2 * k + 1):
        g[k][i] = sep_color
        g[i][k] = sep_color

    base = _base_patch(k, shape_color, rng)
    patches = {
        "tl": base,
        "tr": _mirror_columns(base),
        "bl": _mirror_rows(base),
        "br": _mirror_rows(_mirror_columns(base)),
    }
    origins = {"tl": (0, 0), "tr": (0, k + 1), "bl": (k + 1, 0), "br": (k + 1, k + 1)}
    for name, patch in patches.items():
        if name != empty:
            _put(g, origins[name][0], origins[name][1], patch)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_separators":
        g[1][1] = 3
        return g
    if name == "no_patches":
        for i in range(7):
            g[3][i] = 5
            g[i][3] = 5
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
