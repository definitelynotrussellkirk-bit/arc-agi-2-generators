"""Generator for puzzle d9f24cd1.

Rule: bottom row has color-2 marker columns. Fill upward: every cell
above a 2 becomes 2 (the bottom guide repeats up). For each 5-blocker
above a marker column at row r, replace cells above r with bg, paint
5 at row r itself, and shift the 2 column one step right at row 0..r.

Combinatorial axes (8): grid_w, grid_h, n_markers, n_blockers,
marker_color, blocker_color, anchor_corner, asymmetry_force.
Degenerates: no_markers, all_blockers, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cd818a9d92d1"
VERSION = "1.1.0"
TASK_ID = "cd818a9d92d1"
SUMMARY = "Bottom row guide w/ markers + 5 blockers; rule fills up + bends right."

INVARIANTS = [
    "background is 0",
    "bottom row has >=1 cell of marker color (2)",
    ">=1 5-blocker (gray) sits above a marker column",
    "blockers don't sit on top of bottom row",
]

MARKER_LAYOUTS = ("evenly_spaced", "clustered", "left_heavy",
                  "right_heavy", "scattered")
DEGENERATE_TEXTURES = ("no_markers", "all_blockers", "single_marker")
HELPFUL_TEXTURES = MARKER_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..18"},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "n_blockers":     {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "marker_layout":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MARKER_LAYOUTS)},
    "extra_decoy":    {"type": "color", "default": "rng (≠0,2,5)",
                       "valid": "1..9 (≠2,5)"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for marker_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 11, 16
    else:
        h_lo, h_hi = 7, 11
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w_lo = h_lo + 1
    w_hi = h_hi + 1
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 2, 4)))
    n_markers = max(1, min(6, min(w - 2, n_markers)))
    n_blockers = int(overrides.get("n_blockers",
                                   ctx.draw_int("n_blockers", 1, 3)))
    n_blockers = max(0, min(5, n_blockers))
    layout = (overrides.get("texture") or
              overrides.get("marker_layout")
              or ctx.draw_choice("marker_layout", list(MARKER_LAYOUTS)))
    g = full_grid(h, w, 0)
    marker_cols = _layout_markers(layout, n_markers, w, rng)
    for c in marker_cols:
        g[h - 1][c] = 2
    if w > 8 and rng.random() < 0.5:
        decoy_color = int(overrides.get("extra_decoy",
                                        ctx.draw_color("extra_decoy",
                                                       exclude={0, 2, 5})))
        g[h - 1][w - 1] = decoy_color
    chosen_blockers = rng.sample(marker_cols, min(len(marker_cols),
                                                   n_blockers))
    for c in chosen_blockers:
        if h <= 4:
            r = 1
        else:
            r = rng.randint(2, h - 3)
        g[r][c] = 5
    return g


def _layout_markers(layout, n, w, rng):
    if layout == "evenly_spaced":
        step = max(1, (w - 2) // (n + 1))
        cols = [1 + i * step for i in range(n)]
        return [c for c in cols if c < w - 1][:n]
    if layout == "clustered":
        start = rng.randint(1, max(1, w - n - 2))
        return list(range(start, start + n))
    if layout == "left_heavy":
        return list(range(1, 1 + n))
    if layout == "right_heavy":
        return list(range(max(1, w - n - 1), w - 1))
    candidates = list(range(1, max(2, w - 1)))
    rng.shuffle(candidates)
    return sorted(candidates[:n])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # No 2s on bottom row → rule has no work
        g[h - 1][1] = rng.choice([3, 4, 6, 7, 8, 9])
        return g
    if name == "all_blockers":
        for c in range(1, w - 1):
            g[h - 1][c] = 2
        for c in range(1, w - 1, 2):
            g[h // 2][c] = 5
        return g
    if name == "single_marker":
        g[h - 1][w // 2] = 2
        return g
    return g
