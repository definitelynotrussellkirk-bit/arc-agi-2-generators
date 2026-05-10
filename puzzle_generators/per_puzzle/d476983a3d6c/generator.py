"""Generator for arc_puzzle_bank_21_set6:hard_f06.

The top-left key chooses how same-colored marker pairs are connected: horizontal
then vertical for key 1, or vertical then horizontal for key 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, command,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_pairs, aligned_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d476983a3d6c"
VERSION = "1.1.0"
TASK_ID = "d476983a3d6c"
SUMMARY = "A corner key selects L-path order for each same-color marker pair."

INVARIANTS = [
    "cell (0,0) is command 1 or 2",
    "each non-command color appears exactly twice as single-cell markers",
    "same-color pairs are separated in both row and column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_pairs", "aligned_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command":        {"type": "int", "default": "rng 1|2", "valid": "1 or 2"},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "key_plus_separated_pairs",
                       "valid": "key_plus_separated_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    command = ctx.draw_choice("command", [1, 2])
    if difficulty == "easy":
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        n_pairs = ctx.draw_int("n_pairs", 3, 4)
    else:
        n_pairs = ctx.draw_int("n_pairs", 2, 4)
    g = full_grid(10, 10, 0)
    g[0][0] = command
    colors = [2, 3, 4, 5][:n_pairs]
    used = {(0, 0)}
    for color in colors:
        for _ in range(200):
            p1 = (rng.randint(1, 8), rng.randint(1, 8))
            p2 = (rng.randint(1, 8), rng.randint(1, 8))
            if p1 in used or p2 in used or p1 == p2:
                continue
            if p1[0] == p2[0] or p1[1] == p2[1]:
                continue
            used.add(p1)
            used.add(p2)
            g[p1[0]][p1[1]] = color
            g[p2[0]][p2[1]] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_key":
        # pairs without (0,0) command → no L-path order specified
        g[2][2] = 4; g[5][6] = 4
        g[3][7] = 6; g[7][2] = 6
        return g
    if name == "no_pairs":
        # command alone with no pairs → no markers to connect
        g[0][0] = 1
        return g
    if name == "aligned_pair":
        # pair shares a row → L-path is degenerate (just one segment)
        g[0][0] = 1
        g[3][2] = 4; g[3][7] = 4  # same row
        return g
    return g
