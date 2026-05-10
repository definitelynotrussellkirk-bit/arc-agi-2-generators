"""Generator for c909285e.

Rule: input has one hollow rectangular frame (outline only). Output
crops to the frame's bbox.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, position_bias,
palette_kind, n_inner, anchor_corner, asymmetry_force.
Degenerates: no_frame, two_frames, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "4977f1fc4c50"
VERSION = "1.1.0"
TASK_ID = "4977f1fc4c50"
SUMMARY = "Hollow rectangular frame; rule crops to its bbox."

INVARIANTS = [
    "background is 0",
    "exactly one color forms a perimeter-only rectangular frame, bbox >= 3x3",
    "no other color forms a perimeter-only frame >= 3x3",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "two_frames", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "frame_h":        {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "frame_w":        {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_inner":        {"type": "int", "default": "rng 2..4", "valid": "0..6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
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
        h_lo, h_hi = 10, 12
        f_lo, f_hi = 4, 5
        ni_lo, ni_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        f_lo, f_hi = 6, 9
        ni_lo, ni_hi = 3, 6
    else:
        h_lo, h_hi = 12, 16
        f_lo, f_hi = 5, 8
        ni_lo, ni_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    frame_color = palette[0]
    inner_palette = palette[1:]
    g = full_grid(h, w, 0)
    fh = int(overrides.get("frame_h",
                           ctx.draw_int("frame_h", f_lo, min(f_hi, h - 2))))
    fw = int(overrides.get("frame_w",
                           ctx.draw_int("frame_w", f_lo, min(f_hi, w - 2))))
    fh = max(4, min(fh, h - 2))
    fw = max(4, min(fw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    rr, rc = _pick_frame_pos(bias, h, w, fh, fw, rng)
    draw_rect_outline(g, rr, rc, fh, fw, frame_color)
    n_inner = int(overrides.get("n_inner",
                                ctx.draw_int("n_inner", ni_lo, ni_hi)))
    n_inner = max(0, min(6, n_inner))
    for _ in range(n_inner):
        ir = rng.randint(rr + 1, rr + fh - 2)
        ic = rng.randint(rc + 1, rc + fw - 2)
        if inner_palette:
            g[ir][ic] = rng.choice(inner_palette)
    return g


def _pick_frame_pos(bias, h, w, fh, fw, rng):
    max_r = max(1, h - fh - 1)
    max_c = max(1, w - fw - 1)
    if bias == "centered":
        rr = max(1, (h - fh) // 2 + rng.randint(-1, 1))
        rc = max(1, (w - fw) // 2 + rng.randint(-1, 1))
    elif bias == "corner":
        rr = rng.choice([1, max_r])
        rc = rng.choice([1, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            rr = rng.choice([1, max_r])
            rc = rng.randint(1, max_c)
        else:
            rr = rng.randint(1, max_r)
            rc = rng.choice([1, max_c])
    else:
        rr = rng.randint(1, max_r)
        rc = rng.randint(1, max_c)
    rr = max(1, min(rr, max_r))
    rc = max(1, min(rc, max_c))
    return rr, rc


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_frame":
        for _ in range(8):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "two_frames":
        draw_rect_outline(g, 1, 1, 5, 5, 2)
        draw_rect_outline(g, 8, 8, 5, 5, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
