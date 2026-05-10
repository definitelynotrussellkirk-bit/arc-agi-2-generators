"""Generator for 868de0fa.

Rule: hollow frames; rule fills interior with 7 if interior width is
odd, else 2.

Combinatorial axes (8): grid_h/w, n_frames, frame_h, frame_w,
position_bias, palette_kind, anchor_corner, asymmetry_force.
Degenerates: solid_block, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "c09f9e692978"
VERSION = "1.1.0"
TASK_ID = "c09f9e692978"
SUMMARY = "Hollow frames; rule fills interior with 7 (odd width) or 2 (even width)."

INVARIANTS = [
    "background is 0",
    ">=1 hollow rectangular frames",
    "frames have interior >= 1x1",
    "frames non-overlapping with bg margin",
]

POSITION_BIASES = ("scattered", "row_aligned", "stacked", "corners")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("solid_block", "no_frame", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "frame_h":        {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "frame_w":        {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
        nf_lo, nf_hi = 1, 1
        fh_lo, fh_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
        nf_lo, nf_hi = 2, 4
        fh_lo, fh_hi = 4, 8
    else:
        h_lo, h_hi = 14, 18
        nf_lo, nf_hi = 1, 3
        fh_lo, fh_hi = 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    g = full_grid(h, w, 0)
    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", nf_lo, nf_hi)))
    n_frames = max(1, min(4, n_frames))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed = []
    for _try in range(60):
        if len(placed) >= n_frames:
            break
        fh = int(overrides.get("frame_h",
                               rng.randint(fh_lo, fh_hi)))
        fw = int(overrides.get("frame_w",
                               rng.randint(fh_lo, fh_hi)))
        rr, rc = _pick_pos(bias, h, w, fh, fw, len(placed), placed, rng)
        ok = True
        for r in range(max(0, rr - 1), min(h, rr + fh + 1)):
            for c in range(max(0, rc - 1), min(w, rc + fw + 1)):
                if g[r][c] != 0:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        color = rng.choice(palette)
        draw_rect_outline(g, rr, rc, fh, fw, color)
        placed.append((rr, rc, fh, fw))
    if not placed:
        return _draw_from_degenerate("no_frame", rng)
    return g


def _pick_pos(bias, h, w, fh, fw, idx, placed, rng):
    max_r = max(0, h - fh)
    max_c = max(0, w - fw)
    if bias == "stacked":
        rr = idx * (fh + 2) + 1
        rc = rng.randint(0, max_c)
    elif bias == "row_aligned":
        rr = max(0, h // 3)
        rc = idx * (fw + 2) + 1
    elif bias == "corners":
        positions = [(0, 0), (0, max_c), (max_r, 0), (max_r, max_c)]
        rr, rc = positions[idx % 4]
    else:
        rr = rng.randint(0, max_r)
        rc = rng.randint(0, max_c)
    rr = max(0, min(rr, max_r))
    rc = max(0, min(rc, max_c))
    return rr, rc


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c not in (0, 2, 7)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "solid_block":
        for r in range(3, 7):
            for c in range(3, 7):
                g[r][c] = 4
        return g
    if name == "no_frame":
        g[5][5] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
