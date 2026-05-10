"""Generator for 342dd610.

Rule: bg = mode color. Each non-bg cell shifts by its color:
7 → (-2, 0), 2 → (0, -2), 9 → (2, 0), 1 → (0, 1). Output is bg-filled
grid with markers at new positions.

Combinatorial axes (8): grid_h/w, n_marks, color_distribution,
position_bias, marker_layout, palette_subset, decoy_density,
edge_avoidance.
Degenerates: no_marks, single_color, all_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ba75376d7f1"
VERSION = "1.1.0"
TASK_ID = "3ba75376d7f1"
SUMMARY = "Markers in {7,2,9,1} shift by direction; rule paints new positions."

INVARIANTS = [
    "bg = 8 (most common)",
    ">=2 markers in colors {7, 2, 9, 1}",
    "each marker's shifted target is in-bounds",
    "no two markers share the same shifted target (avoids overwrite ambiguity)",
]

MARKER_LAYOUTS = ("scattered", "clustered", "diagonal", "rows",
                  "cols", "edges_only", "interior_only")
PALETTE_SUBSETS = ("all_four", "vertical_only", "horizontal_only", "pair")
DEGENERATE_TEXTURES = ("no_marks", "single_color", "all_corners")
HELPFUL_TEXTURES = MARKER_LAYOUTS

SHIFT = {7: (-2, 0), 2: (0, -2), 9: (2, 0), 1: (0, 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 6, 9, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 11, 16, 4, 6
    else:
        h_lo, h_hi, n_lo, n_hi = 8, 13, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_marks = int(overrides.get("n_marks",
                                ctx.draw_int("n_marks", n_lo, n_hi)))
    n_marks = max(2, min(8, n_marks))
    palette_subset = overrides.get("palette_subset",
                                   ctx.draw_choice("palette_subset",
                                                   list(PALETTE_SUBSETS)))
    if palette_subset == "vertical_only":
        colors = [7, 9]
    elif palette_subset == "horizontal_only":
        colors = [2, 1]
    elif palette_subset == "pair":
        colors = rng.sample([7, 2, 9, 1], 2)
    else:
        colors = [7, 2, 9, 1]
    layout = (overrides.get("texture") or overrides.get("marker_layout")
              or ctx.draw_choice("marker_layout", list(MARKER_LAYOUTS)))
    g = full_grid(h, w, 8)
    placed = set()
    targets = set()
    for _ in range(60):
        if len(placed) >= n_marks:
            break
        color = rng.choice(colors)
        dr, dc = SHIFT[color]
        r_lo = max(0, -dr)
        r_hi = min(h - 1, h - 1 - dr)
        c_lo = max(0, -dc)
        c_hi = min(w - 1, w - 1 - dc)
        if r_hi < r_lo or c_hi < c_lo:
            continue
        r, c = _pick_pos(layout, r_lo, r_hi, c_lo, c_hi, rng)
        if (r, c) in placed:
            continue
        target = (r + dr, c + dc)
        if target in targets:
            continue
        g[r][c] = color
        placed.add((r, c))
        targets.add(target)
    if len(placed) < 2:
        for color in colors[:2]:
            dr, dc = SHIFT[color]
            r_lo = max(0, -dr)
            r_hi = min(h - 1, h - 1 - dr)
            c_lo = max(0, -dc)
            c_hi = min(w - 1, w - 1 - dc)
            if r_hi >= r_lo and c_hi >= c_lo:
                g[r_lo][c_lo] = color
                placed.add((r_lo, c_lo))
    return g


def _pick_pos(layout, r_lo, r_hi, c_lo, c_hi, rng):
    if layout == "diagonal":
        k = rng.randint(0, min(r_hi - r_lo, c_hi - c_lo))
        return r_lo + k, c_lo + k
    if layout == "rows":
        return rng.randint(r_lo, r_hi), rng.randint(c_lo, c_hi)
    if layout == "cols":
        return rng.randint(r_lo, r_hi), rng.randint(c_lo, c_hi)
    if layout == "clustered":
        cr = (r_lo + r_hi) // 2
        cc = (c_lo + c_hi) // 2
        return cr + rng.randint(-1, 1), cc + rng.randint(-1, 1)
    if layout == "edges_only":
        choices = [(r_lo, rng.randint(c_lo, c_hi)),
                   (r_hi, rng.randint(c_lo, c_hi)),
                   (rng.randint(r_lo, r_hi), c_lo),
                   (rng.randint(r_lo, r_hi), c_hi)]
        return rng.choice(choices)
    if layout == "interior_only":
        rl = r_lo + 1; rh = r_hi - 1
        cl = c_lo + 1; ch = c_hi - 1
        if rh < rl: rl, rh = r_lo, r_hi
        if ch < cl: cl, ch = c_lo, c_hi
        return rng.randint(rl, rh), rng.randint(cl, ch)
    return rng.randint(r_lo, r_hi), rng.randint(c_lo, c_hi)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 8)
    if name == "no_marks":
        return g
    if name == "single_color":
        color = rng.choice([7, 2, 9, 1])
        dr, dc = SHIFT[color]
        r_lo = max(0, -dr); r_hi = min(h - 1, h - 1 - dr)
        c_lo = max(0, -dc); c_hi = min(w - 1, w - 1 - dc)
        if r_hi >= r_lo and c_hi >= c_lo:
            for _ in range(3):
                r = rng.randint(r_lo, r_hi); c = rng.randint(c_lo, c_hi)
                g[r][c] = color
        return g
    if name == "all_corners":
        corners = [(2, 2), (2, w - 3), (h - 3, 2), (h - 3, w - 3)]
        for i, (r, c) in enumerate(corners):
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = [7, 2, 9, 1][i]
        return g
    return g
