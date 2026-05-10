"""Generator for puzzle 8fff9e47.

Rule: map row-major 2×2 input blocks to concentric output rings.
Output dim n = 2*rings where rings = h*w/4.

Combinatorial axes (8): grid_size_kind, palette_kind, palette_size,
block_color_distribution, anchor_corner, asymmetry_force,
distinct_blocks, ring_order_kind.
Degenerates: monochrome, two_colors, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "84def340ce03"
VERSION = "1.1.0"
TASK_ID = "84def340ce03"
SUMMARY = "Even-dim 2×2 blocks; rule maps blocks to concentric output rings."

INVARIANTS = [
    "input dims even with h*w in {16, 24, 32, 36, 40, 48}",
    "each 2×2 block is uniform color",
    "different blocks use different colors so concentric rings are distinguishable",
    "2*rings <= 30 (output fits)",
]

GRID_SIZES = ((4, 4), (4, 6), (6, 4), (6, 6), (4, 8), (8, 4))
PALETTE_KINDS = ("warm", "cool", "broad", "small")
RING_ORDER_KINDS = ("default", "shuffled", "ascending", "descending")
DEGENERATE_TEXTURES = ("monochrome", "two_colors", "all_distinct")
HELPFUL_TEXTURES = RING_ORDER_KINDS

AXES = {
    "grid_size_kind":     {"type": "str", "default": "rng 16|24|36",
                           "valid": "16|24|32|36|40|48"},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "ring_order_kind":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(RING_ORDER_KINDS)},
    "palette_size":       {"type": "int", "default": "= rings",
                           "valid": "1..9"},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "distinct_blocks":    {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "block_color_distribution": {"type": "str", "default": "rng even|skewed",
                                 "valid": "even|skewed"},
    "texture":            {"type": "str", "default": "alias for ring_order_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        size_choices = [(4, 4), (4, 6), (6, 4)]
    elif difficulty == "hard":
        size_choices = [(6, 6), (4, 8), (8, 4)]
    else:
        size_choices = list(GRID_SIZES)
    rng = ctx.draw_rng("dims")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        h, w = rng.choice(size_choices)
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    h, w = rng.choice(size_choices)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = list(range(1, 10))
    rng.shuffle(pool)
    rings = h * w // 4
    if len(pool) < rings:
        extras = [c for c in range(1, 10) if c not in pool]
        rng.shuffle(extras)
        pool += extras
    palette = pool[:rings]
    ring_order = (overrides.get("texture") or
                  overrides.get("ring_order_kind")
                  or ctx.draw_choice("ring_order_kind",
                                     list(RING_ORDER_KINDS)))
    if ring_order == "shuffled":
        rng.shuffle(palette)
    elif ring_order == "ascending":
        palette.sort()
    elif ring_order == "descending":
        palette.sort(reverse=True)
    g = full_grid(h, w, 0)
    block_idx = 0
    for br in range(0, h, 2):
        for bc in range(0, w, 2):
            color = palette[block_idx % len(palette)]
            for dr in range(2):
                for dc in range(2):
                    g[br + dr][bc + dc] = color
            block_idx += 1
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    if name == "monochrome":
        c = palette[0]
        for r in range(h):
            for cc in range(w):
                g[r][cc] = c
        return g
    if name == "two_colors":
        c1, c2 = palette[0], palette[1]
        block_idx = 0
        for br in range(0, h, 2):
            for bc in range(0, w, 2):
                color = c1 if block_idx % 2 == 0 else c2
                for dr in range(2):
                    for dc in range(2):
                        g[br + dr][bc + dc] = color
                block_idx += 1
        return g
    if name == "all_distinct":
        block_idx = 0
        for br in range(0, h, 2):
            for bc in range(0, w, 2):
                color = palette[block_idx % len(palette)]
                for dr in range(2):
                    for dc in range(2):
                        g[br + dr][bc + dc] = color
                block_idx += 1
        return g
    return g
