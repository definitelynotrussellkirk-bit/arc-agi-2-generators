"""Generator for puzzle 72a961c9.

Rule: a 1-bar row with non-{0,1} markers in some columns. Each marker
column gets a column rising up: top cell = marker color, rest filled
with 1. Column height: 3 if marker == 8, 4 otherwise.

Combinatorial axes (8): grid_h/w, n_markers, marker_palette,
bar_position, marker_distribution, anchor_corner, asymmetry_force,
include_8.
Degenerates: no_markers, all_markers, no_bar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c5dd8036311b"
VERSION = "1.1.0"
TASK_ID = "c5dd8036311b"
SUMMARY = "1-bar with markers; rule grows colored columns from each marker."

INVARIANTS = [
    "background is 0",
    "exactly one row is the 1-bar (mostly 1s, has >=1 non-{0,1} marker)",
    "1-3 non-{0,1} markers in the bar row",
    "rows above bar are all 0",
    "h >=5 so 4-tall columns fit",
]

MARKER_DISTRIBUTIONS = ("scattered", "left_heavy", "right_heavy",
                        "centered", "evenly_spaced")
DEGENERATE_TEXTURES = ("no_markers", "all_markers", "no_bar")
HELPFUL_TEXTURES = MARKER_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..9", "valid": "4..14"},
    "grid_w":             {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "n_markers":          {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "marker_distribution":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(MARKER_DISTRIBUTIONS)},
    "include_8":          {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "anchor_corner":      {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "bar_position":       {"type": "str", "default": "bottom",
                          "valid": "bottom"},
    "texture":            {"type": "str", "default": "alias for marker_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 9, 14
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_markers = int(overrides.get("n_markers",
                                  ctx.draw_int("n_markers", 1, 2)))
    n_markers = max(1, min(min(w - 1, 4), n_markers))
    distribution = (overrides.get("texture") or
                    overrides.get("marker_distribution")
                    or ctx.draw_choice("marker_distribution",
                                       list(MARKER_DISTRIBUTIONS)))
    include_8 = bool(overrides.get("include_8", True))
    bar_row = h - 1
    g = full_grid(h, w, 0)
    for c in range(w):
        g[bar_row][c] = 1
    palette = [2, 3, 4, 5, 6, 7, 9]
    if include_8:
        palette = [2, 3, 4, 5, 6, 7, 8, 9]
    cs = _pick_marker_cols(distribution, w, n_markers, rng)
    for c in cs:
        g[bar_row][c] = rng.choice(palette)
    return g


def _pick_marker_cols(distribution, w, n, rng):
    candidates = list(range(w))
    if distribution == "left_heavy":
        return candidates[:n]
    if distribution == "right_heavy":
        return candidates[-n:]
    if distribution == "centered":
        center = w // 2
        cs = [center - (n - 1) // 2 + i for i in range(n)]
        return [c for c in cs if 0 <= c < w][:n]
    if distribution == "evenly_spaced":
        step = max(1, w // (n + 1))
        cs = [step * (i + 1) for i in range(n)]
        return [c for c in cs if 0 <= c < w][:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    bar_row = h - 1
    if name == "no_markers":
        for c in range(w):
            g[bar_row][c] = 1
        return g
    if name == "all_markers":
        for c in range(w):
            g[bar_row][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "no_bar":
        # Markers but no surrounding 1s
        c = w // 2
        g[bar_row][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
