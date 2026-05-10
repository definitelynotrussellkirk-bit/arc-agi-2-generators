"""Generator for ARC task e729b7be.

Rule: for each cell: if v != 7 keep v; else if 180°-mirror cell != 7
take that value; else 7. (Complete 180°-symmetry by mirroring non-7
cells into 7 slots.)

Combinatorial axes: grid_h/w, fg_palette, fg_density, fg_layout,
asymmetric (must be 180°-asymmetric).
Degenerates: rot180_symmetric (rule no-op), all_seven, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1674812130ff"
VERSION = "1.1.0"
TASK_ID = "1674812130ff"
SUMMARY = "Cells on bg=7; rule completes 180°-symmetry by mirroring non-7 into 7 slots."

INVARIANTS = [
    "background is 7",
    "≥1 cell where the 180°-mirror is 7 (so rule fills it)",
    "≥1 fg color so output diversity is meaningful",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "blob", "scattered")
DEGENERATE_TEXTURES = ("rot180_symmetric", "all_seven", "monochrome")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "fg_palette_size": {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "fg_density":      {"type": "float", "default": "rng 0.15..0.4", "valid": "0..0.7"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "texture":         {"type": "str", "default": "alias for fg_layout",
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
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={7})) or [1]
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.15, 0.4)))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    g = full_grid(h, w, 7)
    candidates = [(r, c) for r in range(h) for c in range(w)]
    cells = _layout_cells(layout, candidates, density, rng)
    for r, c in cells:
        g[r][c] = rng.choice(palette)
    # Need ≥1 cell whose 180°-mirror is 7.
    for r in range(h):
        for c in range(w):
            if g[r][c] != 7 and g[h - 1 - r][w - 1 - c] == 7:
                if (r, c) != (h - 1 - r, w - 1 - c):
                    return g
    # Force one such cell.
    for r in range(h):
        for c in range(w):
            mr, mc = h - 1 - r, w - 1 - c
            if (r, c) != (mr, mc):
                g[r][c] = palette[0]
                g[mr][mc] = 7
                return g
    return g


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
        return [(k, k) for k in range(25) if (k, k) in set(candidates)][:n]
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
    palette = list(ctx.draw_distinct_colors("palette", n=3, exclude={7})) or [1]
    g = full_grid(h, w, 7)
    if name == "rot180_symmetric":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    color = rng.choice(palette)
                    g[r][c] = color
                    g[h - 1 - r][w - 1 - c] = color
        return g
    if name == "all_seven":
        return g
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = c0
        return g
    return g
