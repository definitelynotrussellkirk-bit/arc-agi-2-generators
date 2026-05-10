"""Generator for ARC task bd4472b8.

Rule: rows 0..1 keep input. For rows r >= 2: every cell becomes
row-at(g, 0)[(r - 2) mod w]. Effect: rows 2+ become solid bands cycling
through the colors of row 0.

Combinatorial axes: grid_h/w, palette_size, row0_pattern,
row1_decoy_density (rows 1+ are decoy in helpful path),
rows_2plus_decoy_density.
Degenerates: monochrome_row0 (all rows 2+ same color),
all_distinct_row0 (rows 2+ cycle through), single_row0_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f891d1ff5dd8"
VERSION = "1.1.0"
TASK_ID = "f891d1ff5dd8"
SUMMARY = "Top row is a color cycle; rule rewrites rows 2+ to solid bands cycling through it."

INVARIANTS = [
    "h ≥ 3, w ≥ 2",
    "row 0 contains the cycle of colors used for rows 2+",
    "row 1 is decoy (rule passes it through unchanged)",
]

ROW0_PATTERNS = ("all_distinct", "alternating", "blocks", "gradient", "random")
DEGENERATE_TEXTURES = ("monochrome_row0", "single_row0_color", "row0_all_zero")
HELPFUL_TEXTURES = ROW0_PATTERNS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":              {"type": "int", "default": "rng 2..10", "valid": "1..15"},
    "palette_size":        {"type": "int", "default": "rng 2..6", "valid": "1..10"},
    "row0_pattern":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ROW0_PATTERNS)},
    "row1_decoy_density":  {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "row2plus_density":    {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "texture":             {"type": "str", "default": "alias for row0_pattern",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 4, 7, 2, 4, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 11, 14, 7, 10, 5, 8
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 4, 14, 2, 10, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors))
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    pattern = (overrides.get("texture") or overrides.get("row0_pattern")
               or ctx.draw_choice("row0_pattern", list(ROW0_PATTERNS)))
    row1_d = float(overrides.get("row1_decoy_density",
                                 ctx.draw_rng("row1_decoy_density").uniform(0.3, 0.7)))
    row2_d = float(overrides.get("row2plus_density",
                                 ctx.draw_rng("row2plus_density").uniform(0.3, 0.7)))
    g = full_grid(h, w, 0)
    # Row 0 — the cycle.
    if pattern == "all_distinct":
        for c in range(w):
            g[0][c] = palette[c % len(palette)]
    elif pattern == "alternating":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for c in range(w):
            g[0][c] = a if c % 2 == 0 else b
    elif pattern == "blocks":
        block = max(1, w // max(1, len(palette)))
        for c in range(w):
            g[0][c] = palette[(c // block) % len(palette)]
    elif pattern == "gradient":
        for c in range(w):
            g[0][c] = palette[(c * len(palette) // max(1, w)) % len(palette)]
    else:  # random
        for c in range(w):
            g[0][c] = rng.choice(palette)

    # Row 1 — decoy.
    for c in range(w):
        if rng.random() < row1_d:
            g[1][c] = rng.choice(palette)

    # Rows 2+ — decoy (rule overwrites them).
    for r in range(2, h):
        for c in range(w):
            if rng.random() < row2_d:
                g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, 0)
    if name == "monochrome_row0":
        c0 = palette[0]
        for c in range(w):
            g[0][c] = c0
        for r in range(1, h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice(palette)
        return g
    if name == "single_row0_color":
        c0 = palette[0]
        for c in range(w):
            g[0][c] = c0
        return g
    if name == "row0_all_zero":
        # Row 0 is all 0 — rows 2+ would all be 0.
        for r in range(1, h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = rng.choice(palette)
        return g
    return g
