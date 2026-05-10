"""Generator for 64a7c07e.

Rule: collect all 8-blobs. Group by overlapping row range. For each
blob, shift cells right by group's bbox width.

Combinatorial axes (8): grid_h/w, blob_h, blob_w, n_blobs,
distractor_color, position_bias, palette_kind, anchor_corner.
Degenerates: no_blob, blob_at_edge, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "c276ddc1b410"
VERSION = "1.1.0"
TASK_ID = "c276ddc1b410"
SUMMARY = "1-2 solid 8-blobs in left half of grid, leaving room to shift right."

INVARIANTS = [
    "1-2 solid 8-blobs in different row ranges",
    "each blob has space to shift right by its width",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blob", "blob_at_edge", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "blob_h":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "blob_w":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_blobs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "distractor_color":{"type": "color", "default": "rng 2..7", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 5, 5, 7
        bh_lo, bh_hi, bw_lo, bw_hi = 2, 2, 2, 2
        nb_lo, nb_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 10, 12
        bh_lo, bh_hi, bw_lo, bw_hi = 2, 4, 2, 4
        nb_lo, nb_hi = 2, 3
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 7, 7, 9
        bh_lo, bh_hi, bw_lo, bw_hi = 2, 3, 2, 3
        nb_lo, nb_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n_blobs = int(overrides.get("n_blobs",
                                ctx.draw_int("n_blobs", nb_lo, nb_hi)))
    n_blobs = max(1, min(3, n_blobs))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed_rows = []
    for _try in range(40):
        if len(placed_rows) >= n_blobs:
            break
        rh = int(overrides.get("blob_h",
                               rng.randint(bh_lo, bh_hi)))
        rw = int(overrides.get("blob_w",
                               rng.randint(bw_lo, bw_hi)))
        if bias == "stacked":
            r0 = rng.randint(0, h - rh) if not placed_rows else min(h - rh, placed_rows[-1] + 2)
        else:
            r0 = rng.randint(0, h - rh)
        c_max = max(0, w // 2 - rw)
        c0 = rng.randint(0, c_max)
        if any(abs(r0 - pr) < rh + 1 for pr in placed_rows):
            continue
        draw_rect(g, r0, c0, rh, rw, 8)
        placed_rows.append(r0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    dcolor = int(overrides.get("distractor_color", rng.choice(pal)))
    for _try in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = dcolor
            break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6]
    elif kind == "cool":
        pool = [5, 7]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7]
    pool = [c for c in pool if c != 8]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_blob":
        g[2][2] = 3
        return g
    if name == "blob_at_edge":
        draw_rect(g, 0, w - 2, 2, 2, 8)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
