"""Generator for ARC task 5d2a5c43.

Rule: input is h × 9 (4 + 1 sep + 4). Output is h × 4: OR of nonzero
across panels → 8, else 0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "50a1b00ebe2f"
VERSION = "1.1.0"
TASK_ID = "50a1b00ebe2f"
SUMMARY = "Two 4-column panels separated by col 4; OR of nonzero-occupancy → 8, else 0."

INVARIANTS = [
    "input width is 9 (4 left + 1 separator + 4 right)",
    "col 4 is a separator",
    "≥1 non-zero cell across the panels",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "checker", "border", "diagonal")
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "disjoint_panels")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..14", "valid": "1..30"},
    "left_color":     {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "right_color":    {"type": "color", "default": "rng (≠0,left)", "valid": "1..9"},
    "sep_color":      {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "left_density":   {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "right_density":  {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "panel_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PANEL_PATTERNS)},
    "or_target":      {"type": "int", "default": "rng 1..max", "valid": "1..h*4"},
    "texture":        {"type": "str", "default": "alias for panel_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 3, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    rng = ctx.draw_rng("panels")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)
    left_c = int(overrides.get("left_color", ctx.draw_color("left_color", exclude={0})))
    right_c = int(overrides.get("right_color", ctx.draw_color("right_color", exclude={0, left_c})))
    sep = int(overrides.get("sep_color", ctx.draw_color("sep_color", exclude={0, left_c, right_c})))
    ld = float(overrides.get("left_density", ctx.draw_rng("left_density").uniform(0.3, 0.6)))
    rd = float(overrides.get("right_density", ctx.draw_rng("right_density").uniform(0.3, 0.6)))
    pattern = (overrides.get("texture") or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))
    g = full_grid(h, 9, 0)
    for r in range(h):
        g[r][4] = sep
    _fill_panel(g, 0, 4, h, pattern, ld, left_c, rng)
    _fill_panel(g, 5, 9, h, pattern, rd, right_c, rng)
    target = int(overrides.get("or_target",
                               ctx.draw_int("or_target", 1, max(1, h))))
    _ensure_or(g, h, target, left_c, rng)
    return g


def _fill_panel(g, c0, c1, h, pattern, density, fg, rng):
    if pattern == "random":
        for r in range(h):
            for c in range(c0, c1):
                g[r][c] = fg if rng.random() < density else 0
    elif pattern == "blob":
        bh = max(1, int(h * density)); bw = max(1, int((c1 - c0) * density))
        r0 = rng.randint(0, h - bh); cc = rng.randint(c0, c1 - bw)
        for r in range(r0, r0 + bh):
            for c in range(cc, cc + bw):
                g[r][c] = fg
    elif pattern == "stripes":
        for r in range(h):
            if r % 2 == 0:
                for c in range(c0, c1):
                    g[r][c] = fg
    elif pattern == "checker":
        for r in range(h):
            for c in range(c0, c1):
                if (r + c) % 2 == 0:
                    g[r][c] = fg
    elif pattern == "border":
        for c in range(c0, c1):
            g[0][c] = fg; g[h - 1][c] = fg
        for r in range(h):
            g[r][c0] = fg; g[r][c1 - 1] = fg
    elif pattern == "diagonal":
        for k in range(min(h, c1 - c0)):
            g[k][c0 + k] = fg


def _ensure_or(g, h, target, fg, rng):
    have = sum(1 for r in range(h) for c in range(4)
               if g[r][c] != 0 or g[r][c + 5] != 0)
    if have >= target:
        return
    cells = [(r, c) for r in range(h) for c in range(4)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target: break
        if g[r][c] == 0 and g[r][c + 5] == 0:
            g[r][c] = fg
            have += 1


def _draw_from_degenerate(name, h, rng):
    g = full_grid(h, 9, 0)
    left_c = rng.choice([1, 2, 3, 4, 5])
    right_c = rng.choice([6, 7, 8, 9])
    sep = rng.choice([c for c in range(1, 10) if c not in {left_c, right_c}])
    for r in range(h):
        g[r][4] = sep
    if name == "all_zero":
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(4):
                g[r][c] = left_c
                g[r][c + 5] = right_c
        return g
    if name == "disjoint_panels":
        for r in range(h):
            for c in range(4):
                if rng.random() < 0.5:
                    g[r][c] = left_c
                else:
                    g[r][c + 5] = right_c
        return g
    return g
