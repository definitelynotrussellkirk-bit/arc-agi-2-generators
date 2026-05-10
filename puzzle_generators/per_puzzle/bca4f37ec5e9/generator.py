"""Generator for puzzle 8eb1be9a.

Rule: horizontal band of non-bg rows; rule tiles the band vertically.

Combinatorial axes (8): grid_h/w, band_h, band_color, band_pattern_kind,
position_bias, palette_size, anchor_corner, asymmetry_force.
Degenerates: no_band, full_grid_band, single_row_band.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bca4f37ec5e9"
VERSION = "1.1.0"
TASK_ID = "bca4f37ec5e9"
SUMMARY = "Band of non-bg rows; rule tiles vertically."

INVARIANTS = [
    "background is 0",
    "exactly one contiguous block of non-bg rows (the band)",
    "band preceded by >=1 all-zero row",
    "band followed by >=1 all-zero row",
    "band has 2-5 rows, each with >=1 non-bg cell",
]

BAND_PATTERNS = ("alternating", "full", "two_thirds", "halves",
                 "stripes", "diag", "checker")
DEGENERATE_TEXTURES = ("no_band", "full_grid_band", "single_row_band")
HELPFUL_TEXTURES = BAND_PATTERNS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..16", "valid": "8..20"},
    "grid_w":            {"type": "int", "default": "rng 9..16", "valid": "6..20"},
    "band_h":            {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "band_color":        {"type": "color", "default": "rng (≠0)",
                          "valid": "1..9"},
    "band_pattern_kind": {"type": "str", "default": "rng helpful",
                          "valid": "|".join(BAND_PATTERNS)},
    "position_bias":     {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "palette_size":      {"type": "int", "default": "1", "valid": "1..3"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for band_pattern_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 15, 20
    else:
        h_lo, h_hi = 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("band")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    band_h = int(overrides.get("band_h",
                               ctx.draw_int("band_h", 2, 4)))
    band_h = max(2, min(min(6, h - 2), band_h))
    color = int(overrides.get("band_color",
                              ctx.draw_color("band_color", exclude={0})))
    pattern_kind = (overrides.get("texture") or
                    overrides.get("band_pattern_kind")
                    or ctx.draw_choice("band_pattern_kind",
                                       list(BAND_PATTERNS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    if bias == "center":
        band_start = (h - band_h) // 2
    elif bias == "edge":
        band_start = 1
    else:
        band_start = rng.randint(1, h - band_h - 1)
    band_start = max(1, min(h - band_h - 1, band_start))
    g = full_grid(h, w, 0)
    for i in range(band_h):
        for c in range(w):
            if _pattern_matches(pattern_kind, i, c, w):
                g[band_start + i][c] = color
    if not any(g[band_start + i][c] != 0
               for i in range(band_h) for c in range(w)):
        for c in range(0, w, 2):
            g[band_start][c] = color
    return g


def _pattern_matches(kind, r, c, w):
    if kind == "alternating":
        return c % 2 == 0
    if kind == "full":
        return True
    if kind == "two_thirds":
        return c % 3 != 0
    if kind == "halves":
        return c < w // 2
    if kind == "stripes":
        return c % 2 == r % 2
    if kind == "diag":
        return c == r
    if kind == "checker":
        return (r + c) % 2 == 0
    return c % 2 == 0


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_band":
        return g
    if name == "full_grid_band":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_row_band":
        for c in range(0, w, 2):
            g[h // 2][c] = color
        return g
    return g
