"""Generator for arc_puzzle_bank_21_set19_s:S19_E1.

Two same-size panels are unioned into an 8-mask.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_overlap, identical_panels, panel_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels

GENERATOR_ID = "5573cf8e2aa4"
VERSION = "1.1.0"
TASK_ID = "5573cf8e2aa4"
SUMMARY = "Two same-size panels are unioned into an 8-mask."

INVARIANTS = [
    "two vertical panels separated by color 9",
    "panels have the same dimensions",
    "nonzero cells in either panel appear in the output mask",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_overlap", "identical_panels", "panel_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 4..7 per panel",
                       "valid": "1..height*width"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_panels_with_overlap",
                       "valid": "two_panels_with_overlap"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    rng = ctx.draw_rng("cells")
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    a_count = ctx.draw_int("a_count", 4, min(7, len(cells) - 3))
    b_count = ctx.draw_int("b_count", 4, min(7, len(cells) - 3))
    a_cells = set(cells[:a_count])
    b_cells = set(cells[a_count:a_count + b_count])
    if rng.random() < 0.6:
        b_cells.add(rng.choice(tuple(a_cells)))
    return assemble_vertical_panels([
        _panel(h, w, a_cells, 2),
        _panel(h, w, b_cells, 3),
    ])


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    if name == "no_overlap":
        # disjoint panels → union still informative but no shared cells (rule still works)
        a = _panel(h, w, [(0, 0), (1, 1), (2, 2)], 2)
        b = _panel(h, w, [(0, 4), (3, 0), (4, 4)], 3)
        return assemble_vertical_panels([a, b])
    if name == "identical_panels":
        # both panels identical → union equals each, redundant signal
        cells = [(0, 0), (1, 1), (2, 2)]
        a = _panel(h, w, cells, 2)
        b = _panel(h, w, cells, 3)
        return assemble_vertical_panels([a, b])
    if name == "panel_empty":
        # one panel empty → union equals the other panel (no contrast)
        a = _panel(h, w, [], 2)
        b = _panel(h, w, [(0, 0), (1, 1), (2, 2)], 3)
        return assemble_vertical_panels([a, b])
    return full_grid(h, w * 2 + 1, 0)
