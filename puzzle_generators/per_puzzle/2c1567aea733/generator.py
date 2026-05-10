"""Generator for puzzle 1caeab9d.

Rule: blue(1) blob's top row defines target. Each non-zero cell shifts
so its color's top moves to the blue's top.

Combinatorial axes (8): grid_h/w, n_blobs, blob_h_min, blob_h_max,
blob_w_min, blob_w_max, palette_kind, position_bias.
Degenerates: no_blue, single_blob, all_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "2c1567aea733"
VERSION = "1.1.0"
TASK_ID = "2c1567aea733"
SUMMARY = "Rectangles of distinct colors w/ 1 blue anchor; rule aligns by blue's top."

INVARIANTS = [
    "background is 0",
    "2-4 solid rectangles of distinct non-bg colors",
    "exactly one rectangle has color 1 (alignment anchor)",
    "rectangles' column-extents are disjoint",
    "blobs don't overlap",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
POSITION_BIASES = ("scattered", "row_aligned", "col_aligned", "diagonal")
DEGENERATE_TEXTURES = ("no_blue", "single_blob", "all_aligned")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "blob_h_min":     {"type": "int", "default": "2", "valid": "1..4"},
    "blob_h_max":     {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "blob_w_min":     {"type": "int", "default": "2", "valid": "1..4"},
    "blob_w_max":     {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_blobs = int(overrides.get("n_blobs",
                                ctx.draw_int("n_blobs", 2, 3)))
    n_blobs = max(2, min(4, n_blobs))
    bh_min = int(overrides.get("blob_h_min", 2))
    bh_max = int(overrides.get("blob_h_max",
                               ctx.draw_int("blob_h_max", 3, 4)))
    bw_min = int(overrides.get("blob_w_min", 2))
    bw_max = int(overrides.get("blob_w_max",
                               ctx.draw_int("blob_w_max", 3, 4)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    other_pal = _build_palette(palette_kind, n_blobs - 1, rng,
                               exclude={1})
    palette = [1] + other_pal
    rng.shuffle(palette)
    g = full_grid(h, w, 0)
    occupied_cols = set()
    for i, color in enumerate(palette):
        bh = rng.randint(bh_min, bh_max)
        bw = rng.randint(bw_min, bw_max)
        for _ in range(40):
            r0, c0 = _pick_position(bias, h, w, bh, bw, i, rng)
            if r0 is None:
                continue
            if any(c in occupied_cols for c in range(c0, c0 + bw)):
                continue
            draw_rect(g, r0, c0, bh, bw, color)
            for c in range(c0, c0 + bw):
                occupied_cols.add(c)
            break
    return g


def _build_palette(kind, n, rng, exclude):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in exclude]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool and c not in exclude:
                pool.append(c)
    return pool[:n]


def _pick_position(bias, h, w, bh, bw, idx, rng):
    if h - bh - 2 < 1 or w - bw - 2 < 1:
        return None, None
    if bias == "row_aligned":
        rr = max(1, (h - bh) // 2)
        rc = 1 + idx * (bw + 1)
        if rc + bw > w - 1:
            rc = rng.randint(1, w - bw - 1)
        return rr, rc
    if bias == "col_aligned":
        rr = 1 + idx * (bh + 1)
        if rr + bh > h - 1:
            rr = rng.randint(1, h - bh - 1)
        return rr, max(1, (w - bw) // 2)
    if bias == "diagonal":
        rr = 1 + idx * 2
        rc = 1 + idx * (bw + 1)
        if rr + bh > h - 1 or rc + bw > w - 1:
            return rng.randint(1, h - bh - 1), rng.randint(1, w - bw - 1)
        return rr, rc
    return rng.randint(1, h - bh - 1), rng.randint(1, w - bw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_blue":
        # Two blobs without any blue
        draw_rect(g, 2, 2, 2, 2, 3)
        draw_rect(g, 3, 6, 2, 2, 4)
        return g
    if name == "single_blob":
        # Just one blue blob
        draw_rect(g, 2, 2, 2, 2, 1)
        return g
    if name == "all_aligned":
        # All blobs already at same row
        draw_rect(g, 2, 1, 2, 2, 1)
        draw_rect(g, 2, 4, 2, 2, 3)
        draw_rect(g, 2, 7, 2, 2, 4)
        return g
    return g
