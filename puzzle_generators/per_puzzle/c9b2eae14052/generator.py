"""Generator for arc_puzzle_bank_fourth21:M22 — keep one-border-touching objects.

Rule: keep blobs whose bbox touches exactly 1 grid border (top, bottom,
left, or right). Drop blobs that touch 0 or ≥2 borders.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_interior, all_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "c9b2eae14052"
VERSION = "1.1.0"
TASK_ID = "c9b2eae14052"
SUMMARY = "≥1 single-border blob (kept) + ≥1 zero-border interior blob (dropped)."

INVARIANTS = [
    "background is 0",
    "≥1 blob touching exactly 1 grid border (top/bot/left/right)",
    "≥1 blob touching 0 borders (interior, dropped)",
    "blobs don't overlap or 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_interior", "all_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_and_interior_blobs",
                       "valid": "border_and_interior_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _border_count(cells, h, w):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return ((min(rs) == 0) + (max(rs) == h - 1)
            + (min(cs) == 0) + (max(cs) == w - 1))


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for _ in range(60):
        r0 = rng.choice([0, rng.randint(2, h - 3)])
        c0 = rng.choice([0, rng.randint(2, w - 3)])
        cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=20)
        if cells is None: continue
        if _border_count(cells, h, w) == 1:
            for r, c in cells:
                g[r][c] = palette[0]
            used |= cells
            break
    for _ in range(60):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
        if cells is None: continue
        if _border_count(cells, h, w) == 0:
            for r, c in cells:
                g[r][c] = palette[1]
            used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no blobs to classify.
        return g
    if name == "all_interior":
        # All blobs touch 0 borders — rule's "keep single-border"
        # branch never fires; output empty.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6)]: g[r][c] = 6
        return g
    if name == "all_corner":
        # All blobs touch 2 borders (corners) — rule's "exactly 1
        # border" filter excludes; output empty.
        for r, c in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 4
        for r, c in [(h - 1, w - 1), (h - 1, w - 2), (h - 2, w - 1)]: g[r][c] = 6
        return g
    return g
