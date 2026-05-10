"""Generator for arc_puzzle_bank_21_set11_bundle:medium_k14 — Recolor by aspect ratio.

Rule: paint each obj with 2 if h > w (tall), 3 if w > h (wide),
4 if h == w.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_squares, all_tall, all_wide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "f47990415137"
VERSION = "1.1.0"
TASK_ID = "f47990415137"
SUMMARY = "Several non-touching blobs with varied aspect ratios; recolor tall/wide/square."

INVARIANTS = ["mix of tall, wide, and square-ish blobs (≥1 each)"]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_squares", "all_tall", "all_wide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..9"},
    "position_bias":  {"type": "str", "default": "spread_oriented",
                       "valid": "spread_oriented"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _make_oriented(rng, h, w, used, target_size, orient):
    for _ in range(15):
        blob = grow_blob(rng, h, w, used, target_size)
        if blob is None: return None
        bb = bbox_of(blob)
        bh = bb[2] - bb[0] + 1; bw = bb[3] - bb[1] + 1
        if orient == "tall" and bh > bw: return blob
        if orient == "wide" and bw > bh: return blob
        if orient == "square" and bh == bw: return blob
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = ctx.draw_int("n_blobs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set(); bboxes = []
    plan = ["tall", "wide", "square"] + rng.sample(["tall", "wide", "square"],
                                                    k=max(0, n_blobs - 3))
    for i, orient in enumerate(plan):
        size = rng.randint(3, 6)
        for _ in range(10):
            blob = _make_oriented(rng, h, w, used, size, orient)
            if blob is None: continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            used |= blob; bboxes.append(bb)
            for r, c in blob: g[r][c] = colors[i % len(colors)]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "all_squares":
        # all blobs are squares (h==w) → only the square → 4 branch fires; uniform output
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for (r, c) in [(1, 6), (1, 7), (2, 6), (2, 7)]: g[r][c] = 6
        for (r, c) in [(6, 3), (6, 4), (7, 3), (7, 4)]: g[r][c] = 8
        return g
    if name == "all_tall":
        # all blobs are tall (h>w) → only the tall → 2 branch fires
        for r in range(1, 5): g[r][2] = 4
        for r in range(2, 6): g[r][6] = 6
        for r in range(5, 9): g[r][8] = 3
        return g
    if name == "all_wide":
        # all blobs are wide (w>h) → only the wide → 3 branch fires
        for c in range(1, 5): g[2][c] = 4
        for c in range(3, 7): g[5][c] = 6
        for c in range(2, 6): g[8][c] = 3
        return g
    return g
