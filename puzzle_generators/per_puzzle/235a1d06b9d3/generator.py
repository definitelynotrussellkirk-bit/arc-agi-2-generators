"""Generator for ARC task 7e4d4f7c.

Rule: bg = g[2][1]. Output is 3 × w:
  row 0 = input row 0
  row 1 = input row 1
  row 2[c] = bg if g[0][c] == bg else 6

Combinatorial axes: grid_h, grid_w, bg_color, row0_pattern,
row1_pattern, row0_bg_density.
Degenerates: row0_all_bg, row0_no_bg, monochrome_row0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "235a1d06b9d3"
VERSION = "1.1.0"
TASK_ID = "235a1d06b9d3"
SUMMARY = "3+ row grid; rule emits 3 rows: row0, row1, derived row from row 0 + bg."

INVARIANTS = [
    "h ≥ 3",
    "bg = g[2][1] is well-defined",
    "row 0 has both bg and non-bg cells (so derived row has variety)",
]

ROW0_PATTERNS = ("random", "alternating", "blocks", "sparse_bg")
DEGENERATE_TEXTURES = ("row0_all_bg", "row0_no_bg", "monochrome_row0")
HELPFUL_TEXTURES = ROW0_PATTERNS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 3..14", "valid": "3..18"},
    "grid_w":           {"type": "int", "default": "rng 4..14", "valid": "2..18"},
    "bg_color":         {"type": "color", "default": "rng (≠6)", "valid": "0..9 (≠6)"},
    "row0_pattern":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(ROW0_PATTERNS)},
    "row0_bg_density":  {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "texture":          {"type": "str", "default": "alias for row0_pattern",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 3, 5, 4, 7
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 11, 14
    else:
        h_lo, h_hi, w_lo, w_hi = 3, 14, 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={6})))
    pattern = (overrides.get("texture") or overrides.get("row0_pattern")
               or ctx.draw_choice("row0_pattern", list(ROW0_PATTERNS)))
    density = float(overrides.get("row0_bg_density",
                                  ctx.draw_rng("row0_bg_density").uniform(0.3, 0.7)))
    palette = list(ctx.draw_distinct_colors("palette", n=3, exclude={bg, 6}))
    g = full_grid(h, w, bg)
    # Row 0
    if pattern == "random":
        for c in range(w):
            g[0][c] = bg if rng.random() < density else rng.choice(palette)
    elif pattern == "alternating":
        for c in range(w):
            g[0][c] = bg if c % 2 == 0 else palette[0]
    elif pattern == "blocks":
        block = max(1, w // 3)
        for c in range(w):
            g[0][c] = bg if (c // block) % 2 == 0 else palette[0]
    elif pattern == "sparse_bg":
        for c in range(w):
            g[0][c] = palette[0]
        for c in range(0, w, max(1, w // 3)):
            g[0][c] = bg
    # Row 1 — decoy
    for c in range(w):
        g[1][c] = rng.choice([bg] + palette)
    # Row 2 col 1 = bg (rule reads it). Other cells in rows 2+ are decoy.
    g[2][1] = bg
    for r in range(2, h):
        for c in range(w):
            if (r, c) != (2, 1):
                g[r][c] = rng.choice([bg] + palette)
    # Force ≥1 bg and ≥1 non-bg in row 0.
    if all(g[0][c] == bg for c in range(w)):
        g[0][0] = palette[0]
    if all(g[0][c] != bg for c in range(w)):
        g[0][0] = bg
    return g


def _draw_from_degenerate(name, h, w, rng):
    bg = rng.choice([c for c in range(10) if c != 6])
    palette = [c for c in range(1, 10) if c not in {bg, 6}]
    rng.shuffle(palette)
    g = full_grid(h, w, bg)
    if name == "row0_all_bg":
        # Row 2 derived will be all bg → uniform output.
        for r in range(1, h):
            for c in range(w):
                g[r][c] = rng.choice([bg] + palette)
        g[2][1] = bg
        return g
    if name == "row0_no_bg":
        for c in range(w):
            g[0][c] = rng.choice(palette)
        for r in range(1, h):
            for c in range(w):
                g[r][c] = rng.choice([bg] + palette)
        g[2][1] = bg
        return g
    if name == "monochrome_row0":
        c0 = palette[0]
        for c in range(w):
            g[0][c] = c0
        g[2][1] = bg
        return g
    return g
