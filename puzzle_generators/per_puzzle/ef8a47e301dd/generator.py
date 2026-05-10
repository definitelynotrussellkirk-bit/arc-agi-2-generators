"""Generator for puzzle 3bd67248.

Rule: output is fixed by dims + g[0][0] (used as bg-color of col 0):
  col 0 → bg-color
  anti-diagonal (r + c == h - 1) → 2
  last row (r == h - 1, not on col 0 or anti-diag) → 4
  else 0

Combinatorial axes: grid_h/w, bg_color (= g[0][0]),
input_decoration (line / random / blob — rule reads only g[0][0]).
Degenerates: monochrome_bg (no decoration), all_zero_input,
decoy_anti_diag (input mimics output to mislead).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef8a47e301dd"
VERSION = "1.1.0"
TASK_ID = "ef8a47e301dd"
SUMMARY = "Input determines bg via g[0][0]; rule outputs fixed dims-only pattern."

INVARIANTS = [
    "bg color (g[0][0]) ≠ 2 and ≠ 4",
    "h ≥ 3, w ≥ 3",
    "input contents besides g[0][0] are decoy",
]

INPUT_DECORATIONS = ("line", "random", "sparse", "blob", "frame")
DEGENERATE_TEXTURES = ("monochrome_bg", "all_zero_input", "decoy_anti_diag")
HELPFUL_TEXTURES = INPUT_DECORATIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":             {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "bg_color":           {"type": "color", "default": "rng (≠2,4)", "valid": "0..9 (≠2,4)"},
    "line_color":         {"type": "color", "default": "rng (≠bg,2,4)", "valid": "0..9"},
    "input_decoration":   {"type": "str", "default": "rng helpful",
                           "valid": "|".join(INPUT_DECORATIONS)},
    "texture":            {"type": "str", "default": "alias for input_decoration",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={2, 4})))
    line = int(overrides.get("line_color", ctx.draw_color("line_color", exclude={bg, 2, 4})))
    decoration = (overrides.get("texture") or overrides.get("input_decoration")
                  or ctx.draw_choice("input_decoration", list(INPUT_DECORATIONS)))
    g = full_grid(h, w, bg)
    if decoration == "line":
        for r in range(h):
            g[r][0] = line
    elif decoration == "random":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = line
    elif decoration == "sparse":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.15:
                    g[r][c] = line
    elif decoration == "blob":
        bh = h // 2; bw = w // 2
        r0 = rng.randint(0, h - bh); c0 = rng.randint(0, w - bw)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = line
    elif decoration == "frame":
        for c in range(w):
            g[0][c] = line; g[h - 1][c] = line
        for r in range(h):
            g[r][0] = line; g[r][w - 1] = line
    # Force g[0][0] = bg (since rule uses it).
    g[0][0] = bg
    return g


def _draw_from_degenerate(name, h, w, ctx, rng):
    bg = ctx.draw_color("bg_color", exclude={2, 4})
    g = full_grid(h, w, bg)
    if name == "monochrome_bg":
        return g
    if name == "all_zero_input":
        return full_grid(h, w, 0)
    if name == "decoy_anti_diag":
        # Input mimics the output anti-diag pattern.
        for r in range(h):
            for c in range(w):
                if r + c == h - 1 and c != 0:
                    g[r][c] = 2
        g[0][0] = bg
        return g
    return g
