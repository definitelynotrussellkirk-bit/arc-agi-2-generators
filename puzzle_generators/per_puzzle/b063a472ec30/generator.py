"""Generator for 3bdb4ada.

Rule: in each cell where above and below cells share v, alternate cells
(by parity from leftmost matching cell) become 0.

Combinatorial axes (8): grid_h/w, n_bars, bar_width_range,
palette_size, bar_position_bias, vertical_spacing, decoy_density,
bar_clustering.
Degenerates: single_bar, full_grid_bar, no_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "b063a472ec30"
VERSION = "1.1.0"
TASK_ID = "b063a472ec30"
SUMMARY = "Horizontal solid bars (3 rows × W cols); rule hollows alternate cells in middle row."

INVARIANTS = [
    "background is 0",
    ">=1 horizontal bar of 3 rows × >=4 cols (so middle row has visible cells)",
    "bars don't share rows (4-row separation including the bar's 3 rows)",
    "each bar uses one solid color (≠0)",
]

DEGENERATE_TEXTURES = ("single_bar", "full_grid_bar", "no_bars")
HELPFUL_TEXTURES = ("balanced", "many_bars", "wide_bars", "edge_aligned")

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":            {"type": "int", "default": "rng 14..22", "valid": "10..28"},
    "n_bars":            {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "bar_width_range":   {"type": "str", "default": "rng small|medium|large",
                          "valid": "small|medium|large"},
    "palette_size":      {"type": "int", "default": "= n_bars",
                          "valid": "1..7"},
    "bar_position_bias": {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "vertical_spacing":  {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "decoy_density":     {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":           {"type": "str", "default": "rng helpful",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 10, 14
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 20, 28
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 14, 14, 22
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    if texture == "many_bars":
        n_bars = 4
    elif texture == "wide_bars":
        n_bars = 2
    elif texture == "edge_aligned":
        n_bars = 2
    else:
        n_bars = int(overrides.get("n_bars", ctx.draw_int("n_bars", 2, 4)))
    n_bars = max(1, min(5, n_bars))
    palette_pool = [c for c in range(1, 10) if c != 0]
    rng.shuffle(palette_pool)
    palette = palette_pool[:max(1, n_bars)]
    bw_kind = overrides.get("bar_width_range",
                            ctx.draw_choice("bar_width_range",
                                            ["small", "medium", "large"]))
    bw_lo, bw_hi = {"small": (5, 8), "medium": (7, 12),
                    "large": (10, 16)}[bw_kind]
    if texture == "wide_bars":
        bw_lo, bw_hi = max(8, bw_lo), max(15, bw_hi)
    bias = overrides.get("bar_position_bias",
                         ctx.draw_choice("bar_position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 0)
    used_rows = set()
    bars_placed = 0
    for _ in range(40):
        if bars_placed >= n_bars:
            break
        bar_w = rng.randint(bw_lo, min(w - 2, bw_hi))
        if bias == "center":
            bc = max(1, (w - bar_w) // 2 + rng.randint(-2, 2))
        elif bias == "edge":
            bc = rng.choice([1, max(1, w - bar_w - 1)])
        elif texture == "edge_aligned":
            bc = 1 if bars_placed % 2 == 0 else max(1, w - bar_w - 1)
        else:
            bc = rng.randint(1, w - bar_w - 1)
        bc = max(1, min(w - bar_w - 1, bc))
        br = rng.randint(0, h - 3)
        if any(r in used_rows for r in range(br - 1, br + 4)):
            continue
        draw_rect(g, br, bc, 3, bar_w, palette[bars_placed % len(palette)])
        for r in range(br - 1, br + 4):
            used_rows.add(r)
        bars_placed += 1
    if bars_placed < 1:
        bw = max(5, w // 2)
        draw_rect(g, h // 2 - 1, 1, 3, bw, palette[0])
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "single_bar":
        bw = max(5, w // 2)
        draw_rect(g, h // 2 - 1, 1, 3, bw, color)
        return g
    if name == "full_grid_bar":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "no_bars":
        return g
    return g
