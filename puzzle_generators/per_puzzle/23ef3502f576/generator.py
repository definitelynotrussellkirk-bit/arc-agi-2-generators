"""Generator for arc_puzzle_bank_21_set19_s:S19_E4.

A top header's nonzero count selects one of three row panels.

Combinatorial axes (8): panel_h, panel_w, palette_kind, choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_header, no_panels, count_out_of_range.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_horizontal_panels

GENERATOR_ID = "23ef3502f576"
VERSION = "1.1.0"
TASK_ID = "23ef3502f576"
SUMMARY = "A top header's nonzero count selects one of three row panels."

INVARIANTS = [
    "four horizontal panels separated by color 9",
    "the header contains exactly one, two, or three nonzero cells",
    "the chosen body panel is recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_panels", "count_out_of_range")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 5..6", "valid": "3..8"},
    "panel_w":        {"type": "int", "default": "rng 6..8", "valid": "3..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "choice":         {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "header_plus_three_panels",
                       "valid": "header_plus_three_panels"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _panel(h, w, cells, color):
    panel = full_grid(h, w, 0)
    for r, c in cells:
        panel[r][c] = color
    return panel


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        ph = ctx.draw_int("panel_h", 5, 5)
        pw = ctx.draw_int("panel_w", 6, 7)
        choice = ctx.draw_int("choice", 1, 1)
    elif difficulty == "hard":
        ph = ctx.draw_int("panel_h", 6, 6)
        pw = ctx.draw_int("panel_w", 7, 8)
        choice = ctx.draw_int("choice", 2, 3)
    else:
        ph = ctx.draw_int("panel_h", 5, 6)
        pw = ctx.draw_int("panel_w", 6, 8)
        choice = ctx.draw_int("choice", 1, 3)
    rng = ctx.draw_rng("layout")
    header = full_grid(2, pw, 0)
    header_cells = [(r, c) for r in range(2) for c in range(pw)]
    for r, c in rng.sample(header_cells, choice):
        header[r][c] = 2
    panels = []
    for idx, count in enumerate([4, 6, 8]):
        cells = [(r, c) for r in range(ph) for c in range(pw)]
        rng.shuffle(cells)
        panels.append(_panel(ph, pw, cells[:count], 3 + idx))
    return assemble_horizontal_panels([header] + panels)


def _draw_from_degenerate(name, rng):
    ph, pw = 5, 7
    if name == "no_header":
        # blank header (count = 0) → no panel selected
        header = full_grid(2, pw, 0)
        panels = []
        cells = [(r, c) for r in range(ph) for c in range(pw)]
        for idx, count in enumerate([4, 6, 8]):
            rng = __import__("random").Random(0)
            rng.shuffle(cells)
            panels.append(_panel(ph, pw, cells[:count], 3 + idx))
        return assemble_horizontal_panels([header] + panels)
    if name == "no_panels":
        # header alone with no body panels → nothing to recolor
        header = full_grid(2, pw, 0)
        header[0][0] = 2
        return header
    if name == "count_out_of_range":
        # header has 4+ nonzero cells → "1, 2, or 3" precondition fails
        header = full_grid(2, pw, 0)
        for r in range(2):
            for c in range(2):
                header[r][c] = 2
        panels = []
        cells = [(r, c) for r in range(ph) for c in range(pw)]
        for idx, count in enumerate([4, 6, 8]):
            panels.append(_panel(ph, pw, cells[:count], 3 + idx))
        return assemble_horizontal_panels([header] + panels)
    return full_grid(ph, pw, 0)
