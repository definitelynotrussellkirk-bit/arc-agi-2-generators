"""Generator for puzzle 9b30e358.

Rule: bottom band of non-bg rows + all-bg rows above. Rule tiles the
bottom band upward to fill empty space.

Combinatorial axes (8): grid_h/w, band_h, band_color, band_pattern,
palette_size, bg_color, decoy_density, band_density.
Degenerates: no_band, full_band, alternating_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e28d95a116e4"
VERSION = "1.1.0"
TASK_ID = "e28d95a116e4"
SUMMARY = "Bottom band of non-bg rows; rule tiles upward to fill empty space."

INVARIANTS = [
    "bg is most common color (rule uses (mode g -1))",
    "the bottom band of non-bg rows starts at the bottom",
    "above the band is entirely bg",
    "band height >=2 and < grid_h",
]

BAND_PATTERNS = ("even_cols", "odd_cols", "halves", "thirds",
                 "diagonal", "checker", "frame", "scattered")
DEGENERATE_TEXTURES = ("no_band", "full_band", "alternating_rows")
HELPFUL_TEXTURES = BAND_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "band_h":         {"type": "int", "default": "rng 2..5",  "valid": "2..8"},
    "band_color":     {"type": "color", "default": "rng (≠0)",
                       "valid": "1..9"},
    "band_pattern":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(BAND_PATTERNS)},
    "band_density":   {"type": "float", "default": "rng 0.5..0.8",
                       "valid": "0.2..1"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "bg_color":       {"type": "color", "default": "0", "valid": "0..9"},
    "texture":        {"type": "str", "default": "alias for band_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, b_lo, b_hi = 6, 10, 5, 9, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, b_lo, b_hi = 14, 20, 12, 18, 4, 6
    else:
        h_lo, h_hi, w_lo, w_hi, b_lo, b_hi = 8, 16, 8, 14, 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("band")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    band_h = int(overrides.get("band_h", ctx.draw_int("band_h", b_lo, b_hi)))
    band_h = max(2, min(h - 1, band_h))
    band_color = int(overrides.get("band_color",
                                   ctx.draw_color("band_color", exclude={0})))
    n_palette = int(overrides.get("palette_size", 1))
    pool = [c for c in range(1, 10) if c not in (0, band_color)]
    rng.shuffle(pool)
    palette = [band_color] + pool[:max(0, n_palette - 1)]
    pattern = (overrides.get("texture") or overrides.get("band_pattern")
               or ctx.draw_choice("band_pattern", list(BAND_PATTERNS)))
    density = float(overrides.get("band_density",
                                  ctx.draw_rng("band_density")
                                  .uniform(0.5, 0.8)))
    g = full_grid(h, w, 0)
    _fill_band(g, pattern, h, w, band_h, palette, density, rng)
    bg_count = sum(1 for r in range(h) for c in range(w) if g[r][c] == 0)
    band_count = sum(1 for r in range(h - band_h, h) for c in range(w)
                     if g[r][c] != 0)
    if band_count < (band_h * w) // 4:
        for r in range(h - band_h, h):
            g[r][0] = band_color
            g[r][w - 1] = band_color
    return g


def _fill_band(g, pattern, h, w, band_h, palette, density, rng):
    for r in range(h - band_h, h):
        for c in range(w):
            if _band_should_fill(pattern, r - (h - band_h), c, band_h, w, rng, density):
                g[r][c] = rng.choice(palette)


def _band_should_fill(pattern, br, c, band_h, w, rng, density):
    if pattern == "even_cols":
        return c % 2 == 0 and rng.random() < density + 0.2
    if pattern == "odd_cols":
        return c % 2 == 1 and rng.random() < density + 0.2
    if pattern == "halves":
        return c < w // 2
    if pattern == "thirds":
        return c % 3 != 0
    if pattern == "diagonal":
        return c == br or c == band_h - 1 - br
    if pattern == "checker":
        return (br + c) % 2 == 0
    if pattern == "frame":
        return br in (0, band_h - 1) or c in (0, w - 1)
    return rng.random() < density


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_band":
        return g
    if name == "full_band":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "alternating_rows":
        for r in range(h):
            if r % 2 == 0:
                for c in range(w):
                    g[r][c] = color
        return g
    return g
