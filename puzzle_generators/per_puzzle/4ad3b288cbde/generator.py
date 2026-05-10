"""Generator for ARC task 963e52fc.

Rule: for each row, find the smallest period p such that g[r][c] ==
g[r][c mod p] for all c. Output is h × 2w with row[r][c] = g[r][c mod p].

Combinatorial axes (8):
  * grid_h / grid_w        — input dims (output 2w must fit)
  * palette_size           — distinct colors used
  * period_distribution    — same / mixed / progressive (rows may have
                             different periods)
  * period_range           — small (1-3) / medium (2-4) / large (1-6)
  * row_pattern_kind       — repeat / alternate / palette_cycle / blocks
  * decoy_color_count      — non-period colors that interrupt? Must
                             preserve period — so used as fill but
                             carefully
  * inter_row_relation     — independent / linked / cycling
  * caller-opt-in degenerates: all_period_1 (output equals input/2),
                              non_periodic (rule fails),
                              max_period (period == w).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4ad3b288cbde"
VERSION = "1.1.0"
TASK_ID = "4ad3b288cbde"
SUMMARY = "Rows are periodic; rule doubles width by repeating each row's period."

INVARIANTS = [
    "each row has an exact small period that divides w",
    "input width ≤ 14 (so 2w fits)",
    "≥2 distinct colors per row so the period is non-trivial",
]

PERIOD_DISTRIBUTIONS = ("same", "mixed", "progressive")
PERIOD_RANGES = ("small", "medium", "large")
ROW_PATTERN_KINDS = ("repeat", "alternate", "palette_cycle", "blocks")
INTER_ROW_RELATIONS = ("independent", "linked", "cycling")
DEGENERATE_TEXTURES = ("all_period_1", "max_period_w", "non_periodic")
HELPFUL_TEXTURES = ROW_PATTERN_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 3..14", "valid": "1..18"},
    "grid_w":              {"type": "choice", "default": "rng",
                            "valid": "4|6|8|10|12"},
    "palette_size":        {"type": "int", "default": "rng 3..6", "valid": "2..10"},
    "period_distribution": {"type": "str", "default": "rng helpful",
                            "valid": "|".join(PERIOD_DISTRIBUTIONS)},
    "period_range":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(PERIOD_RANGES)},
    "row_pattern_kind":    {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ROW_PATTERN_KINDS)},
    "inter_row_relation":  {"type": "str", "default": "rng helpful",
                            "valid": "|".join(INTER_ROW_RELATIONS)},
    "texture":              {"type": "str", "default": "alias for row_pattern_kind",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_choices = 3, 6, [4, 6]
    elif difficulty == "hard":
        h_lo, h_hi, w_choices = 11, 14, [10, 12]
    else:
        h_lo, h_hi, w_choices = 3, 14, [4, 6, 8, 10, 12]
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_choice("grid_w", w_choices)
    n_colors = ctx.draw_int("palette_size", 3, 6)
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors))
    rng = ctx.draw_rng("rows")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    period_dist = overrides.get("period_distribution",
                                ctx.draw_choice("period_distribution",
                                                list(PERIOD_DISTRIBUTIONS)))
    period_range = overrides.get("period_range",
                                 ctx.draw_choice("period_range",
                                                 list(PERIOD_RANGES)))
    pattern_kind = (overrides.get("texture") or overrides.get("row_pattern_kind")
                    or ctx.draw_choice("row_pattern_kind", list(ROW_PATTERN_KINDS)))
    relation = overrides.get("inter_row_relation",
                             ctx.draw_choice("inter_row_relation",
                                             list(INTER_ROW_RELATIONS)))
    valid_periods = [p for p in _periods_for_w(w, period_range) if p > 0]
    if not valid_periods:
        valid_periods = [2]
    g = full_grid(h, w, 0)
    last_pattern = None
    for r in range(h):
        period = _pick_period(period_dist, r, valid_periods, rng)
        pat = _make_row_pattern(pattern_kind, period, palette, rng,
                                relation, last_pattern)
        last_pattern = pat
        for c in range(w):
            g[r][c] = pat[c % period]
    return g


def _periods_for_w(w, range_kind):
    divisors = [d for d in range(1, w + 1) if w % d == 0]
    if range_kind == "small":
        return [d for d in divisors if d <= 3]
    if range_kind == "medium":
        return [d for d in divisors if 2 <= d <= 4]
    if range_kind == "large":
        return [d for d in divisors if 1 <= d <= 6]
    return divisors


def _pick_period(dist, r, valid_periods, rng):
    if dist == "same":
        return valid_periods[0]
    if dist == "progressive":
        return valid_periods[r % len(valid_periods)]
    return rng.choice(valid_periods)


def _make_row_pattern(kind, period, palette, rng, relation, last):
    if relation == "linked" and last and len(last) == period:
        return last
    if relation == "cycling" and last:
        return [last[(i + 1) % len(last)] for i in range(period)]
    if kind == "repeat":
        c = rng.choice(palette)
        return [c] * period if period > 1 else [c]
    if kind == "alternate":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        return [a if i % 2 == 0 else b for i in range(period)]
    if kind == "palette_cycle":
        return [palette[i % len(palette)] for i in range(period)]
    if kind == "blocks":
        return [rng.choice(palette) for _ in range(period)]
    return [rng.choice(palette) for _ in range(period)]


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, 0)
    if name == "all_period_1":
        for r in range(h):
            c0 = rng.choice(palette)
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "max_period_w":
        # Each row has period w (no internal repetition).
        for r in range(h):
            cells = [rng.choice(palette) for _ in range(w)]
            for c in range(w):
                g[r][c] = cells[c]
        return g
    if name == "non_periodic":
        # Entirely random; rule's `find-first` may fail or give unexpected period.
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        return g
    return g
