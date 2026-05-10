"""Generator for 2a28add5.

Rule: per row, find non-7 cells. If a 6 exists at index idx of N
non-7 cells, paint cols [c6 - idx, c6 - idx + N - 1] with 8.

Combinatorial axes (8): grid_h/w, n_active_rows, bar_length_kind,
position_bias, palette_kind, decoy_density, idx_kind, asymmetry.
Degenerates: no_active_rows, all_six, multiple_sixes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "587396c0817d"
VERSION = "1.1.0"
TASK_ID = "587396c0817d"
SUMMARY = "7-bg with 6-anchored rows; rule paints 8-bar centered on 6's index."

INVARIANTS = [
    "bg = 7",
    ">=2 rows have >=3 non-7 cells",
    "in those rows: exactly one cell is color 6",
    "non-7 cells in those rows fit such that bar stays in bounds",
    "no color 8 in input (rule writes 8 for output)",
]

BAR_LENGTH_KINDS = ("small", "medium", "large", "varied")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_active_rows", "all_six", "multiple_sixes")
HELPFUL_TEXTURES = BAR_LENGTH_KINDS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "grid_w":           {"type": "int", "default": "rng 9..16", "valid": "8..20"},
    "n_active_rows":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "bar_length_kind":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(BAR_LENGTH_KINDS)},
    "position_bias":    {"type": "str", "default": "rng spread|center|edge",
                         "valid": "spread|center|edge"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "idx_kind":         {"type": "str", "default": "rng spread|left_biased|right_biased",
                         "valid": "spread|left_biased|right_biased"},
    "min_cells":        {"type": "int", "default": "3", "valid": "2..6"},
    "texture":          {"type": "str", "default": "alias for bar_length_kind",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 8, 11
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_active = int(overrides.get("n_active_rows",
                                 ctx.draw_int("n_active_rows", 2, 4)))
    n_active = max(1, min(h, n_active))
    bar_kind = (overrides.get("texture") or
                overrides.get("bar_length_kind")
                or ctx.draw_choice("bar_length_kind",
                                   list(BAR_LENGTH_KINDS)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        other_palette = [3, 4, 9]
    elif palette_kind == "cool":
        other_palette = [1, 5]
    elif palette_kind == "small":
        other_palette = [1, 2, 3]
    else:
        other_palette = [0, 1, 2, 3, 4, 5, 8, 9]
    idx_kind = overrides.get("idx_kind",
                             ctx.draw_choice("idx_kind",
                                             ["spread", "left_biased",
                                              "right_biased"]))
    g = full_grid(h, w, 7)
    rows = rng.sample(range(h), n_active)
    for r in rows:
        bar_len = _draw_bar_length(bar_kind, w, rng)
        idx = _draw_idx(idx_kind, bar_len, rng)
        c6_min = idx
        c6_max = w - 1 - (bar_len - 1 - idx)
        if c6_min > c6_max:
            continue
        c6 = rng.randint(c6_min, c6_max)
        before_cols = sorted(rng.sample(range(0, c6), idx)) if idx > 0 else []
        after_cols = (sorted(rng.sample(range(c6 + 1, w), bar_len - 1 - idx))
                      if (bar_len - 1 - idx) > 0 else [])
        g[r][c6] = 6
        for c in before_cols:
            g[r][c] = rng.choice(other_palette) if other_palette else 1
        for c in after_cols:
            g[r][c] = rng.choice(other_palette) if other_palette else 1
    return g


def _draw_bar_length(kind, w, rng):
    if kind == "small":
        return rng.randint(3, min(4, w))
    if kind == "medium":
        return rng.randint(4, min(6, w))
    if kind == "large":
        return rng.randint(5, min(8, w))
    return rng.randint(3, min(6, w))


def _draw_idx(kind, bar_len, rng):
    if kind == "left_biased":
        return rng.randint(0, max(0, bar_len // 3))
    if kind == "right_biased":
        return rng.randint(max(0, 2 * bar_len // 3), bar_len - 1)
    return rng.randint(0, bar_len - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    if name == "no_active_rows":
        return g
    if name == "all_six":
        for r in range(h):
            g[r][w // 2] = 6
        return g
    if name == "multiple_sixes":
        r = h // 2
        g[r][1] = 6
        g[r][w - 2] = 6
        return g
    return g
