"""Generator for 878187ab.

Rule: scattered cells in 2-3 colors; rule outputs a clipped diamond
from min/max counts.

Combinatorial axes (8): grid_h/w, bg, n_colors, count_skew, palette_kind,
position_bias, anchor_corner, asymmetry_force.
Degenerates: equal_counts, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e9b415370025"
VERSION = "1.1.0"
TASK_ID = "e9b415370025"
SUMMARY = "Scattered cells in 2-3 colors; rule outputs clipped diamond from min/max counts."

INVARIANTS = [
    "bg is the most-common color",
    "2-3 distinct non-bg colors",
    "non-bg colors have distinct counts in [3, 14]",
]

POSITION_BIASES = ("scattered", "clustered", "row_lean", "col_lean")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("equal_counts", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "bg":             {"type": "color", "default": "rng", "valid": "0..9"},
    "n_colors":       {"type": "int", "default": "2", "valid": "2..3"},
    "count_skew":     {"type": "str", "default": "rng",
                       "valid": "small_gap|big_gap|even"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
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
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    bg = ctx.draw_color("bg")
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={bg})
    skew = overrides.get("count_skew",
                         ctx.draw_choice("count_skew",
                                         ["small_gap", "big_gap", "even"]))
    if skew == "small_gap":
        a = rng.randint(3, 5)
        b = a + rng.randint(1, 2)
    elif skew == "big_gap":
        a = rng.randint(3, 4)
        b = rng.randint(7, 8)
    else:
        a = rng.randint(3, 5)
        b = rng.randint(6, 8)
    counts = sorted([a, b])
    g = full_grid(h, w, bg)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    positions = _pick_positions(bias, h, w, rng)
    idx = 0
    for color, cnt in zip(palette, counts):
        for _ in range(cnt):
            if idx >= len(positions):
                break
            r, c = positions[idx]; idx += 1
            g[r][c] = color
    return g


def _pick_positions(bias, h, w, rng):
    if bias == "clustered":
        cr, cc = h // 2, w // 2
        positions = sorted(((r, c) for r in range(h) for c in range(w)),
                            key=lambda x: abs(x[0] - cr) + abs(x[1] - cc))
        positions = positions[:max(1, h * w // 2)]
        rng.shuffle(positions)
        return positions
    if bias == "row_lean":
        r0 = rng.randint(0, h - 1)
        positions = [(r0, c) for c in range(w)]
        positions += [(r, c) for r in range(h) for c in range(w) if r != r0]
        return positions[:h * w]
    if bias == "col_lean":
        c0 = rng.randint(0, w - 1)
        positions = [(r, c0) for r in range(h)]
        positions += [(r, c) for r in range(h) for c in range(w) if c != c0]
        return positions[:h * w]
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    return positions


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "equal_counts":
        for i in range(4):
            g[i][0] = 2
            g[i + 4][0] = 3
        return g
    if name == "single_color":
        for i in range(5):
            g[i][0] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
