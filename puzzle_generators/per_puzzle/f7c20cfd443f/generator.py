"""Generator for puzzle ce22a75a.

Rule: for each cell, if any 8-neighbor (including itself) has value 5
→ output 1, else output 0. (5-cell 8-neighborhood dilation.)

Combinatorial axes (8):
  * grid_h / grid_w        — outer canvas size
  * bg_color               — background (≠ 1, ≠ 5)
  * n_dots                 — number of gray(5) dots
  * dot_layout             — random / cluster / row / column / diagonal /
                             scattered / blob / corners
  * dot_clustering         — controls dot density via spread/concentrated
  * decoy_palette_size     — non-5 non-bg cells to confuse (rule ignores)
  * decoy_density          — how many decoys
  * caller-opt-in degenerates: no_dots (rule no-op),
                              dot_in_every_cell (output all 1),
                              border_dots_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7c20cfd443f"
VERSION = "1.1.0"
TASK_ID = "f7c20cfd443f"
SUMMARY = "Gray(5) dots on bg; rule paints 1 in the 3 × 3 halo of each dot."

INVARIANTS = [
    "bg ≠ 5 and bg ≠ 1",
    "≥1 gray(5) cell",
    "n_dots ≤ h*w/3 (so output isn't all 1s in helpful path)",
]

DOT_LAYOUTS = ("random", "cluster", "row", "column", "diagonal",
               "scattered", "blob", "corners")
DOT_CLUSTERINGS = ("spread", "concentrated", "uniform")
DEGENERATE_TEXTURES = ("no_dots", "dot_in_every_cell", "border_dots_only")
HELPFUL_TEXTURES = DOT_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 4..18", "valid": "3..25"},
    "grid_w":             {"type": "int", "default": "rng 4..18", "valid": "3..25"},
    "bg_color":           {"type": "color", "default": "rng (≠1,5)", "valid": "0..9 (≠1,5)"},
    "n_dots":             {"type": "int", "default": "rng 1..h*w/4", "valid": "1..h*w/3"},
    "dot_layout":         {"type": "str", "default": "rng helpful",
                           "valid": "|".join(DOT_LAYOUTS)},
    "dot_clustering":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(DOT_CLUSTERINGS)},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.15", "valid": "0..0.5"},
    "texture":            {"type": "str", "default": "alias for dot_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 4, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={1, 5})))
    n_dots = int(overrides.get("n_dots",
                               ctx.draw_int("n_dots", 1, max(1, (h * w) // 4))))
    layout = (overrides.get("texture") or overrides.get("dot_layout")
              or ctx.draw_choice("dot_layout", list(DOT_LAYOUTS)))
    clustering = overrides.get("dot_clustering",
                               ctx.draw_choice("dot_clustering", list(DOT_CLUSTERINGS)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.15)))
    g = full_grid(h, w, bg)
    decoy_palette = [c for c in range(1, 10) if c not in {bg, 1, 5}]
    rng.shuffle(decoy_palette)
    decoy_palette = decoy_palette[:max(0, n_decoy)]
    if decoy_palette:
        for r in range(h):
            for c in range(w):
                if rng.random() < decoy_d:
                    g[r][c] = rng.choice(decoy_palette)
    cells = _dot_layout(layout, clustering, h, w, n_dots, rng)
    for r, c in cells:
        g[r][c] = 5
    if not any(g[r][c] == 5 for r in range(h) for c in range(w)):
        g[h // 2][w // 2] = 5
    return g


def _dot_layout(layout, clustering, h, w, n, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "cluster" or clustering == "concentrated":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "row":
        r = rng.randint(0, h - 1)
        cells = [(r, c) for c in range(w)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        c = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        return [(k, k) for k in range(min(h, w))][:n]
    if layout == "scattered" or clustering == "spread":
        scat = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(scat)
        return scat[:n]
    if layout == "blob":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells.sort(key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return cells[:n]
    if layout == "corners":
        return [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)][:n]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    bg = rng.choice([c for c in range(10) if c not in {1, 5}])
    g = full_grid(h, w, bg)
    if name == "no_dots":
        # Add ≥1 dot to keep invariant — caller-opt-in is "rule has nothing to do" intent.
        # Place exactly 1 dot at a corner (output is just a tiny halo).
        g[0][0] = 5
        return g
    if name == "dot_in_every_cell":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "border_dots_only":
        for c in range(w):
            g[0][c] = 5
            g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5
            g[r][w - 1] = 5
        return g
    return g
