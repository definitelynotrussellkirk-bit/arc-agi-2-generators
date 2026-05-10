"""Generator for arc_puzzle_bank_21_set19_bundle:easy_p05.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ring_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rings, filled_rings, broken_rings.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f813212d1e20"
VERSION = "1.1.0"
TASK_ID = "f813212d1e20"
SUMMARY = "Separated hollow 3x3 monochrome rings have zero centers to fill."

INVARIANTS = [
    "background is 0",
    "each ring is a complete 3x3 border with a zero center",
    "rings do not overlap or touch, avoiding accidental mixed windows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rings", "filled_rings", "broken_rings")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ring_count":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "complete_3x3_rings_with_zero_centers",
                       "valid": "complete_3x3_rings_with_zero_centers"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_for_ring(grid, r0, c0):
    h = len(grid)
    w = len(grid[0])
    for r in range(max(0, r0 - 1), min(h, r0 + 4)):
        for c in range(max(0, c0 - 1), min(w, c0 + 4)):
            if grid[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        ring_count = ctx.draw_int("ring_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        ring_count = ctx.draw_int("ring_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        ring_count = ctx.draw_int("ring_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)

    positions = [(r, c) for r in range(h - 2) for c in range(w - 2)]
    rng.shuffle(positions)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], ring_count)
    placed = 0
    for r0, c0 in positions:
        if placed >= ring_count:
            break
        if not _clear_for_ring(grid, r0, c0):
            continue
        color = colors[placed]
        for dr in range(3):
            for dc in range(3):
                if dr == 1 and dc == 1:
                    continue
                grid[r0 + dr][c0 + dc] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_rings":
        # blank → no ring centers to fill
        return g
    if name == "filled_rings":
        # 3x3 already solid (center filled too) → fill rule is identity
        for dr in range(3):
            for dc in range(3):
                g[1 + dr][1 + dc] = 4
                g[5 + dr][6 + dc] = 6
        return g
    if name == "broken_rings":
        # ring with one border cell missing → not a closed ring, no enclosed center
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[1 + dr][1 + dc] = 4
        # right side at (1, 2) intentionally missing
        return g
    return g
