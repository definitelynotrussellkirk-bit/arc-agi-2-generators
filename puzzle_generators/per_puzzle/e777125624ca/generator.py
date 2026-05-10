"""Generator for ARC task 1b2d62fb.

Rule: input is h × 7 (3 + 1 sep + 3). Output is h × 3:
left[r][c]==0 AND right[r][c]==0 → 8, else 0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e777125624ca"
VERSION = "1.1.0"
TASK_ID = "e777125624ca"
SUMMARY = "Two 3-column panels separated by a marker; aligned both-zero cells become 8."

INVARIANTS = [
    "input width is 7: 3 left + 1 separator + 3 right",
    "panels use 0 and one fg color",
    "≥1 aligned cell pair is both zero",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "checker", "border", "diagonal")
DEGENERATE_TEXTURES = ("no_both_zero", "all_both_zero", "same_panels")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..12", "valid": "1..18"},
    "fg_color":       {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "sep_color":      {"type": "color", "default": "rng (≠0,fg)", "valid": "1..9"},
    "left_density":   {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "right_density":  {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "panel_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PANEL_PATTERNS)},
    "both_zero_target": {"type": "int", "default": "rng 1..h", "valid": "1..h*3"},
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
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 3, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    rng = ctx.draw_rng("panels")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    sep = int(overrides.get("sep_color", ctx.draw_color("sep_color", exclude={0, fg})))
    ld = float(overrides.get("left_density",
                             ctx.draw_rng("left_density").uniform(0.3, 0.6)))
    rd = float(overrides.get("right_density",
                             ctx.draw_rng("right_density").uniform(0.3, 0.6)))
    pattern = (overrides.get("texture") or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))
    g = full_grid(h, 7, 0)
    for r in range(h):
        g[r][3] = sep
    _fill_panel(g, 0, 3, h, pattern, ld, fg, rng)
    _fill_panel(g, 4, 7, h, pattern, rd, fg, rng)
    target = int(overrides.get("both_zero_target",
                               ctx.draw_int("both_zero_target", 1, max(1, h))))
    _ensure_both_zero(g, h, target, rng)
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


def _ensure_both_zero(g, h, target, rng):
    have = sum(1 for r in range(h) for c in range(3)
               if g[r][c] == 0 and g[r][c + 4] == 0)
    if have >= target:
        return
    cells = [(r, c) for r in range(h) for c in range(3)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target: break
        g[r][c] = 0; g[r][c + 4] = 0
        have += 1


def _draw_from_degenerate(name, h, rng):
    g = full_grid(h, 7, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])  # ≠ 8 since 8 is output marker
    sep = rng.choice([c for c in range(1, 10) if c not in {fg, 8}])
    for r in range(h):
        g[r][3] = sep
    if name == "no_both_zero":
        for r in range(h):
            for c in range(3):
                g[r][c] = fg
                g[r][c + 4] = 0 if rng.random() < 0.4 else fg
        return g
    if name == "all_both_zero":
        return g
    if name == "same_panels":
        for r in range(h):
            for c in range(3):
                v = fg if rng.random() < 0.5 else 0
                g[r][c] = v
                g[r][c + 4] = v
        return g
    return g
