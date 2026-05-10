"""Generator for e7a25a18.

Rule: 2-frame containing small key; output is frame with key upscaled.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_frame, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "5da2f80a4a4f"
VERSION = "1.1.0"
TASK_ID = "5da2f80a4a4f"
SUMMARY = "2-frame at center with 2x2 of distinct colors at top-left of interior."

INVARIANTS = [
    "single 2-frame outline of size 6x6 placed in the grid",
    "interior top-left corner has a 2x2 of distinct non-zero colors",
    "interior dimensions divide evenly by the key's dimensions",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_key", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "frame_h":        {"type": "int", "default": "6", "valid": "4..8"},
    "frame_w":        {"type": "int", "default": "6", "valid": "4..8"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 15, 18
    else:
        h_lo, h_hi = 12, 15
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    fh = int(overrides.get("frame_h", 6))
    fw = int(overrides.get("frame_w", 6))
    fh = max(4, min(fh, h - 2))
    fw = max(4, min(fw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    max_r = max(1, h - fh - 1)
    max_c = max(1, w - fw - 1)
    if bias == "centered":
        r0 = max(1, (h - fh) // 2)
        c0 = max(1, (w - fw) // 2)
    elif bias == "corner":
        r0 = rng.choice([1, max_r])
        c0 = rng.choice([1, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([1, max_r])
            c0 = rng.randint(1, max_c)
        else:
            r0 = rng.randint(1, max_r)
            c0 = rng.choice([1, max_c])
    else:
        r0 = rng.randint(1, max_r)
        c0 = rng.randint(1, max_c)
    draw_rect_outline(g, r0, c0, fh, fw, 2)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    if r0 + 2 < h and c0 + 2 < w:
        g[r0 + 1][c0 + 1] = palette[0]
        g[r0 + 1][c0 + 2] = palette[1]
        g[r0 + 2][c0 + 1] = palette[2]
        g[r0 + 2][c0 + 2] = palette[3]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 2)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool and c != 2:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_frame":
        g[5][5] = 3; g[5][6] = 4; g[6][5] = 5; g[6][6] = 6
        return g
    if name == "no_key":
        draw_rect_outline(g, 3, 3, 6, 6, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
