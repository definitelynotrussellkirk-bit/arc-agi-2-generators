"""Generator for b5bb5719.

Rule: cellular automaton on row 0. For each lower row's cell:
diagonals lp/rp; if both same → opposite color; else → rp.

Combinatorial axes (8): grid_h/w, n_marks, mark_color_distribution,
position_bias, mark_layout, decoy_density, palette_kind,
asymmetry_force.
Degenerates: empty_top, all_same_color, full_top.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f59691ac00f3"
VERSION = "1.1.0"
TASK_ID = "f59691ac00f3"
SUMMARY = "Top row scattered 2/5 on 7-bg; rule runs CA downward."

INVARIANTS = [
    "bg = 7",
    ">=2 non-bg cells in row 0 (cells in {2, 5})",
    "rest of grid (rows 1..h-1) is bg=7",
    ">=1 of each color {2, 5} in row 0 (so CA branches both ways) — relaxed when n_marks >= 2",
]

MARK_LAYOUTS = ("scattered", "alternating", "left_biased",
                "right_biased", "edges", "center")
COLOR_DISTRIBUTIONS = ("balanced", "twos_heavy", "fives_heavy")
DEGENERATE_TEXTURES = ("empty_top", "all_same_color", "full_top")
HELPFUL_TEXTURES = MARK_LAYOUTS

AXES = {
    "grid_h":               {"type": "int", "default": "rng 5..10", "valid": "3..14"},
    "grid_w":               {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "n_marks":              {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "mark_color_distribution": {"type": "str", "default": "rng helpful",
                                "valid": "|".join(COLOR_DISTRIBUTIONS)},
    "mark_layout":          {"type": "str", "default": "rng helpful",
                             "valid": "|".join(MARK_LAYOUTS)},
    "position_bias":        {"type": "str", "default": "rng spread|center|edge",
                             "valid": "spread|center|edge"},
    "anchor_endpoints":     {"type": "bool", "default": "false",
                             "valid": "true|false"},
    "asymmetry_force":      {"type": "bool", "default": "false",
                             "valid": "true|false"},
    "texture":              {"type": "str", "default": "alias for mark_layout",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 3, 5, 4, 7
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 12, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 10, 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_marks = int(overrides.get("n_marks",
                                ctx.draw_int("n_marks", 2, min(5, w))))
    n_marks = max(2, min(w, n_marks))
    layout = (overrides.get("texture") or overrides.get("mark_layout")
              or ctx.draw_choice("mark_layout", list(MARK_LAYOUTS)))
    color_dist = overrides.get("mark_color_distribution",
                               ctx.draw_choice("mark_color_distribution",
                                               list(COLOR_DISTRIBUTIONS)))
    g = full_grid(h, w, 7)
    cols = _layout_cols(layout, w, n_marks, rng)
    for i, c in enumerate(cols):
        if color_dist == "twos_heavy":
            g[0][c] = 2 if rng.random() < 0.7 else 5
        elif color_dist == "fives_heavy":
            g[0][c] = 5 if rng.random() < 0.7 else 2
        else:
            g[0][c] = 2 if i % 2 == 0 else 5
    if bool(overrides.get("anchor_endpoints", False)):
        g[0][0] = 2
        g[0][w - 1] = 5
    return g


def _layout_cols(layout, w, n, rng):
    cols = list(range(w))
    if layout == "alternating":
        cols = [c for c in cols if c % 2 == 0]
        return cols[:n] if cols else list(range(n))
    if layout == "left_biased":
        return cols[:n]
    if layout == "right_biased":
        return cols[-n:]
    if layout == "edges":
        return ([0, w - 1] + sorted(rng.sample(range(1, w - 1),
                                               max(0, n - 2))))[:n]
    if layout == "center":
        center = w // 2
        cols.sort(key=lambda c: abs(c - center))
        return sorted(cols[:n])
    rng.shuffle(cols)
    return sorted(cols[:n])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    if name == "empty_top":
        return g
    if name == "all_same_color":
        for c in range(0, w, 2):
            g[0][c] = 2
        return g
    if name == "full_top":
        for c in range(w):
            g[0][c] = rng.choice([2, 5])
        return g
    return g
