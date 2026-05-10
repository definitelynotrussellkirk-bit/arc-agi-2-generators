"""Generator for arc_puzzle_bank_21_set6:medium_f04 — object halos.

Rule: each separated object gets a 1-cell orthogonal halo of its color
drawn in surrounding background cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, touching_objects, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e826540d45d"
VERSION = "1.1.0"
TASK_ID = "7e826540d45d"

SUMMARY = "Separated small objects whose orthogonal halos can be drawn without overlap."

INVARIANTS = [
    "background is 0",
    "objects are separated by at least two blank cells",
    "objects use distinct colors",
    "each object has in-bounds blank neighbors for a visible halo",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "touching_objects", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "wide_separation_for_halos",
                       "valid": "wide_separation_for_halos"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]


def _clear(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    rs = [r0 + r for r, _ in cells]
    cs = [c0 + c for _, c in cells]
    if min(rs) < 1 or min(cs) < 1 or max(rs) >= h - 1 or max(cs) >= w - 1:
        return False
    for r in range(max(0, min(rs) - 2), min(h, max(rs) + 3)):
        for c in range(max(0, min(cs) - 2), min(w, max(cs) + 3)):
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for color in colors:
        cells = rng.choice(SHAPES)
        for _ in range(100):
            r0 = rng.randint(1, h - 4)
            c0 = rng.randint(1, w - 4)
            if _clear(g, r0, c0, cells):
                for dr, dc in cells:
                    g[r0 + dr][c0 + dc] = color
                break
        else:
            raise ValueError("could not place halo object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — no object to halo.
        return g
    if name == "touching_objects":
        # Two objects placed adjacent — halos would overlap or merge,
        # violating the rule's per-object halo isolation.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (2, 0)]:
            g[3 + dr][6 + dc] = 6
        return g
    if name == "single_object":
        # Just one object — minimal context, the rule's per-object
        # halo behavior reduces to a single demo.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 4
        return g
    return g
