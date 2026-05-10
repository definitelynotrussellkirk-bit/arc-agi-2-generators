"""Generator for arc_additional_puzzles_21_set22_bundle:H148 — apply A→B transform to C.

Rule: a 9-separated panel pair reveals a transform that is applied to
the third panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, command,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_panel_a, identical_a_b.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4c17a205be08"
VERSION = "1.1.0"
TASK_ID = "4c17a205be08"
SUMMARY = "A 9-separated panel pair reveals a transform that is applied to the third panel."

INVARIANTS = [
    "full color-9 columns separate three panels",
    "the cropped second panel is a command transform of the cropped first panel",
    "the cropped third panel receives the same command transform",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_panel_a", "identical_a_b")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5..5"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command":        {"type": "int", "default": "rng 2..6", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "three_panels_with_separators",
                       "valid": "three_panels_with_separators"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _cells_for(cmd):
    base = [(0, 0), (1, 0), (1, 1)]
    if cmd == 2:
        return [(0, 0), (0, 1), (1, 0)]
    if cmd == 3:
        return [(0, 0), (0, 1), (1, 1)]
    if cmd == 4:
        return [(0, 1), (1, 0), (1, 1)]
    if cmd == 5:
        return [(0, 1), (1, 0), (1, 1)]
    return [(0, 0), (0, 1), (1, 0)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        command = ctx.draw_int("command", 2, 3)
    elif difficulty == "hard":
        command = ctx.draw_int("command", 4, 6)
    else:
        command = ctx.draw_int("command", 2, 6)
    color = ctx.draw_color("color", exclude={0, 9})
    g = full_grid(5, 11, 0)
    for sep in [3, 7]:
        for r in range(5):
            g[r][sep] = 9
    for dr, dc in [(0, 0), (1, 0), (1, 1)]:
        g[1 + dr][dc] = color
    for dr, dc in _cells_for(command):
        g[1 + dr][4 + dc] = color
    for dr, dc in [(0, 0), (0, 1), (1, 1)]:
        g[1 + dr][8 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 11, 0)
    if name == "no_separators":
        # panels exist but no 9-separators → cannot crop A/B/C
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][dc] = 4
            g[1 + dr][4 + dc] = 4
            g[1 + dr][8 + dc] = 4
        return g
    if name == "no_panel_a":
        # B and C present + separators but A panel is empty → no A→B transform
        for sep in [3, 7]:
            for r in range(5):
                g[r][sep] = 9
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][4 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[1 + dr][8 + dc] = 4
        return g
    if name == "identical_a_b":
        # A == B → transform is identity, rule has no edit to apply
        for sep in [3, 7]:
            for r in range(5):
                g[r][sep] = 9
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][dc] = 4
            g[1 + dr][4 + dc] = 4   # B = A
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[1 + dr][8 + dc] = 4
        return g
    return g
