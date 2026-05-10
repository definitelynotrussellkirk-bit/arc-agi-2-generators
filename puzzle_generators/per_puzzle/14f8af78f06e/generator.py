"""Generator for arc_puzzle_bank_21_set8_s:S8_H7.

Rule: top-left periodic seed tile fills an irregular color-8 mask elsewhere.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_mask, mask_inside_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "14f8af78f06e"
VERSION = "1.1.0"
TASK_ID = "14f8af78f06e"
SUMMARY = "Fill an irregular 8-mask from the top-left periodic seed tile."

INVARIANTS = [
    "the seed tile starts at the top-left corner and is entirely nonzero",
    "row 0 and column 0 terminate the seed with zeros after the tile",
    "the mask uses color 8 and does not overlap the seed tile",
    "mask cells are filled by the seed tile modulo the mask bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_mask", "mask_inside_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "6..16"},
    "tile_h":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "tile_w":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..9", "valid": "4..9"},
    "position_bias":  {"type": "str", "default": "seed_at_corner_with_mask",
                       "valid": "seed_at_corner_with_mask"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..9", "valid": "4..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MASKS = [
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1), (2, 2), (3, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (3, 0), (3, 1)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 2), (3, 1), (3, 2)],
]


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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        tile_h = ctx.draw_int("tile_h", 2, 2)
        tile_w = ctx.draw_int("tile_w", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 15)
        tile_h = ctx.draw_int("tile_h", 3, 4)
        tile_w = ctx.draw_int("tile_w", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        tile_h = ctx.draw_int("tile_h", 2, 3)
        tile_w = ctx.draw_int("tile_w", 2, 3)
    pool = [1, 2, 3, 4, 5, 6, 7, 9]
    n_colors = min(tile_h * tile_w, len(pool))
    colors = rng.sample(pool, n_colors)
    while len(colors) < tile_h * tile_w:
        colors.append(rng.choice(pool))
    mask = _MASKS[ctx.draw_int("mask_shape", 0, len(_MASKS) - 1)]
    max_dr = max(r for r, _ in mask)
    max_dc = max(c for _, c in mask)

    g = full_grid(h, w, 0)
    i = 0
    for r in range(tile_h):
        for c in range(tile_w):
            g[r][c] = colors[i]
            i += 1

    top = rng.randint(tile_h + 2, h - max_dr - 1)
    left = rng.randint(tile_w + 2, w - max_dc - 1)
    for dr, dc in mask:
        g[top + dr][left + dc] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # Mask present but no seed tile — rule's "fill from seed"
        # has no source data; output undefined.
        for r, c in [(4, 5), (4, 6), (5, 5), (6, 5)]: g[r][c] = 8
        return g
    if name == "no_mask":
        # Seed tile but no 8-mask — rule has no targets to fill.
        g[0][0] = 1; g[0][1] = 2
        g[1][0] = 3; g[1][1] = 4
        return g
    if name == "mask_inside_seed":
        # 8-mask placed where it overlaps the seed cells — rule's
        # "no overlap" precondition is violated.
        g[0][0] = 1; g[0][1] = 2
        g[1][0] = 3; g[1][1] = 4
        g[0][0] = 8
        return g
    return g
