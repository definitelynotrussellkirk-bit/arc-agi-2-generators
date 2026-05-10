"""Generator for 19b:hard_131 — build boolean gallery (union, ∩, XOR).

Rule: 2 fixed 5x5 panels at cols [0..4, 6..10]. Output hstacks the
boolean union (color 2), intersection (color 3), and XOR (color 4) of
their binary masks, with 1-col gaps.

Multi-panel family: panels live at fixed offsets the rule reads. Both
panels are sampled to non-trivial densities so the boolean output
isn't all-empty or all-full.

Combinatorial axes (8): density_l, density_r, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_intersection, empty_xor, identical_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8384d9743be8"
VERSION = "1.1.0"
TASK_ID = "8384d9743be8"

SUMMARY = "2 5x5 panels at cols [0..4, 6..10] with 5-9 cells each."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 11 cols wide",
    "left panel at cols 0..4 holds 5-9 non-bg cells in a single color",
    "right panel at cols 6..10 holds 5-9 non-bg cells in a single (different) color",
    "the union, intersection, and xor each have at least one non-bg cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_intersection", "empty_xor", "identical_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "density_l":      {"type": "int", "default": "rng 5..9", "valid": "1..25"},
    "density_r":      {"type": "int", "default": "rng 5..9", "valid": "1..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_5x5_panels",
                       "valid": "two_5x5_panels"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
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
        n_lo, n_hi = 6, 9
    elif difficulty == "hard":
        n_lo, n_hi = 4, 12
    else:
        n_lo, n_hi = 5, 9
    rng = ctx.draw_rng("layout")
    h = 5; w = 11
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    for _ in range(40):
        g = full_grid(h, w, 0)
        cells_left = [(r, c) for r in range(5) for c in range(0, 5)]
        cells_right = [(r, c) for r in range(5) for c in range(6, 11)]
        n_l = rng.randint(n_lo, n_hi)
        n_r = rng.randint(n_lo, n_hi)
        slots_l = set(rng.sample(cells_left, min(n_l, 25)))
        slots_r = set(rng.sample(cells_right, min(n_r, 25)))
        a = {(r, c) for r, c in slots_l}
        b = {(r, c - 6) for r, c in slots_r}
        union = a | b
        inter = a & b
        xor = a ^ b
        if not (union and inter and xor):
            continue
        for r, c in slots_l: g[r][c] = palette[0]
        for r, c in slots_r: g[r][c] = palette[1]
        return g
    raise ValueError("could not produce panels with non-empty union/inter/xor in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 5, 11
    g = full_grid(h, w, 0)
    if name == "empty_intersection":
        # Left and right panels have no overlapping cells — boolean
        # AND output is all-empty.
        for r, c in [(0, 0), (1, 1), (2, 2)]: g[r][c] = 1
        for r, c in [(3, 6), (3, 7), (4, 8)]: g[r][c] = 4
        return g
    if name == "empty_xor":
        # Both panels share the SAME cells exactly — XOR output is
        # all-empty (rule's xor panel collapses).
        cells = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        for r, c in cells: g[r][c] = 1
        for r, c in cells: g[r][c + 6] = 4
        return g
    if name == "identical_panels":
        # Both panels identical — union==intersection, xor empty,
        # rule's three-output gallery degenerates.
        cells = [(0, 0), (1, 1), (2, 2), (1, 3), (3, 2)]
        for r, c in cells: g[r][c] = 2
        for r, c in cells: g[r][c + 6] = 7
        return g
    return g
