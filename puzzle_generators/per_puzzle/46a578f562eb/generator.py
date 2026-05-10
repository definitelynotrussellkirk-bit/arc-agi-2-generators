"""Generator for puzzle d037b0a7.

Rule: for each cell: keep if non-zero; else fill with the TOPMOST
non-zero cell above it in the same column. (Vertical "drip down" from
the topmost non-zero per column.)

Combinatorial axes: grid_h/w, fg_palette, n_cells, fg_layout, row_bias.
Degenerates: all_bg, monochrome (single color), only_bottom_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "46a578f562eb"
VERSION = "1.1.0"
TASK_ID = "46a578f562eb"
SUMMARY = "Sparse non-bg cells; rule fills bg cells with the topmost non-bg above (column-wise)."

INVARIANTS = [
    "bg = 0",
    "≥1 non-bg cell with at least one not in the bottom row",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "scattered")
ROW_BIASES = ("top", "bottom", "spread")
DEGENERATE_TEXTURES = ("all_bg", "monochrome", "only_bottom_row")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "fg_palette_size": {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "n_cells":         {"type": "int", "default": "rng 2..h*w/4", "valid": "1..h*w/2"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "row_bias":        {"type": "str", "default": "rng top|spread",
                        "valid": "|".join(ROW_BIASES)},
    "texture":         {"type": "str", "default": "alias for fg_layout",
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
    n_palette = int(overrides.get("fg_palette_size",
                                  ctx.draw_int("fg_palette_size", 1, 4)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    n_cells = int(overrides.get("n_cells",
                                ctx.draw_int("n_cells", 2, max(2, (h * w) // 4))))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    row_bias = overrides.get("row_bias",
                             ctx.draw_choice("row_bias", list(ROW_BIASES)))
    g = full_grid(h, w, 0)
    candidates = _candidates_for_bias(row_bias, h, w)
    cells = _layout_cells(layout, candidates, n_cells, rng)
    for r, c in cells:
        if 0 <= r < h - 1 and 0 <= c < w:  # bias above bottom so rule has effect
            g[r][c] = rng.choice(palette)
    if not any(g[r][c] != 0 for r in range(h - 1) for c in range(w)):
        g[0][0] = palette[0]
    return g


def _candidates_for_bias(bias, h, w):
    if bias == "top":
        return [(r, c) for r in range(0, max(1, h // 2)) for c in range(w)]
    if bias == "bottom":
        return [(r, c) for r in range(max(0, h // 2), h - 1) for c in range(w)]
    return [(r, c) for r in range(h - 1) for c in range(w)]


def _layout_cells(layout, candidates, n, rng):
    if not candidates:
        return []
    n = min(n, len(candidates))
    if layout == "cluster":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return candidates[:n]
    if layout == "row":
        rs = sorted({r for r, _ in candidates})
        if not rs: return []
        r = rng.choice(rs)
        cells = [(r, c) for (rr, c) in candidates if rr == r]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        cs = sorted({c for _, c in candidates})
        if not cs: return []
        c = rng.choice(cs)
        cells = [(r, c) for (r, cc) in candidates if cc == c]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        cand_set = set(candidates)
        return [(k, k) for k in range(25) if (k, k) in cand_set][:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "all_bg":
        # Need ≥1 cell to satisfy invariant.
        g[0][0] = fg
        return g
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = fg
        g[0][0] = fg
        return g
    if name == "only_bottom_row":
        for c in range(w):
            if rng.random() < 0.5:
                g[h - 1][c] = fg
        g[h - 1][0] = fg
        # Ensure ≥1 cell above bottom row (else rule has nothing to drip).
        g[0][0] = fg
        return g
    return g
