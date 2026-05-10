"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_39_crop_tallest_component.

Rule: the unique tallest connected component is cropped out by its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, tied_height, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4fd85612056f"
VERSION = "1.1.0"
TASK_ID = "4fd85612056f"

SUMMARY = "The unique tallest component is cropped out by its bounding box."

INVARIANTS = [
    "background is 0",
    "components are separated by background",
    "one component has a strictly greatest bbox height",
    "output is the tight crop of that component",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "tied_height", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 3..5", "valid": "2..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..7"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        target = ctx.draw_int("components", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 16)
        w = ctx.draw_int("grid_w", 15, 20)
        target = ctx.draw_int("components", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 15)
        target = ctx.draw_int("components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    r0 = rng.randint(1, h - 5)
    c0 = rng.randint(1, w - 3)
    tall = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)]
    for dr, dc in tall:
        g[r0 + dr][c0 + dc] = color
    placed = 1
    attempts = 0
    while placed < target and attempts < 500:
        attempts += 1
        rh, rw = rng.choice([(1, 2), (2, 1), (2, 2), (3, 1)])
        rr = rng.randint(0, h - rh)
        cc = rng.randint(0, w - rw)
        if any(g[r][c] != 0 for r in range(max(0, rr - 1), min(h, rr + rh + 1))
               for c in range(max(0, cc - 1), min(w, cc + rw + 1))):
            continue
        cval = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(rr, rr + rh):
            for c in range(cc, cc + rw):
                g[r][c] = cval
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no candidate to crop.
        return g
    if name == "tied_height":
        # Two components with the same maximum bbox height — selection ambiguous.
        for dr, dc in [(0, 0), (1, 0), (2, 0), (3, 0)]:
            g[1 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (2, 0), (3, 0)]:
            g[1 + dr][8 + dc] = 6
        return g
    if name == "single_component":
        # Only one component — rule trivially returns the whole thing.
        for dr, dc in [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)]:
            g[2 + dr][3 + dc] = 5
        return g
    return g
