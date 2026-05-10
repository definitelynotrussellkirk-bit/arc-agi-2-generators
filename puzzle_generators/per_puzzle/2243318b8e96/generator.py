"""Generator for arc_additional_puzzle_bank_volume3:M17 — Recolor objects by parity of size.

Rule: paint each object's cells with 3 if obj-size is odd, 8 if even.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_odd_sizes, all_even_sizes, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2243318b8e96"
VERSION = "1.1.0"
TASK_ID = "2243318b8e96"
SUMMARY = "Several non-touching colored blobs of varied sizes; output recolors by size parity."

INVARIANTS = [
    "between 3 and 5 non-touching blobs",
    "blob sizes include at least one odd and at least one even",
    "blobs use distinct non-bg colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_odd_sizes", "all_even_sizes", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _has_neighbor(p, used, ignore=frozenset()):
    r, c = p
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if (nr, nc) in ignore: continue
        if (nr, nc) in used: return True
    return False


def _grow_blob(rng, h, w, used, target_size):
    for _ in range(50):
        seed = (rng.randint(0, h-1), rng.randint(0, w-1))
        if seed in used or _has_neighbor(seed, used): continue
        cells = {seed}
        frontier = [seed]
        while frontier and len(cells) < target_size:
            r, c = frontier.pop(rng.randint(0, len(frontier)-1))
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                if not (0 <= nr < h and 0 <= nc < w): continue
                cand = (nr, nc)
                if cand in cells or cand in used: continue
                if _has_neighbor(cand, used, ignore=cells): continue
                cells.add(cand)
                frontier.append(cand)
                if len(cells) == target_size: break
        if len(cells) == target_size:
            return cells
    return None


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_blobs = ctx.draw_int("n_blobs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_blobs = ctx.draw_int("n_blobs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 5)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = [1, 2, 3, 4, 5]
    rng.shuffle(sizes)
    sizes = sizes[:n_blobs]
    if all(s % 2 == 0 for s in sizes): sizes[0] = 3
    if all(s % 2 == 1 for s in sizes): sizes[0] = 4

    colors = [c for c in range(1, 10)]
    rng.shuffle(colors)

    used: set[tuple[int,int]] = set()
    for i, size in enumerate(sizes):
        blob = _grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        color = colors[i % len(colors)]
        for r, c in blob: g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 10, 10
    g = full_grid(h, w, 0)
    used: set[tuple[int,int]] = set()
    if name == "all_odd_sizes":
        # every blob has odd size → output is monochrome 3, parity rule has no contrast
        for size, color in [(1, 4), (3, 5), (5, 6)]:
            blob = _grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
        return g
    if name == "all_even_sizes":
        # every blob has even size → output is monochrome 8, parity rule has no contrast
        for size, color in [(2, 4), (4, 5), (6, 6)]:
            blob = _grow_blob(rng, h, w, used, size)
            if blob is None: continue
            used |= blob
            for r, c in blob: g[r][c] = color
        return g
    if name == "no_blobs":
        # empty grid → no objects to recolor, rule no-op
        return g
    return g
