"""Generator for ARC task 6ea4a07e.

Rule: find first non-bg color; map via {3→1, 5→4, 8→2, else→same}.
For each cell: non-bg → 0; bg → mapped color. (Invert + recolor bg.)

Combinatorial axes: grid_h/w, fg_color (in {3, 5, 8} for canonical
mapping), fg_density, fg_layout. Degenerates: all_zero, all_fg,
unmapped_color (rule keeps the same color).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "03478139591b"
VERSION = "1.1.0"
TASK_ID = "03478139591b"
SUMMARY = "Binary grid; rule clears fg and recolors bg via mapping (3→1, 5→4, 8→2)."

INVARIANTS = [
    "input uses 0 + exactly one fg color",
    "≥1 fg cell and ≥1 bg cell so output is non-trivial",
    "fg color in {3, 5, 8} (mapped) or other (unchanged)",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "blob", "border")
DEGENERATE_TEXTURES = ("all_zero", "all_fg", "unmapped_color")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":     {"type": "int", "default": "rng 3..10", "valid": "1..15"},
    "grid_w":     {"type": "int", "default": "rng 3..10", "valid": "1..15"},
    "fg_color":   {"type": "choice", "default": "rng of 3|5|8", "valid": "3|5|8"},
    "fg_density": {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "fg_layout":  {"type": "str", "default": "rng helpful",
                   "valid": "|".join(FG_LAYOUTS)},
    "texture":    {"type": "str", "default": "alias for fg_layout",
                   "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 8, 10
    else:
        h_lo, h_hi = 3, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("fg_color", ctx.draw_choice("fg_color", [3, 5, 8])))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.3, 0.6)))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    g = full_grid(h, w, 0)
    if layout == "random":
        for r in range(h):
            for c in range(w):
                if rng.random() < density:
                    g[r][c] = color
    elif layout == "cluster":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        for r in range(h):
            for c in range(w):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density:
                    g[r][c] = color
    elif layout == "row":
        r = rng.randint(0, h - 1)
        for c in range(w):
            if rng.random() < density:
                g[r][c] = color
    elif layout == "column":
        c = rng.randint(0, w - 1)
        for r in range(h):
            if rng.random() < density:
                g[r][c] = color
    elif layout == "diagonal":
        for k in range(min(h, w)):
            g[k][k] = color
    elif layout == "blob":
        bh = max(1, int(h * density)); bw = max(1, int(w * density))
        r0 = rng.randint(0, h - bh); c0 = rng.randint(0, w - bw)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = color
    elif layout == "border":
        for c in range(w):
            g[0][c] = color; g[h - 1][c] = color
        for r in range(h):
            g[r][0] = color; g[r][w - 1] = color
    # Ensure ≥1 fg and ≥1 bg
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[0][0] = color
    if all(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[-1][-1] = 0
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([3, 5, 8])
    if name == "all_zero":
        return g
    if name == "all_fg":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "unmapped_color":
        # Use a fg color NOT in {3, 5, 8} → rule keeps same color.
        color = rng.choice([1, 2, 4, 6, 7, 9])
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = color
        g[0][0] = color
        return g
    return g
