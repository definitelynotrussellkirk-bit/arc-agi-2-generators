"""Generator for arc_additional_puzzle_bank_volume5:M35 — Transpose each object locally.

Rule: for each object, replace its cells with the transpose around its
bbox top-left corner: (r, c) → (r1 + (c - c1), c1 + (r - r1)).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_solid_squares, single_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "7071285d78ce"
VERSION = "1.1.0"
TASK_ID = "7071285d78ce"
SUMMARY = "Several non-touching monocolor blobs; output transposes each blob within its own bbox."

INVARIANTS = [
    "between 2 and 3 non-touching blobs",
    "each blob has distinct color",
    "each blob's bbox stays in-bounds after transpose (square bbox or sufficient room)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_solid_squares", "single_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_nonsquare_blobs",
                       "valid": "spaced_nonsquare_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_blobs = ctx.draw_int("n_blobs", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    placed = 0
    for _ in range(n_blobs * 5):
        if placed >= n_blobs: break
        size = rng.randint(3, 5)
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        rs = [r for r, _ in blob]; cs = [c for _, c in blob]
        r1, c1 = min(rs), min(cs); r2, c2 = max(rs), max(cs)
        bh = r2 - r1 + 1; bw = c2 - c1 + 1
        if r1 + bw > h or c1 + bh > w:
            continue
        if len(rs) == bh * bw:
            continue
        used |= blob
        for r, c in blob: g[r][c] = colors[placed]
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no objects to transpose, rule has no effect
        return g
    if name == "all_solid_squares":
        # solid square bboxes → transpose is identity
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(3):
            for c in range(3): g[5 + r][5 + c] = 6
        return g
    if name == "single_cell_blobs":
        # 1x1 cells → transpose is identity
        g[1][2] = 4
        g[5][7] = 6
        g[8][3] = 3
        return g
    return g
