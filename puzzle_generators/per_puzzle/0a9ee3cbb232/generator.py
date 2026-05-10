"""Generator for puzzle 5289ad53.

Rule: count horizontal segments of color 3 (n3) and color 2 (n2).
Output a 2x3 grid with 3s first (n3 cells), then 2s (n2 cells), in
row-major order; rest is 0.

Combinatorial axes (8): grid_h/w, n_3_segs, n_2_segs, seg_min_len,
seg_max_len, position_bias, palette_size, asymmetry_force.
Degenerates: no_segs, all_3_no_2, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a9ee3cbb232"
VERSION = "1.1.0"
TASK_ID = "0a9ee3cbb232"
SUMMARY = "Horizontal segments of 3s and 2s; rule outputs 2x3 with counts."

INVARIANTS = [
    "background is 0",
    "1-6 horizontal segments of 3",
    "1-6 horizontal segments of 2",
    "n_3 + n_2 <= 6 (so 2x3 output isn't overflowed)",
    "segments don't touch (>=1 bg cell between)",
]

POSITION_BIASES = ("scattered", "row_aligned", "top_heavy", "bottom_heavy",
                   "alternating", "clustered")
DEGENERATE_TEXTURES = ("no_segs", "all_3_no_2", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_3_segs":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "n_2_segs":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "seg_min_len":    {"type": "int", "default": "2", "valid": "2..6"},
    "seg_max_len":    {"type": "int", "default": "rng 3..5", "valid": "2..8"},
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
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_3 = int(overrides.get("n_3_segs",
                            ctx.draw_int("n_3_segs", 1, 3)))
    n_2 = int(overrides.get("n_2_segs",
                            ctx.draw_int("n_2_segs", 1, 3)))
    n_3 = max(1, min(6, n_3))
    n_2 = max(1, min(6 - n_3, n_2))
    seg_min = int(overrides.get("seg_min_len", 2))
    seg_max = int(overrides.get("seg_max_len",
                                ctx.draw_int("seg_max_len", 3, 5)))
    seg_min = max(2, min(seg_min, w // 2))
    seg_max = max(seg_min, min(seg_max, w // 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    _place_segs(g, h, w, 3, n_3, seg_min, seg_max, bias, rng)
    _place_segs(g, h, w, 2, n_2, seg_min, seg_max, bias, rng)
    return g


def _place_segs(g, h, w, color, n, seg_min, seg_max, bias, rng):
    placed = 0
    for _ in range(n * 8):
        if placed >= n:
            break
        sl = rng.randint(seg_min, seg_max)
        if sl >= w:
            sl = w - 1
        r = _pick_row(bias, h, placed, rng)
        sc = rng.randint(0, w - sl)
        ec = sc + sl
        if any(g[r][c] != 0 for c in range(max(0, sc - 1),
                                            min(w, ec + 1))):
            continue
        for c in range(sc, ec):
            g[r][c] = color
        placed += 1


def _pick_row(bias, h, idx, rng):
    if bias == "row_aligned":
        return idx * 2 % h
    if bias == "top_heavy":
        return rng.randint(0, max(0, h // 2 - 1))
    if bias == "bottom_heavy":
        return rng.randint(h // 2, h - 1)
    if bias == "alternating":
        return idx * 2 % h
    if bias == "clustered":
        center = h // 2
        return max(0, min(h - 1, center + rng.randint(-2, 2)))
    return rng.randint(0, h - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_segs":
        # No 3 or 2 cells — output all-zero
        return g
    if name == "all_3_no_2":
        for i in range(2):
            r = rng.randint(0, h - 1)
            sc = rng.randint(0, max(0, w - 4))
            for c in range(sc, sc + 3):
                if c < w and g[r][c] == 0:
                    g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 2
        return g
    return g
