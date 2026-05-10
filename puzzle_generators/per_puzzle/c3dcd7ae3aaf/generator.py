"""Generator for arc_additional_puzzle_bank_volume4:E26.

Rule: exact straight cyan triominoes are recolored orange.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triominoes, longer_lines, l_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c3dcd7ae3aaf"
VERSION = "1.1.0"
TASK_ID = "c3dcd7ae3aaf"
SUMMARY = "Exact straight cyan triominoes are recolored orange."

INVARIANTS = [
    "background is 0",
    "target cyan components are straight lines of exactly three cells",
    "optional longer cyan line components are non-target distractors",
    "cyan components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triominoes", "longer_lines", "l_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triominoes":   {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_triominoes",
                       "valid": "spaced_triominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_triominoes = ctx.draw_int("n_triominoes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_triominoes = ctx.draw_int("n_triominoes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_triominoes = ctx.draw_int("n_triominoes", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    horizontal = rng.choice([False, True])
    used: set[int] = set()
    made = 0
    for _ in range(200):
        if made >= n_triominoes:
            break
        if horizontal:
            choices = [r for r in range(h) if all(abs(r - rr) > 1 for rr in used)]
            if not choices:
                break
            r = rng.choice(choices)
            c = rng.randint(0, w - 3)
            for dc in range(3):
                g[r][c + dc] = 8
            used.add(r)
        else:
            choices = [c for c in range(w) if all(abs(c - cc) > 1 for cc in used)]
            if not choices:
                break
            c = rng.choice(choices)
            r = rng.randint(0, h - 3)
            for dr in range(3):
                g[r + dr][c] = 8
            used.add(c)
        made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_triominoes":
        # blank → no straight cyan lines, rule has no effect
        return g
    if name == "longer_lines":
        # 4-cell or 5-cell cyan lines → predicate "exactly 3" fails
        for c in range(1, 5): g[2][c] = 8
        for c in range(2, 7): g[5][c] = 8
        return g
    if name == "l_shapes":
        # L-shaped cyan triominoes → predicate "straight line" fails
        g[2][2] = 8; g[2][3] = 8; g[3][3] = 8
        g[5][5] = 8; g[6][5] = 8; g[6][6] = 8
        return g
    return g
