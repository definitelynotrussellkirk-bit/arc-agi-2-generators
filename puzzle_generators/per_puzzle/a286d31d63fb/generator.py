"""Generator for arc_puzzle_bank_21_set14_s:S14_E4 — flat-row components → 8.

Rule: components whose row profiles are flat (each row has the same
cell count) are recolored to 8; non-flat components stay as-is.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_flat (rule recolors every component → no contrast),
all_non_flat (rule recolors none → output equals input),
single_component (one comp only → no flat/non-flat contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a286d31d63fb"
VERSION = "1.1.0"
TASK_ID = "a286d31d63fb"
SUMMARY = "Components whose row profiles are flat are recolored to 8 while non-flat components remain unchanged."

INVARIANTS = [
    "background is 0",
    "there is at least one component with a constant row profile",
    "there is at least one component with a non-constant row profile",
    "only constant-row-profile components are recolored",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_flat", "all_non_flat", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":            {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":             {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "flat_component_count": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "scattered_flat_and_nonflat",
                          "valid": "scattered_flat_and_nonflat"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_FLAT = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
]
_NON_FLAT = [
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]


def _size(shape):
    return max(r for r, _ in shape) + 1, max(c for _, c in shape) + 1


def _free(g, r0, c0, shape, pad=1):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    if r0 < 0 or c0 < 0 or r0 + sh > h or c0 + sw > w:
        return False
    for r in range(max(0, r0 - pad), min(h, r0 + sh + pad)):
        for c in range(max(0, c0 - pad), min(w, c0 + sw + pad)):
            if g[r][c] != 0:
                return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    for _ in range(120):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free(g, r0, c0, shape):
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            return
    raise ValueError("could not place component")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
        flat_count = ctx.draw_int("flat_component_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 15, 18)
        flat_count = ctx.draw_int("flat_component_count", 2, 3)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
        flat_count = ctx.draw_int("flat_component_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5]
    rng.shuffle(colors)
    for i in range(flat_count):
        _place(g, rng, rng.choice(_FLAT), colors[i])
    for color in colors[flat_count:flat_count + 2]:
        _place(g, rng, rng.choice(_NON_FLAT), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "all_flat":
        # All components have flat row profile — rule recolors every
        # component to 8; no flat/non-flat contrast in output.
        for dr, dc in _FLAT[0]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in _FLAT[1]:
            g[5 + dr][7 + dc] = 3
        for dr, dc in _FLAT[2]:
            g[7 + dr][2 + dc] = 4
        return g
    if name == "all_non_flat":
        # All components are non-flat — rule recolors nothing; output
        # equals input exactly.
        for dr, dc in _NON_FLAT[0]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in _NON_FLAT[1]:
            g[5 + dr][7 + dc] = 3
        for dr, dc in _NON_FLAT[2]:
            g[8 + dr][2 + dc] = 4
        return g
    if name == "single_component":
        # Only one component — no flat/non-flat contrast in output.
        for dr, dc in _FLAT[2]:
            g[3 + dr][5 + dc] = 6
        return g
    return g
