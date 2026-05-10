"""Generator for arc_additional_puzzles_21_set6:M38 — cmd-driven mirror to fill zeros.

Rule: cmd at (0,0); zero out (0,0) and (0, w-1). For each cell (r,c):
if non-zero keep; else mirror — cmd=1 use base[c][r] (transpose), else
base[h-1-c][w-1-r] (anti-diagonal).

Combinatorial axes (8): grid_n, palette_kind, cmd, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_pattern, full_grid_pattern.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4f3a702ae0c4"
VERSION = "1.1.0"
TASK_ID = "4f3a702ae0c4"
SUMMARY = "Square grid; cmd at (0,0) is 1 or 2; small pattern in interior; output fills zero cells via mirror."

INVARIANTS = [
    "grid is square so transpose is well-defined",
    "cmd at (0,0) ∈ {1, 2}",
    "(0, w-1) is 0 (clear)",
    "interior has 4-7 non-zero cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_pattern", "full_grid_pattern")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_n":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "n_cells":        {"type": "int", "default": "rng 4..7", "valid": "1..15"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "cmd_at_origin_with_interior_pattern",
                       "valid": "cmd_at_origin_with_interior_pattern"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
    if difficulty == "easy":
        n = ctx.draw_int("grid_n", 7, 7)
        cmd = ctx.draw_int("cmd", 1, 1)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_n", 8, 9)
        cmd = ctx.draw_int("cmd", 1, 2)
    else:
        n = ctx.draw_int("grid_n", 7, 9)
        cmd = ctx.draw_int("cmd", 1, 2)
    h = w = n
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    n_cells = rng.randint(4, 7)
    used = {(0, 0), (0, w - 1)}
    color = rng.choice([4, 5, 6, 7, 8, 9])
    placed = 0
    for _ in range(n_cells * 5):
        if placed >= n_cells: break
        r = rng.randint(1, h - 1); c = rng.randint(1, w - 2)
        if (r, c) in used: continue
        used.add((r, c)); g[r][c] = color; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    n = 8; h = w = n
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # missing cmd → rule has no transform to choose
        for (r, c) in [(2, 3), (3, 5), (5, 2), (6, 4)]: g[r][c] = 4
        return g
    if name == "no_pattern":
        # cmd present but no interior cells → rule has nothing to mirror
        g[0][0] = 1
        return g
    if name == "full_grid_pattern":
        # interior full of cells → no zero cells to fill via mirror, rule is identity
        g[0][0] = 2
        for r in range(1, h):
            for c in range(1, w - 1):
                g[r][c] = 4
        return g
    return g
