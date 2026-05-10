"""Generator for puzzle cf98881b.

Rule: input is 4 × 14 (Q1: cols 0-3 | sep col 4 | Q2: cols 5-8 |
sep col 9 | Q3: cols 10-13). Output is 4 × 4 where each cell uses
priority Q1 > Q2 > Q3: first non-bg across the three panels wins.

Combinatorial axes: q1/q2/q3 colors, q1/q2/q3 density, fill_pattern.
Degenerates: all_zero, only_q1 (no overlay), all_three_overlap_at_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2534c7164e36"
VERSION = "1.1.0"
TASK_ID = "2534c7164e36"
SUMMARY = "Three 4 × 4 panels separated by bg cols; rule overlays priority Q1 > Q2 > Q3."

INVARIANTS = [
    "input is 4 × 14",
    "columns 4 and 9 are all bg (separators)",
    "each quadrant has ≥1 non-bg cell so output is non-trivial",
    "Q1, Q2, Q3 use distinct colors",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "border", "diagonal")
DEGENERATE_TEXTURES = ("all_zero", "only_q1", "all_overlap")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "q1_color":      {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "q2_color":      {"type": "color", "default": "rng (≠0,q1)", "valid": "1..9"},
    "q3_color":      {"type": "color", "default": "rng (≠0,q1,q2)", "valid": "1..9"},
    "q1_density":    {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "q2_density":    {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "q3_density":    {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "panel_pattern": {"type": "str", "default": "rng helpful",
                      "valid": "|".join(PANEL_PATTERNS)},
    "texture":       {"type": "str", "default": "alias for panel_pattern",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("panels")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    q1_c = int(overrides.get("q1_color", ctx.draw_color("q1_color", exclude={0})))
    q2_c = int(overrides.get("q2_color", ctx.draw_color("q2_color", exclude={0, q1_c})))
    q3_c = int(overrides.get("q3_color", ctx.draw_color("q3_color", exclude={0, q1_c, q2_c})))
    q1_d = float(overrides.get("q1_density",
                               ctx.draw_rng("q1_density").uniform(0.3, 0.7)))
    q2_d = float(overrides.get("q2_density",
                               ctx.draw_rng("q2_density").uniform(0.3, 0.7)))
    q3_d = float(overrides.get("q3_density",
                               ctx.draw_rng("q3_density").uniform(0.3, 0.7)))
    pattern = (overrides.get("texture") or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))
    g = full_grid(4, 14, 0)
    for q_idx, (color, density) in enumerate([(q1_c, q1_d), (q2_c, q2_d), (q3_c, q3_d)]):
        c0 = q_idx * 5
        _fill_panel(g, c0, c0 + 4, pattern, density, color, rng)
    return g


def _fill_panel(g, c0, c1, pattern, density, fg, rng):
    h = 4; w_p = c1 - c0
    if pattern == "random":
        for r in range(h):
            for c in range(c0, c1):
                if rng.random() < density:
                    g[r][c] = fg
    elif pattern == "blob":
        bh = max(1, int(h * density)); bw = max(1, int(w_p * density))
        rr = rng.randint(0, h - bh); cc = rng.randint(c0, c1 - bw)
        for r in range(rr, rr + bh):
            for c in range(cc, cc + bw):
                g[r][c] = fg
    elif pattern == "stripes":
        for r in range(h):
            if r % 2 == 0:
                for c in range(c0, c1):
                    g[r][c] = fg
    elif pattern == "border":
        for c in range(c0, c1):
            g[0][c] = fg; g[h - 1][c] = fg
        for r in range(h):
            g[r][c0] = fg; g[r][c1 - 1] = fg
    elif pattern == "diagonal":
        for k in range(min(h, w_p)):
            g[k][c0 + k] = fg


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    if name == "all_zero":
        return g
    if name == "only_q1":
        # Q2 and Q3 are entirely bg. Output is just Q1.
        c0 = 0
        for r in range(4):
            for c in range(c0, c0 + 4):
                if rng.random() < 0.5:
                    g[r][c] = palette[0]
        return g
    if name == "all_overlap":
        # All three quadrants have the same fg pattern at the same cells —
        # priority Q1 wins everywhere.
        cells = [(r, c) for r in range(4) for c in range(4)]
        rng.shuffle(cells)
        for r, c in cells[:8]:
            g[r][c] = palette[0]
            g[r][c + 5] = palette[1]
            g[r][c + 10] = palette[2]
        return g
    return g
