"""Generator for arc_puzzle_bank_21_set4:S4_M7 — T shapes to pluses.

Rule: each color-3 four-cell T gets its missing arm filled to make a plus.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_shapes, non_t_shape, single_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e1cd9abbb81"
VERSION = "1.1.0"
TASK_ID = "2e1cd9abbb81"

SUMMARY = "Separated green four-cell T shapes, each missing one plus arm."

INVARIANTS = [
    "background is 0",
    "each color-3 object is exactly one of the four 4-cell T shapes",
    "each T has room for the missing plus arm in-bounds",
    "T objects are separated so they remain distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shapes", "non_t_shape", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "str", "default": "1 (color 3)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_isolated",
                       "valid": "scattered_isolated"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
]


def _clear(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    rs = [r0 + r for r, _ in cells]
    cs = [c0 + c for _, c in cells]
    if min(rs) < 1 or min(cs) < 1 or max(rs) >= h - 1 or max(cs) >= w - 1:
        return False
    for r in range(min(rs) - 1, max(rs) + 2):
        for c in range(min(cs) - 1, max(cs) + 2):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(rng.randint(1, 3)):
        cells = rng.choice(SHAPES)
        for _attempt in range(80):
            r0 = rng.randint(1, h - 4)
            c0 = rng.randint(1, w - 4)
            if _clear(g, r0, c0, cells):
                for dr, dc in cells:
                    g[r0 + dr][c0 + dc] = 3
                break
        else:
            raise ValueError("could not place T shape")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        # Empty grid — no T to extend into a plus.
        return g
    if name == "non_t_shape":
        # 2x2 squares — rule's T-match never fires, so the rule is a no-op.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][7 + dc] = 3
        return g
    if name == "single_shape":
        # Just one T — minimal context.
        for dr, dc in SHAPES[0]:
            g[3 + dr][4 + dc] = 3
        return g
    return g
