"""Generator for puzzle 7ee1c6ea.

Rule: gray(5) frame with 2 distinct non-bg colors inside; swap them.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, palette_kind,
fill_ratio, position_bias, anchor_corner, asymmetry_force.
Degenerates: single_color_inside, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "51e59bb53cac"
VERSION = "1.1.0"
TASK_ID = "51e59bb53cac"
SUMMARY = "Gray frame w/ 2 colors inside; rule swaps them."

INVARIANTS = [
    "background is 0",
    "exactly 1 rectangular gray(5) frame",
    "frame >=5x5 (interior >=3x3)",
    "interior has exactly 2 distinct non-{0,5} colors",
]

POSITION_BIASES = ("scattered", "centered", "corner", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_color_inside", "no_frame", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "frame_h":        {"type": "int", "default": "rng 5..h-3", "valid": "5..h-1"},
    "frame_w":        {"type": "int", "default": "rng 5..w-3", "valid": "5..w-1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "fill_ratio":     {"type": "float", "default": "rng 0.4..0.8",
                       "valid": "0.2..0.95"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng_pos = ctx.draw_rng("frame_pos")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng_pos)
    fh = int(overrides.get("frame_h",
                           ctx.draw_int("frame_h", 5, max(5, h - 3))))
    fw = int(overrides.get("frame_w",
                           ctx.draw_int("frame_w", 5, max(5, w - 3))))
    fh = max(5, min(h - 2, fh))
    fw = max(5, min(w - 2, fw))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    in_colors = _build_palette(palette_kind, 2, rng_pos)
    rng_ratio = ctx.draw_rng("fill_ratio")
    ratio = float(overrides.get("fill_ratio",
                                rng_ratio.uniform(0.4, 0.8)))
    rr, rc = _pick_position(bias, h, w, fh, fw, rng_pos)
    g = full_grid(h, w, 0)
    draw_rect_outline(g, rr, rc, fh, fw, 5)
    interior_cells = [(rr + dr, rc + dc)
                      for dr in range(1, fh - 1)
                      for dc in range(1, fw - 1)]
    rng = ctx.draw_rng("interior")
    rng.shuffle(interior_cells)
    n_paint = max(2, int(len(interior_cells) * ratio))
    for i, (r, c) in enumerate(interior_cells[:n_paint]):
        if i == 0:
            g[r][c] = in_colors[0]
        elif i == 1:
            g[r][c] = in_colors[1]
        else:
            g[r][c] = rng.choice(in_colors)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c != 5]
    rng.shuffle(pool)
    return pool[:n]


def _pick_position(bias, h, w, fh, fw, rng):
    if bias == "centered":
        return max(1, (h - fh) // 2), max(1, (w - fw) // 2)
    if bias == "corner":
        return rng.choice([(1, 1), (1, w - fw - 1),
                           (h - fh - 1, 1),
                           (h - fh - 1, w - fw - 1)])
    if bias == "spread":
        return rng.randint(1, h - fh - 1), rng.randint(1, w - fw - 1)
    return rng.randint(1, h - fh - 1), rng.randint(1, w - fw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_color_inside":
        draw_rect_outline(g, 1, 1, 6, 6, 5)
        for r in range(2, 6):
            for c in range(2, 6):
                if rng.random() < 0.6:
                    g[r][c] = 3
        return g
    if name == "no_frame":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
