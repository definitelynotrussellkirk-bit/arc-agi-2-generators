"""Generator for puzzle ea959feb.

Rule: detect smallest period p such that non-1 cells obey period.
Reconstruct tile + tile across grid.

Combinatorial axes (8): period, h_factor, w_factor, palette_size,
n_corruption_blocks, block_size, anchor_corner, asymmetry_force.
Degenerates: no_corruption, all_corrupted, no_period.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f839f3ccafe5"
VERSION = "1.1.0"
TASK_ID = "f839f3ccafe5"
SUMMARY = "Periodic-tiled grid w/ 1-corruption blocks; rule restores tile."

INVARIANTS = [
    "h, w divisible by p",
    "p in {3, 5, 7}",
    "tile uses colors from {2..9} (no 0 or 1)",
    "non-corruption cells obey period",
    "1-3 rectangular 1-blocks corrupt the pattern",
]

POSITION_BIASES = ("scattered", "centered", "corners", "spread")
DEGENERATE_TEXTURES = ("no_corruption", "all_corrupted", "no_period")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "period":           {"type": "int", "default": "rng [3,5,7]",
                         "valid": "3|5|7"},
    "h_factor":         {"type": "int", "default": "rng 3..4",
                         "valid": "2..5"},
    "w_factor":         {"type": "int", "default": "rng 3..4",
                         "valid": "2..5"},
    "palette_size":     {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "n_corruption":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "block_size_max":   {"type": "int", "default": "rng 3..5",
                         "valid": "2..6"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        period_pool = [3]
    elif difficulty == "hard":
        period_pool = [5, 7]
    else:
        period_pool = [3, 5, 7]
    p = int(overrides.get("period", rng.choice(period_pool)))
    if p not in (3, 5, 7):
        p = 3
    h_factor = int(overrides.get("h_factor",
                                 ctx.draw_int("h_factor", 3, 4)))
    w_factor = int(overrides.get("w_factor",
                                 ctx.draw_int("w_factor", 3, 4)))
    h = p * max(2, min(5, h_factor))
    w = p * max(2, min(5, w_factor))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    palette_pool = list(range(2, 10))
    rng.shuffle(palette_pool)
    palette = palette_pool[:palette_size]
    tile = [[rng.choice(palette) for _ in range(p)] for _ in range(p)]
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % p][c % p]
    n_blocks = int(overrides.get("n_corruption",
                                 ctx.draw_int("n_corruption", 1, 3)))
    n_blocks = max(1, min(5, n_blocks))
    block_max = int(overrides.get("block_size_max",
                                  ctx.draw_int("block_size_max", 3, 5)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    for _ in range(n_blocks):
        bh = rng.randint(2, max(2, block_max - 1))
        bw = rng.randint(2, max(2, block_max))
        if bh > h or bw > w:
            continue
        br, bc = _pick_block_pos(bias, h, w, bh, bw, rng)
        for r in range(br, min(br + bh, h)):
            for c in range(bc, min(bc + bw, w)):
                g[r][c] = 1
    return g


def _pick_block_pos(bias, h, w, bh, bw, rng):
    if bias == "centered":
        return max(0, (h - bh) // 2), max(0, (w - bw) // 2)
    if bias == "corners":
        return rng.choice([(0, 0), (0, w - bw), (h - bh, 0),
                           (h - bh, w - bw)])
    return rng.randint(0, h - bh), rng.randint(0, w - bw)


def _draw_from_degenerate(name, rng):
    p = 3
    h = p * 3; w = p * 3
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    tile = [[palette[(r + c) % 3] for c in range(p)] for r in range(p)]
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % p][c % p]
    if name == "no_corruption":
        return g
    if name == "all_corrupted":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    if name == "no_period":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        return g
    return g
