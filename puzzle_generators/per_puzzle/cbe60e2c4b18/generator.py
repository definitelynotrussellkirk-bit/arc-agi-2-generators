"""Generator for arc_puzzle_bank_21_set19_s:S19_E2.

Two same-size panels are intersected into an 8-mask.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shared_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, panels_identical, panel_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels

GENERATOR_ID = "cbe60e2c4b18"
VERSION = "1.1.0"
TASK_ID = "cbe60e2c4b18"
SUMMARY = "Two same-size panels are intersected into an 8-mask."

INVARIANTS = [
    "two vertical panels separated by color 9",
    "panels have at least one shared occupied coordinate",
    "only shared occupied coordinates appear in the output mask",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "panels_identical", "panel_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shared_count":   {"type": "int", "default": "rng 2..4", "valid": "1..40"},
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
        shared_count = ctx.draw_int("shared_count", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        shared_count = ctx.draw_int("shared_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        shared_count = ctx.draw_int("shared_count", 2, 4)
    rng = ctx.draw_rng("cells")
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    shared = set(cells[:shared_count])
    extra_a = set(cells[shared_count:shared_count + 3])
    extra_b = set(cells[shared_count + 3:shared_count + 6])
    return assemble_vertical_panels([
        _panel(h, w, shared | extra_a, 4),
        _panel(h, w, shared | extra_b, 6),
    ])


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    if name == "no_shared":
        # disjoint supports → intersection mask is empty
        a = _panel(h, w, [(0, 0), (1, 1), (2, 2)], 4)
        b = _panel(h, w, [(0, 4), (1, 3), (2, 0)], 6)
        return assemble_vertical_panels([a, b])
    if name == "panels_identical":
        # identical supports → intersection equals each panel (no contrast)
        cells = [(0, 0), (1, 1), (2, 2), (3, 3)]
        a = _panel(h, w, cells, 4)
        b = _panel(h, w, cells, 6)
        return assemble_vertical_panels([a, b])
    if name == "panel_empty":
        # one panel empty → intersection is empty regardless of the other
        a = _panel(h, w, [], 4)
        b = _panel(h, w, [(0, 0), (1, 1), (2, 2)], 6)
        return assemble_vertical_panels([a, b])
    return full_grid(h, w * 2 + 1, 0)
