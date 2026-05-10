"""Generator for ARC task 66f2d22f.

Rule: input is h × 2w (no separator). Output is h × w: both-zero across
left/right halves → 5, else 0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "784b131b3b93"
VERSION = "1.1.0"
TASK_ID = "784b131b3b93"
SUMMARY = "Two equal-width halves stacked horizontally; aligned both-zero cells become 5."

INVARIANTS = [
    "input width is even (2*half_w)",
    "halves use 0 + non-zero colors",
    "≥1 cell-pair is both zero",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "checker", "border", "diagonal")
DEGENERATE_TEXTURES = ("no_both_zero", "all_both_zero", "same_halves")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..14", "valid": "1..30"},
    "half_w":         {"type": "int", "default": "rng 3..7", "valid": "1..15"},
    "left_color":     {"type": "color", "default": "rng (≠0,5)", "valid": "1..9 (≠5)"},
    "right_color":    {"type": "color", "default": "rng (≠0,5,left)", "valid": "1..9 (≠5)"},
    "left_density":   {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "right_density":  {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "panel_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PANEL_PATTERNS)},
    "both_zero_target": {"type": "int", "default": "rng 1..max", "valid": "1..h*half_w"},
    "texture":        {"type": "str", "default": "alias for panel_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, hw_lo, hw_hi = 3, 5, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, hw_lo, hw_hi = 10, 14, 6, 7
    else:
        h_lo, h_hi, hw_lo, hw_hi = 3, 14, 3, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    half_w = ctx.draw_int("half_w", hw_lo, hw_hi)
    rng = ctx.draw_rng("panels")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, half_w, rng)
    left_c = int(overrides.get("left_color", ctx.draw_color("left_color", exclude={0, 5})))
    right_c = int(overrides.get("right_color", ctx.draw_color("right_color", exclude={0, 5, left_c})))
    ld = float(overrides.get("left_density",
                             ctx.draw_rng("left_density").uniform(0.3, 0.6)))
    rd = float(overrides.get("right_density",
                             ctx.draw_rng("right_density").uniform(0.3, 0.6)))
    pattern = (overrides.get("texture") or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))
    g = full_grid(h, 2 * half_w, 0)
    _fill_panel(g, 0, half_w, h, pattern, ld, left_c, rng)
    _fill_panel(g, half_w, 2 * half_w, h, pattern, rd, right_c, rng)
    target = int(overrides.get("both_zero_target",
                               ctx.draw_int("both_zero_target", 1, max(1, h))))
    _ensure_both_zero(g, h, half_w, target, rng)
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


def _ensure_both_zero(g, h, half_w, target, rng):
    have = sum(1 for r in range(h) for c in range(half_w)
               if g[r][c] == 0 and g[r][c + half_w] == 0)
    if have >= target:
        return
    cells = [(r, c) for r in range(h) for c in range(half_w)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target: break
        g[r][c] = 0; g[r][c + half_w] = 0
        have += 1


def _draw_from_degenerate(name, h, half_w, rng):
    w = 2 * half_w
    g = full_grid(h, w, 0)
    left_c = rng.choice([1, 2, 3, 4])
    right_c = rng.choice([6, 7, 8, 9])
    if name == "no_both_zero":
        for r in range(h):
            for c in range(half_w):
                g[r][c] = left_c
                g[r][c + half_w] = 0 if rng.random() < 0.4 else right_c
        return g
    if name == "all_both_zero":
        return g
    if name == "same_halves":
        for r in range(h):
            for c in range(half_w):
                v = left_c if rng.random() < 0.5 else 0
                g[r][c] = v
                g[r][c + half_w] = (right_c if v != 0 else 0)
        return g
    return g
