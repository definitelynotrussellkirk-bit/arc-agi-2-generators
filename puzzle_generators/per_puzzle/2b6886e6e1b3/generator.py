"""Generator for arc_additional_puzzles_21_set19_bundle:H130 -- command-transform overlap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_command, no_panels, mismatched_transform.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2b6886e6e1b3"
VERSION = "1.1.0"
TASK_ID = "2b6886e6e1b3"
SUMMARY = "A command at (0,3) transforms the right 3x3 panel, then overlaps it with the left panel."

INVARIANTS = [
    "input has a left 3x3 panel and a right 3x3 panel",
    "command values 1..4 select identity, clockwise rotation, horizontal mirror, or 180 rotation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_command", "no_panels", "mismatched_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "command_plus_two_panels",
                       "valid": "command_plus_two_panels"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


BASE_MASKS = (
    ((1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((0, 2), (1, 0), (1, 1), (1, 2)),
)


def _turn_cw(cells):
    return [(c, 2 - r) for r, c in cells]


def _turn_180(cells):
    return [(2 - r, 2 - c) for r, c in cells]


def _mirror_lr(cells):
    return [(r, 2 - c) for r, c in cells]


def _inverse(cells, cmd):
    if cmd == 1:
        return list(cells)
    if cmd == 2:
        return [(2 - c, r) for r, c in cells]
    if cmd == 3:
        return _mirror_lr(cells)
    return _turn_180(cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        cmd = ctx.draw_int("cmd", 1, 1)
    elif difficulty == "hard":
        cmd = ctx.draw_int("cmd", 2, 4)
    else:
        cmd = ctx.draw_int("cmd", 1, 4)
    rng = ctx.draw_rng("layout")
    left_cells = list(rng.choice(BASE_MASKS))
    right_cells = _inverse(left_cells, cmd)
    g = full_grid(4, 7, 0)
    g[0][3] = cmd
    for r, c in left_cells:
        g[1 + r][c] = rng.choice([2, 3, 4])
    for r, c in right_cells:
        g[1 + r][4 + c] = rng.choice([5, 6, 7])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 7, 0)
    if name == "no_command":
        # panels without (0,3) command → no transform specified
        left_cells = list(BASE_MASKS[0])
        right_cells = _inverse(left_cells, 2)
        for r, c in left_cells: g[1 + r][c] = 4
        for r, c in right_cells: g[1 + r][4 + c] = 6
        return g
    if name == "no_panels":
        # command alone with no panels → no shapes to transform/overlap
        g[0][3] = 2
        return g
    if name == "mismatched_transform":
        # command says 2 (rotate-cw) but right panel doesn't match transform of left
        g[0][3] = 2
        left_cells = list(BASE_MASKS[0])
        for r, c in left_cells: g[1 + r][c] = 4
        # right panel has unrelated shape
        for r, c in BASE_MASKS[1]:
            g[1 + r][4 + c] = 6
        return g
    return g
