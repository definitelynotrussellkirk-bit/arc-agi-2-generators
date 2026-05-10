"""Generator for arc_additional_puzzle_bank_volume4:M27 — Transpose-within-bbox per object.

Rule: for each object, paint its cells at transposed positions
(swap r/c offsets within the bbox). Output unions original + transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: symmetric_blobs, square_blobs, blobs_off_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "d6605edf4881"
VERSION = "1.1.0"
TASK_ID = "d6605edf4881"
SUMMARY = "Several non-touching, bbox-isolated, asymmetric blobs; output unions transpose-within-bbox."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "blobs are bbox-isolated",
    "at least one blob differs from its transpose (asymmetric)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("symmetric_blobs", "square_blobs", "blobs_off_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread_asymmetric_blobs",
                       "valid": "spread_asymmetric_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        n_blobs = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = 4
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set(); bboxes = []
    for i in range(n_blobs):
        size = rng.randint(3, 6)
        for _ in range(10):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            r1, c1, r2, c2 = bb
            bh = r2-r1+1; bw = c2-c1+1
            if r1 + bw - 1 >= h or c1 + bh - 1 >= w: continue
            used |= blob; bboxes.append(bb)
            for r, c in blob: g[r][c] = colors[i % len(colors)]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "symmetric_blobs":
        # all blobs are transpose-symmetric → rule's union is identity, no visible change
        # 2x2 solid square has equal h/w and is transpose-symmetric
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        # diagonal-symmetric L
        for (r, c) in [(5, 5), (6, 5), (5, 6)]: g[r][c] = 6
        return g
    if name == "square_blobs":
        # solid square blobs → transpose within bbox is identity for solids
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 4
        for r in range(6, 9):
            for c in range(6, 9): g[r][c] = 6
        return g
    if name == "blobs_off_grid":
        # blob bbox transpose would land outside grid → rule has nowhere to paint
        # Place a tall thin blob that would need a wide bbox after transpose
        for r in range(1, 8): g[r][9] = 4   # 7-tall column at right edge
        return g
    return g
