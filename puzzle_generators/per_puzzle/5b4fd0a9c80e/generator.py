"""Generator for 10b:m64 — stack crops by area.

Rule: components sorted by (size, row, col). Output vstacks their
bbox crops top-aligned (center-aligned), with 1-row gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, single_component, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5b4fd0a9c80e"
VERSION = "1.1.0"
TASK_ID = "5b4fd0a9c80e"

SUMMARY = "3 components in distinct colors with strictly distinct sizes."

INVARIANTS = [
    "background is 0",
    "exactly 3 components in distinct colors",
    "components have strictly distinct cell counts (so the sort is unambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_component", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "scattered_distinct_size_blobs",
                       "valid": "scattered_distinct_size_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
    7: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(60):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample([3, 4, 5, 6, 7], 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    for size, color in zip(sizes, palette):
        _place_or_raise(g, rng, rng.choice(_BY_SIZE[size]), color, f"size-{size}")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has nothing to stack.
        return g
    if name == "single_component":
        # Only 1 component — rule's stack collapses to a single
        # crop; ordering is trivial.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        return g
    if name == "tied_sizes":
        # Two components share the same size — rule's primary
        # sort key (size) ties; (row, col) tie-break decides.
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 4
        for r, c in [(5, 7), (5, 8)]: g[r][c] = 6
        for r, c in [(8, 3), (8, 4), (8, 5)]: g[r][c] = 7
        return g
    return g
