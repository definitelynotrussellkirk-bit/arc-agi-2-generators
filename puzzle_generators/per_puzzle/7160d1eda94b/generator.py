"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_38_keep_bottommost_component.

Rule: among the connected non-bg components, keep only the one whose
bbox bottom row is strictly the lowest; clear the rest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, components, texture.
Degenerates: no_components, single_component, tied_bottom.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7160d1eda94b"
VERSION = "1.1.0"
TASK_ID = "7160d1eda94b"

SUMMARY = "Only the component with the lowest bounding-box bottom row is kept."

INVARIANTS = [
    "background is 0",
    "components are separated by background",
    "one component has a strictly greatest bottom row",
    "kept component preserves its original shape and color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_component", "tied_bottom")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 3..5", "valid": "2..10"},
    "palette_size":   {"type": "int", "default": "= components", "valid": "2..10"},
    "position_bias":  {"type": "str", "default": "scattered_with_one_lowest",
                       "valid": "scattered_with_one_lowest"},
    "n_distinct_colors": {"type": "int", "default": "= components", "valid": "2..10"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("components", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 11, 14)
        target = ctx.draw_int("components", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(colors)
    br = h - 2
    bc = rng.randint(1, w - 3)
    for dr, dc in ((0, 0), (1, 0), (1, 1)):
        g[br + dr][bc + dc] = colors[0]
    placed = 1
    attempts = 0
    while placed < target and attempts < 400:
        attempts += 1
        rh, rw = rng.choice([(1, 2), (2, 1), (2, 2), (1, 3)])
        r0 = rng.randint(0, max(0, h - 5))
        c0 = rng.randint(0, w - rw)
        ok = True
        for r in range(max(0, r0 - 1), min(h, r0 + rh + 1)):
            for c in range(max(0, c0 - 1), min(w, c0 + rw + 1)):
                if g[r][c] != 0:
                    ok = False
        if not ok:
            continue
        for r in range(r0, r0 + rh):
            for c in range(c0, c0 + rw):
                g[r][c] = colors[placed % len(colors)]
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 9
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no components to choose between.
        return g
    if name == "single_component":
        # Only one component exists — rule's "keep bottommost" is
        # trivially that one; rule's effect is invisible.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        return g
    if name == "tied_bottom":
        # Multiple components share the same bottom row — rule's
        # strictly-lowest tiebreak has no entry.
        for r, c in [(7, 1), (7, 2), (8, 1)]: g[r][c] = 4
        for r, c in [(7, 6), (7, 7), (8, 7)]: g[r][c] = 6
        return g
    return g
