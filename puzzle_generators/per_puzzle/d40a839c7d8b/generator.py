"""Generator for puzzle d406998b.

Rule: target_parity = (w+1) % 2. For each cell with v == 5: if
c % 2 == target_parity → 3, else keep. Effect: gray(5) cells at
"alternate parity" columns become green(3); the rest stay gray.

Combinatorial axes: grid_h/w, gray_count, gray_layout, gray_col_density
(controls how many grays land on the trigger parity), bg_color.
Degenerates: no_grays, all_grays_one_parity, single_gray.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d40a839c7d8b"
VERSION = "1.1.0"
TASK_ID = "d40a839c7d8b"
SUMMARY = "Gray cells on bg; rule recolors gray at columns matching (w+1)%2 parity to green."

INVARIANTS = [
    "background is non-gray, non-green",
    "≥1 gray(5) cell at the trigger column parity",
    "≥1 gray(5) cell at the OTHER column parity (so rule branches both ways)",
]

GRAY_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "scattered")
DEGENERATE_TEXTURES = ("no_grays", "all_grays_one_parity", "single_gray")
HELPFUL_TEXTURES = GRAY_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "gray_count":      {"type": "int", "default": "rng 4..h*w/4", "valid": "1..h*w"},
    "gray_layout":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(GRAY_LAYOUTS)},
    "bg_color":        {"type": "color", "default": "rng (≠0,3,5)", "valid": "0..9 (≠3,5)"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "texture":         {"type": "str", "default": "alias for gray_layout",
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
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color", exclude={3, 5})))
    n_decor = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 3)))
    decor_palette = list(ctx.draw_distinct_colors(
        "decor", n=max(0, n_decor), exclude={bg, 3, 5}))
    n_grays = int(overrides.get("gray_count",
                                ctx.draw_int("gray_count", 4, max(4, (h * w) // 4))))
    layout = (overrides.get("texture") or overrides.get("gray_layout")
              or ctx.draw_choice("gray_layout", list(GRAY_LAYOUTS)))
    g = full_grid(h, w, bg)
    if decor_palette:
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.15:
                    g[r][c] = rng.choice(decor_palette)
    cells = _gray_layout_cells(layout, h, w, n_grays, rng)
    for r, c in cells:
        g[r][c] = 5

    target_parity = (w + 1) % 2
    has_trigger = any(c % 2 == target_parity and g[r][c] == 5
                      for r in range(h) for c in range(w))
    has_other = any(c % 2 != target_parity and g[r][c] == 5
                    for r in range(h) for c in range(w))
    if not has_trigger:
        # Force one gray at trigger parity.
        for c in range(w):
            if c % 2 == target_parity:
                g[0][c] = 5
                break
    if not has_other:
        for c in range(w):
            if c % 2 != target_parity:
                g[0][c] = 5
                break
    return g


def _gray_layout_cells(layout, h, w, n, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if layout == "cluster":
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
    if layout == "scattered":
        scat = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(scat)
        return scat[:n]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_grays":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice([1, 2, 4, 6, 7, 8, 9])
        return g
    if name == "all_grays_one_parity":
        target_parity = (w + 1) % 2
        for c in range(w):
            if c % 2 == target_parity:
                for r in range(h):
                    if rng.random() < 0.5:
                        g[r][c] = 5
        # ensure ≥1 gray
        g[0][0 if 0 % 2 == target_parity else 1] = 5
        return g
    if name == "single_gray":
        target_parity = (w + 1) % 2
        c = next((cc for cc in range(w) if cc % 2 == target_parity), 0)
        g[rng.randint(0, h - 1)][c] = 5
        return g
    return g
