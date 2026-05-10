"""Generator for ARC task 662c240a.

Rule: input has 3 vertically-stacked panels of size ph × w. Output is
the FIRST panel (top to bottom) that is NOT diagonal-symmetric.

Combinatorial axes: panel_h, panel_w, palette_size,
asymmetric_position (top/middle/bottom), texture_kind.
Degenerates: all_diagonal_symmetric (rule has no answer), all_asymmetric
(output is always panel 0), single_panel_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d97c22b1360"
VERSION = "1.1.0"
TASK_ID = "8d97c22b1360"
SUMMARY = "Three stacked square panels; rule selects the first non-diagonal-symmetric panel."

INVARIANTS = [
    "input is 3 panels of equal height stacked vertically (panel is square)",
    "≥1 panel is non-diagonal-symmetric (rule has answer)",
    "≥1 panel is diagonal-symmetric (so the rule's choice is meaningful)",
]

ASYMMETRIC_POSITIONS = ("top", "middle", "bottom")
DEGENERATE_TEXTURES = ("all_symmetric", "all_asymmetric", "single_color_panels")
HELPFUL_TEXTURES = ASYMMETRIC_POSITIONS

AXES = {
    "panel_size":           {"type": "int", "default": "rng 3..6", "valid": "3..10"},
    "fg_color":             {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "alt_color":            {"type": "color", "default": "rng (≠0,fg)", "valid": "1..9"},
    "asymmetric_position":  {"type": "str", "default": "rng top|middle|bottom",
                             "valid": "|".join(ASYMMETRIC_POSITIONS)},
    "texture":              {"type": "str", "default": "alias for asymmetric_position",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        s_lo, s_hi = 3, 4
    elif difficulty == "hard":
        s_lo, s_hi = 5, 6
    else:
        s_lo, s_hi = 3, 6
    ph = ctx.draw_int("panel_size", s_lo, s_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], ph, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    alt = int(overrides.get("alt_color", ctx.draw_color("alt_color", exclude={0, fg})))
    pos = overrides.get("texture",
                        overrides.get("asymmetric_position",
                                      ctx.draw_choice("asymmetric_position",
                                                      list(ASYMMETRIC_POSITIONS))))
    g = full_grid(3 * ph, ph, 0)
    panels = [_make_symmetric_panel(ph, fg, alt, rng) for _ in range(3)]
    if pos == "top":
        panels[0] = _make_asymmetric_panel(ph, fg, alt, rng)
    elif pos == "middle":
        panels[1] = _make_asymmetric_panel(ph, fg, alt, rng)
    elif pos == "bottom":
        panels[2] = _make_asymmetric_panel(ph, fg, alt, rng)
    for pi, panel in enumerate(panels):
        for r in range(ph):
            for c in range(ph):
                g[pi * ph + r][c] = panel[r][c]
    return g


def _make_symmetric_panel(n, fg, alt, rng):
    """Diagonal-symmetric panel: g[r][c] == g[c][r]."""
    p = full_grid(n, n, 0)
    for r in range(n):
        for c in range(r + 1):
            v = rng.choice([0, fg, alt])
            p[r][c] = v
            p[c][r] = v
    return p


def _make_asymmetric_panel(n, fg, alt, rng):
    p = full_grid(n, n, 0)
    for r in range(n):
        for c in range(n):
            p[r][c] = rng.choice([0, fg, alt])
    # Force diagonal asymmetry.
    if all(p[r][c] == p[c][r] for r in range(n) for c in range(n)):
        if n >= 2:
            p[0][1] = fg
            p[1][0] = alt
    return p


def _draw_from_degenerate(name, ph, rng):
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    alt = rng.choice([c for c in range(1, 10) if c != fg])
    g = full_grid(3 * ph, ph, 0)
    if name == "all_symmetric":
        for pi in range(3):
            panel = _make_symmetric_panel(ph, fg, alt, rng)
            for r in range(ph):
                for c in range(ph):
                    g[pi * ph + r][c] = panel[r][c]
        return g
    if name == "all_asymmetric":
        for pi in range(3):
            panel = _make_asymmetric_panel(ph, fg, alt, rng)
            for r in range(ph):
                for c in range(ph):
                    g[pi * ph + r][c] = panel[r][c]
        return g
    if name == "single_color_panels":
        for pi in range(3):
            for r in range(ph):
                for c in range(ph):
                    g[pi * ph + r][c] = fg
        return g
    return g
