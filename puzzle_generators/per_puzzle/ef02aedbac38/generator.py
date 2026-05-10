"""Generator for puzzle f76d97a5.

Rule: find first non-5 cell value (call it `other`). For each cell:
if v == 5 → other, else → 0. (Swap 5 ↔ other and zero everything else.)

Combinatorial axes (8): grid_h/w, other_color, fg_density (non-5 cells),
fg_layout (random/cluster/blob/diagonal/border/scattered/stripes),
fg_position_bias, multi_other (whether more than 1 non-5 color),
n_unique_others.
Degenerates: all_5, no_5, monochrome_other.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef02aedbac38"
VERSION = "1.1.0"
TASK_ID = "ef02aedbac38"
SUMMARY = "Bg=5 with one other color; rule swaps 5 ↔ other and zeros original cells."

INVARIANTS = [
    "bg = 5",
    "≥1 non-5, non-0 cell (rule's color source)",
    "≥1 cell of bg = 5 (so output has at least one swapped cell)",
]

FG_LAYOUTS = ("random", "cluster", "blob", "diagonal", "border",
              "scattered", "stripes", "row")
DEGENERATE_TEXTURES = ("all_5", "no_5", "monochrome_other")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 4..18", "valid": "3..25"},
    "grid_w":          {"type": "int", "default": "rng 4..18", "valid": "3..25"},
    "other_color":     {"type": "color", "default": "rng (≠0,5)", "valid": "1..9 (≠5)"},
    "fg_density":      {"type": "float", "default": "rng 0.15..0.4", "valid": "0..0.7"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "fg_position_bias": {"type": "str", "default": "rng top|bottom|center|spread",
                        "valid": "top|bottom|center|spread"},
    "multi_other":     {"type": "bool", "default": "false", "valid": "true|false"},
    "n_unique_others": {"type": "int", "default": "rng 1..3", "valid": "1..6"},
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
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 4, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    other = int(overrides.get("other_color",
                              ctx.draw_color("other_color", exclude={0, 5})))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.15, 0.4)))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    bias = overrides.get("fg_position_bias",
                         ctx.draw_choice("fg_position_bias",
                                         ["top", "bottom", "center", "spread"]))
    multi = bool(overrides.get("multi_other", False))
    n_others = int(overrides.get("n_unique_others",
                                 ctx.draw_int("n_unique_others", 1, 3)))
    palette = [other]
    if multi and n_others > 1:
        extras = list(ctx.draw_distinct_colors("extras", n=n_others - 1, exclude={0, 5, other}))
        palette = [other] + extras
    g = full_grid(h, w, 5)
    candidates = _candidates_for_bias(bias, h, w)
    cells = _layout_cells(layout, candidates, density, rng)
    for r, c in cells:
        g[r][c] = rng.choice(palette)
    if not any(g[r][c] != 5 for r in range(h) for c in range(w)):
        g[0][0] = other
    return g


def _candidates_for_bias(bias, h, w):
    if bias == "top":
        return [(r, c) for r in range(0, max(1, h // 2)) for c in range(w)]
    if bias == "bottom":
        return [(r, c) for r in range(max(0, h // 2), h) for c in range(w)]
    if bias == "center":
        return [(r, c) for r in range(h // 4, max(h // 4 + 1, 3 * h // 4))
                for c in range(w // 4, max(w // 4 + 1, 3 * w // 4))]
    return [(r, c) for r in range(h) for c in range(w)]


def _layout_cells(layout, candidates, density, rng):
    if not candidates: return []
    n = max(1, int(len(candidates) * density))
    if layout == "cluster":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return candidates[:n]
    if layout == "blob":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return candidates[:n]
    if layout == "diagonal":
        cset = set(candidates)
        return [(k, k) for k in range(25) if (k, k) in cset][:n]
    if layout == "border":
        h = max(r for r, _ in candidates) + 1
        w = max(c for _, c in candidates) + 1
        cells = [(r, c) for (r, c) in candidates
                 if r in (0, h - 1) or c in (0, w - 1)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    if layout == "stripes":
        cells = [(r, c) for (r, c) in candidates if r % 2 == 0]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "row":
        rs = sorted({r for r, _ in candidates})
        if not rs: return []
        r = rng.choice(rs)
        cells = [(r, c) for (rr, c) in candidates if rr == r]
        rng.shuffle(cells)
        return cells[:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 5)
    other = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "all_5":
        # No non-5 cell; rule has no `other` color to read.
        # Insert 1 cell to keep invariant.
        g[0][0] = other
        return g
    if name == "no_5":
        for r in range(h):
            for c in range(w):
                g[r][c] = other
        # Force 1 bg=5 cell so rule has work.
        g[0][0] = 5
        return g
    if name == "monochrome_other":
        for r in range(h):
            for c in range(w):
                g[r][c] = other
        return g
    return g
