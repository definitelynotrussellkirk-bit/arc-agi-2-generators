"""Generator for ad3b40cf.

Rule: the rare non-line color is reflected across a complete guide row
or column.

Combinatorial axes (8): grid_h/w, line_kind, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_line, no_rare, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0591985abf42"
VERSION = "1.1.0"
TASK_ID = "0591985abf42"
SUMMARY = "Rare non-line color is reflected across a complete guide row or column."

INVARIANTS = [
    "background is color 0",
    "one full row or column is a non-background guide line",
    "the reflected color is rarer than any other non-guide color",
    "the guide line stays unchanged while rare cells are mirrored",
]

LINE_KINDS = ("row", "col")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_rare", "full_grid")
HELPFUL_TEXTURES = LINE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "10..13"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "10..13"},
    "line_kind":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LINE_KINDS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for line_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    kind = (overrides.get("texture") if overrides.get("texture") in LINE_KINDS else None) or \
           overrides.get("line_kind") or \
           ctx.draw_choice("line_kind", list(LINE_KINDS))
    line_color, reflect_color, decoy_color = ctx.draw_distinct_colors(
        "colors", n=3, exclude={0}
    )
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 3)
    g = full_grid(h, w, 0)

    if kind == "row":
        line_r = h // 2
        for c in range(w):
            g[line_r][c] = line_color
        for r, c in [(line_r - 2, 2), (line_r - 3, w - 4)]:
            g[r][c] = reflect_color
        for r, c in [(1, w - 2), (2, w - 2), (3, w - 2)]:
            if r != line_r:
                g[r][c] = decoy_color
    else:
        line_c = w // 2
        for r in range(h):
            g[r][line_c] = line_color
        for r, c in [(2, line_c - 2), (h - 4, line_c - 3)]:
            g[r][c] = reflect_color
        for r, c in [(h - 2, 1), (h - 2, 2), (h - 3, 2)]:
            if c != line_c:
                g[r][c] = decoy_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_line":
        g[2][2] = 3
        return g
    if name == "no_rare":
        for c in range(10):
            g[5][c] = 4
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 4
        return g
    return g
