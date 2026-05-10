"""Generator for puzzle c1d99e64.

Rule: replace every all-bg row and every all-bg column with red(2).

Combinatorial axes (8): grid_h/w, fg_color, fill_ratio,
n_inactive_rows, n_inactive_cols, palette_size, fg_layout, position_bias.
Degenerates: no_inactive_rows, no_inactive_cols, all_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "548c1010ce89"
VERSION = "1.1.0"
TASK_ID = "548c1010ce89"
SUMMARY = "Some all-bg rows and cols; rule recolors them red."

INVARIANTS = [
    "background is 0",
    ">=1 all-bg row (so row-replace branch fires)",
    ">=1 all-bg column",
    ">=1 row with content",
    ">=1 col with content",
    "non-bg colors do not include 2 (red is the rule's fill)",
]

FG_LAYOUTS = ("scattered", "cluster", "diagonal", "anti_diag",
              "rows_dominant", "cols_dominant", "noise")
DEGENERATE_TEXTURES = ("no_inactive_rows", "no_inactive_cols", "all_bg")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":          {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "fg_color":        {"type": "color", "default": "rng (≠0,2)", "valid": "1..9 (≠2)"},
    "fill_ratio":      {"type": "float", "default": "rng 0.2..0.5",
                        "valid": "0.1..0.7"},
    "n_inactive_rows": {"type": "int", "default": "rng 2..4", "valid": "1..h-2"},
    "n_inactive_cols": {"type": "int", "default": "rng 2..4", "valid": "1..w-2"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "palette_size":    {"type": "int", "default": "1", "valid": "1..3"},
    "texture":         {"type": "str", "default": "alias for fg_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg_color = int(overrides.get("fg_color",
                                 ctx.draw_color("fg_color", exclude={0, 2})))
    n_palette = int(overrides.get("palette_size", 1))
    palette_pool = [c for c in range(1, 10) if c not in (0, 2, fg_color)]
    rng.shuffle(palette_pool)
    palette = [fg_color] + palette_pool[:max(0, n_palette - 1)]
    fill_ratio = float(overrides.get("fill_ratio",
                                     ctx.draw_rng("fill_ratio").uniform(0.2, 0.5)))
    n_inactive_r = int(overrides.get("n_inactive_rows",
                                     ctx.draw_int("n_inactive_rows", 2, max(2, h // 4))))
    n_inactive_c = int(overrides.get("n_inactive_cols",
                                     ctx.draw_int("n_inactive_cols", 2, max(2, w // 4))))
    n_inactive_r = max(1, min(h - 2, n_inactive_r))
    n_inactive_c = max(1, min(w - 2, n_inactive_c))
    inactive_rows = set(rng.sample(range(h), n_inactive_r))
    inactive_cols = set(rng.sample(range(w), n_inactive_c))
    active_rows = [r for r in range(h) if r not in inactive_rows]
    active_cols = [c for c in range(w) if c not in inactive_cols]
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    g = full_grid(h, w, 0)
    cells = _layout_cells(layout, active_rows, active_cols, fill_ratio, rng)
    for r, c in cells:
        g[r][c] = rng.choice(palette)
    if all(g[r][c] == 0 for r in active_rows for c in active_cols):
        if active_rows and active_cols:
            g[active_rows[0]][active_cols[0]] = fg_color
    for r in active_rows:
        if all(g[r][c] == 0 for c in range(w)):
            g[r][active_cols[0]] = fg_color
    for c in active_cols:
        if all(g[r][c] == 0 for r in range(h)):
            g[active_rows[0]][c] = fg_color
    return g


def _layout_cells(layout, active_rows, active_cols, ratio, rng):
    if not active_rows or not active_cols:
        return []
    cells = [(r, c) for r in active_rows for c in active_cols]
    n = max(2, int(len(cells) * ratio))
    if layout == "diagonal":
        sorted_rows = sorted(active_rows)
        sorted_cols = sorted(active_cols)
        diag = []
        for k in range(min(len(sorted_rows), len(sorted_cols))):
            diag.append((sorted_rows[k], sorted_cols[k]))
        return diag[:n] if diag else cells[:n]
    if layout == "anti_diag":
        sorted_rows = sorted(active_rows)
        sorted_cols = sorted(active_cols, reverse=True)
        diag = []
        for k in range(min(len(sorted_rows), len(sorted_cols))):
            diag.append((sorted_rows[k], sorted_cols[k]))
        return diag[:n] if diag else cells[:n]
    if layout == "cluster":
        cr = rng.choice(active_rows)
        cc = rng.choice(active_cols)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "rows_dominant":
        chosen_rows = rng.sample(active_rows, min(2, len(active_rows)))
        out = [(r, c) for r in chosen_rows for c in active_cols]
        return out[:n]
    if layout == "cols_dominant":
        chosen_cols = rng.sample(active_cols, min(2, len(active_cols)))
        out = [(r, c) for r in active_rows for c in chosen_cols]
        return out[:n]
    if layout == "noise":
        rng.shuffle(cells)
        return cells[:n]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_inactive_rows":
        for r in range(h):
            g[r][0] = color
        return g
    if name == "no_inactive_cols":
        for c in range(w):
            g[0][c] = color
        return g
    if name == "all_bg":
        return g
    return g
