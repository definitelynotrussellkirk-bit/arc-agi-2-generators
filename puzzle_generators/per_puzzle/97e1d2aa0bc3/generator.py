"""Generator for 2de01db2.

Rule: per row, find most-frequent non-{0,7} color (mc). For each cell:
if cell == mc, output 0; else output mc.

Combinatorial axes (8): grid_h/w, palette_diversity, mc_ratio_kind,
distractor_ratio, fill_layout, palette_kind, asymmetry,
include_07_distractors.
Degenerates: monochrome_row, all_zero_seven, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "97e1d2aa0bc3"
VERSION = "1.1.0"
TASK_ID = "97e1d2aa0bc3"
SUMMARY = "Each row has a non-{0,7} majority color; rule complements + paints rest."

INVARIANTS = [
    "h in [2, 8], w in [6, 18]",
    "each row has a STRICTLY majority non-{0,7} color (>= half)",
    "rows have distinct majority colors (so per-row mc is unambiguous)",
    "0 and 7 may appear as distractors",
]

FILL_LAYOUTS = ("scattered", "blob_per_row", "alternating",
                "left_majority", "edges_distractor")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("monochrome_row", "all_zero_seven", "single_row")
HELPFUL_TEXTURES = FILL_LAYOUTS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 3..7", "valid": "2..9"},
    "grid_w":           {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "mc_ratio_kind":    {"type": "str", "default": "rng tight|loose|extreme",
                         "valid": "tight|loose|extreme"},
    "distractor_ratio": {"type": "float", "default": "rng 0.1..0.3",
                         "valid": "0..0.5"},
    "fill_layout":      {"type": "str", "default": "rng helpful",
                         "valid": "|".join(FILL_LAYOUTS)},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "include_07_distractors": {"type": "bool", "default": "true",
                               "valid": "true|false"},
    "min_majority":     {"type": "int", "default": "= w/2 + 1",
                         "valid": "1..w"},
    "texture":          {"type": "str", "default": "alias for fill_layout",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 2, 4, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 14, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 3, 7, 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 8, 9]
    rng.shuffle(pool)
    if len(pool) < h:
        extras = [c for c in [1, 2, 3, 4, 6, 8, 9] if c not in pool]
        rng.shuffle(extras)
        pool += extras
    pool = pool[:h]
    layout = (overrides.get("texture") or overrides.get("fill_layout")
              or ctx.draw_choice("fill_layout", list(FILL_LAYOUTS)))
    mc_kind = overrides.get("mc_ratio_kind",
                            ctx.draw_choice("mc_ratio_kind",
                                            ["tight", "loose", "extreme"]))
    if mc_kind == "tight":
        mc_lo, mc_hi = w // 2 + 1, w // 2 + 2
    elif mc_kind == "extreme":
        mc_lo, mc_hi = max(w - 2, w // 2 + 1), w
    else:
        mc_lo, mc_hi = int(w * 0.5) + 1, int(w * 0.7) + 1
    use_07 = bool(overrides.get("include_07_distractors", True))
    g = full_grid(h, w, 0)
    distractor_pool = ([0, 7] if use_07 else []) + [c for c in [1, 2, 3, 4, 6, 8, 9]]
    for r in range(h):
        mc = pool[r]
        n_mc = rng.randint(min(mc_lo, w), min(mc_hi, w))
        cols = _layout_mc_cols(layout, w, n_mc, rng)
        for c in cols:
            g[r][c] = mc
        for c in range(w):
            if g[r][c] == 0:
                pool_for_distract = [v for v in distractor_pool if v != mc]
                if not pool_for_distract:
                    pool_for_distract = [0]
                g[r][c] = rng.choice(pool_for_distract)
        counts = {}
        for v in g[r]:
            if v not in (0, 7):
                counts[v] = counts.get(v, 0) + 1
        if counts:
            sorted_c = sorted(counts.items(), key=lambda kv: -kv[1])
            if sorted_c[0][0] != mc:
                for c in range(w):
                    if g[r][c] == sorted_c[0][0]:
                        g[r][c] = mc
                        if sorted_c[0][1] - 1 < counts.get(mc, 0):
                            break
    return g


def _layout_mc_cols(layout, w, n, rng):
    cols = list(range(w))
    if layout == "blob_per_row":
        center = rng.randint(0, w - 1)
        cols.sort(key=lambda c: abs(c - center))
        return cols[:n]
    if layout == "left_majority":
        return cols[:n]
    if layout == "edges_distractor":
        return cols[1:1 + n] if w > 1 else cols[:n]
    if layout == "alternating":
        even = [c for c in cols if c % 2 == 0]
        odd = [c for c in cols if c % 2 != 0]
        return (even + odd)[:n]
    rng.shuffle(cols)
    return cols[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "monochrome_row":
        for r in range(h):
            color = rng.choice([1, 2, 3, 4, 6, 8, 9])
            for c in range(w):
                g[r][c] = color
        return g
    if name == "all_zero_seven":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([0, 7])
        return g
    if name == "single_row":
        if h <= 1:
            return [[1] * w]
        color = rng.choice([1, 2, 3, 4, 6, 8, 9])
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
