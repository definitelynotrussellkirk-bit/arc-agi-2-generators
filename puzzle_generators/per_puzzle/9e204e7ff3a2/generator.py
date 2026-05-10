"""Generator for puzzle 496994bd.

Rule: complete vertical (UD) symmetry. Output cell (r, c) = input cell
if non-zero; else its UD mirror's value if non-zero; else 0.

Combinatorial axes: grid_h/w, fg_palette, fg_density, fg_layout,
ud_asymmetric (must be UD-asymmetric so rule has visible effect).
Degenerates: ud_symmetric (rule no-op), all_zero, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e204e7ff3a2"
VERSION = "1.1.0"
TASK_ID = "9e204e7ff3a2"
SUMMARY = "Sparse non-bg cells; rule completes UD symmetry by mirroring into bg cells."

INVARIANTS = [
    "background is 0",
    "≥1 cell where the UD mirror is bg (so rule fills it)",
    "≥2 distinct fg colors so output diversity is meaningful",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "blob", "scattered")
DEGENERATE_TEXTURES = ("ud_symmetric", "all_zero", "monochrome")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "fg_palette_size": {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "fg_density":     {"type": "float", "default": "rng 0.15..0.4", "valid": "0..0.7"},
    "fg_layout":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(FG_LAYOUTS)},
    "row_bias":       {"type": "str", "default": "rng top|bottom|spread",
                       "valid": "top|bottom|spread"},
    "texture":        {"type": "str", "default": "alias for fg_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)
    n_palette = int(overrides.get("fg_palette_size",
                                  ctx.draw_int("fg_palette_size", 1, 4)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.15, 0.4)))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    row_bias = overrides.get("row_bias",
                             ctx.draw_choice("row_bias", ["top", "bottom", "spread"]))
    g = full_grid(h, w, 0)
    candidates = _candidates_for_bias(row_bias, h, w)
    cells = _layout_cells(layout, candidates, density, rng)
    for r, c in cells:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = rng.choice(palette)
    # Need at least one cell whose UD mirror is bg.
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0 and g[h - 1 - r][c] == 0 and r != h - 1 - r:
                return g
    # Force one such cell.
    for r in range(h // 2):
        for c in range(w):
            if r != h - 1 - r:
                g[r][c] = palette[0]
                g[h - 1 - r][c] = 0
                return g
    return g


def _candidates_for_bias(bias, h, w):
    if bias == "top":
        return [(r, c) for r in range(h // 2) for c in range(w)]
    if bias == "bottom":
        return [(r, c) for r in range(h // 2, h) for c in range(w)]
    return [(r, c) for r in range(h) for c in range(w)]


def _layout_cells(layout, candidates, density, rng):
    if not candidates:
        return []
    n = max(1, int(len(candidates) * density))
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
    if layout == "blob":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return candidates[:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, ctx, rng):
    palette = list(ctx.draw_distinct_colors("palette", n=3, exclude={0}))
    g = full_grid(h, w, 0)
    if name == "ud_symmetric":
        for r in range(h // 2):
            for c in range(w):
                if rng.random() < 0.3:
                    color = rng.choice(palette)
                    g[r][c] = color
                    g[h - 1 - r][c] = color
        return g
    if name == "all_zero":
        return g
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = c0
        g[0][0] = c0
        return g
    return g
