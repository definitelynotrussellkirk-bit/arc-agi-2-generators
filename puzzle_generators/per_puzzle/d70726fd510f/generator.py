"""Generator for ARC task 34b99a2b.

Rule: input has a full color-4 separator column at col `sep`. Output
is h × sep: cells where exactly one of (left, right) is zero → 2,
else 0.

Combinatorial axes (8): grid_h, panel_w, left_color, right_color,
left_density, right_density, panel_pattern, xor_target.
Degenerates: same_panels, disjoint_panels, all_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d70726fd510f"
VERSION = "1.1.0"
TASK_ID = "d70726fd510f"
SUMMARY = "Two equal-width panels split by a full color-4 col; XOR of zero-occupancy → 2."

INVARIANTS = [
    "one full separator column is color 4",
    "left and right panels have equal width (panel_w)",
    "≥1 aligned cell differs in zero/nonzero occupancy",
]

PANEL_PATTERNS = ("random", "blob", "stripes", "checker", "border", "diagonal", "scatter")
DEGENERATE_TEXTURES = ("same_panels", "disjoint_panels", "all_zero")
HELPFUL_TEXTURES = PANEL_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..14", "valid": "1..18"},
    "panel_w":        {"type": "int", "default": "rng 3..7", "valid": "1..14"},
    "left_color":     {"type": "color", "default": "rng (≠0,2,4)", "valid": "1..9 (≠2,4)"},
    "right_color":    {"type": "color", "default": "rng (≠0,2,4,left)", "valid": "1..9"},
    "left_density":   {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "right_density":  {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "panel_pattern":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PANEL_PATTERNS)},
    "xor_target":     {"type": "int", "default": "rng 1..h*pw/2", "valid": "1..h*pw"},
    "texture":        {"type": "str", "default": "alias for panel_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, pw_lo, pw_hi = 4, 6, 3, 5
    elif difficulty == "hard":
        h_lo, h_hi, pw_lo, pw_hi = 11, 14, 6, 7
    else:
        h_lo, h_hi, pw_lo, pw_hi = 4, 14, 3, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    pw = ctx.draw_int("panel_w", pw_lo, pw_hi)
    rng = ctx.draw_rng("panels")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, pw, rng)
    left_c = int(overrides.get("left_color",
                               ctx.draw_color("left_color", exclude={0, 2, 4})))
    right_c = int(overrides.get("right_color",
                                ctx.draw_color("right_color", exclude={0, 2, 4, left_c})))
    ld = float(overrides.get("left_density",
                             ctx.draw_rng("left_density").uniform(0.3, 0.7)))
    rd = float(overrides.get("right_density",
                             ctx.draw_rng("right_density").uniform(0.3, 0.7)))
    pattern = (overrides.get("texture") or overrides.get("panel_pattern")
               or ctx.draw_choice("panel_pattern", list(PANEL_PATTERNS)))
    g = full_grid(h, 2 * pw + 1, 0)
    for r in range(h):
        g[r][pw] = 4
    _fill(g, 0, pw, h, pattern, ld, left_c, rng)
    _fill(g, pw + 1, 2 * pw + 1, h, pattern, rd, right_c, rng)
    target = int(overrides.get("xor_target",
                               ctx.draw_int("xor_target", 1, max(1, h * pw // 2))))
    have = sum(1 for r in range(h) for c in range(pw)
               if (g[r][c] == 0) != (g[r][pw + 1 + c] == 0))
    cells = [(r, c) for r in range(h) for c in range(pw)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target: break
        if g[r][c] == 0 and g[r][pw + 1 + c] == 0:
            g[r][c] = left_c
            have += 1
    return g


def _fill(g, c0, c1, h, pattern, density, fg, rng):
    if pattern == "random":
        for r in range(h):
            for c in range(c0, c1):
                if rng.random() < density:
                    g[r][c] = fg
    elif pattern == "blob":
        bh = max(1, int(h * density)); bw = max(1, int((c1 - c0) * density))
        rr = rng.randint(0, h - bh); cc = rng.randint(c0, c1 - bw)
        for r in range(rr, rr + bh):
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
    elif pattern == "scatter":
        for r in range(h):
            for c in range(c0, c1):
                if rng.random() < density * 0.5:
                    g[r][c] = fg


def _draw_from_degenerate(name, h, pw, rng):
    g = full_grid(h, 2 * pw + 1, 0)
    for r in range(h):
        g[r][pw] = 4
    left_c = rng.choice([1, 3, 5, 6, 7, 8, 9])
    right_c = rng.choice([c for c in [1, 3, 5, 6, 7, 8, 9] if c != left_c])
    if name == "same_panels":
        for r in range(h):
            for c in range(pw):
                v = left_c if rng.random() < 0.5 else 0
                g[r][c] = v
                g[r][pw + 1 + c] = (right_c if v != 0 else 0)
        return g
    if name == "disjoint_panels":
        for r in range(h):
            for c in range(pw):
                if rng.random() < 0.5:
                    g[r][c] = left_c
                else:
                    g[r][pw + 1 + c] = right_c
        return g
    if name == "all_zero":
        return g
    return g
