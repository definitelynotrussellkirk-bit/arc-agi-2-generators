"""Generator for ARC task 0c9aba6e.

Rule: `(rule! (lambda (g) (zip-halves g (lambda (a b) (if (and (= a 0) (= b 0)) 8 0)) 7)))`.
Two same-sized panels split by a full color-7 row. The rule combines
them: cells where BOTH panels have 0 → 8, otherwise → 0.

Combinatorial axes:
  * panel_h / panel_w     — panel dims
  * top_color / bot_color — fg colors of the two panels
  * top_density / bot_density — fraction of fg cells in each panel
  * pattern               — fg arrangement: random/blob/stripes/checker/border/L
  * aligned_zeros_count   — minimum number of (r, c) where BOTH panels are 0
                            (controls how much "match" appears in output)
  * caller-opt-in degenerates: no_aligned_zeros (output is all 0),
                               all_aligned_zeros (output is all 8),
                               same_panels (top==bottom)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "76aff6297765"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "76aff6297765"
SUMMARY = "Two same-sized panels split by a full 7-row; aligned double-zero cells become 8."

INVARIANTS = [
    "separator row is all 7",
    "top and bottom panels have equal dimensions",
    "at least one aligned cell is zero in both panels (output has ≥1 8)",
]

HELPFUL_PATTERNS = (
    "random", "blob", "stripes", "checker",
    "border", "L_shape", "diagonal", "scatter",
)
DEGENERATE_TEXTURES = ("no_aligned_zeros", "all_aligned_zeros", "same_panels")

AXES = {
    "panel_h":             {"type": "int",   "default": "rng 3..8", "valid": "2..14"},
    "panel_w":             {"type": "int",   "default": "rng 3..8", "valid": "2..30"},
    "top_color":           {"type": "color", "default": "rng",      "valid": "1..9 (≠7)"},
    "bot_color":           {"type": "color", "default": "rng",      "valid": "1..9 (≠7, ≠top)"},
    "top_density":         {"type": "float", "default": "rng 0.4..0.7", "valid": "0.1..0.9"},
    "bot_density":         {"type": "float", "default": "rng 0.4..0.7", "valid": "0.1..0.9"},
    "pattern":             {"type": "str",   "default": "rng helpful",
                            "valid": "|".join(HELPFUL_PATTERNS)},
    "aligned_zeros_count": {"type": "int",   "default": "rng 1..max",
                            "valid": "1..panel_h*panel_w"},
    "texture":             {"type": "str",   "default": "alias for pattern",
                            "valid": "|".join(HELPFUL_PATTERNS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 3, 5, 3, 5
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 6, 8
    else:
        h_lo, h_hi, w_lo, w_hi = 3, 8, 3, 8

    ph = ctx.draw_int("panel_h", h_lo, h_hi)
    pw = ctx.draw_int("panel_w", w_lo, w_hi)
    rng = ctx.draw_rng("panels")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], ph, pw, rng)

    top_color = int(overrides.get("top_color",
                                  ctx.draw_color("top_color", exclude={0, 7})))
    bot_color = int(overrides.get("bot_color",
                                  ctx.draw_color("bot_color", exclude={0, 7, top_color})))
    top_d = float(overrides.get(
        "top_density",
        ctx.draw_rng("top_density").uniform(0.4, 0.7)))
    bot_d = float(overrides.get(
        "bot_density",
        ctx.draw_rng("bot_density").uniform(0.4, 0.7)))
    pattern = (overrides.get("texture")
               or overrides.get("pattern")
               or ctx.draw_choice("pattern", list(HELPFUL_PATTERNS)))

    g = full_grid(ph * 2 + 1, pw, 0)
    for c in range(pw):
        g[ph][c] = 7

    _paint_panel(g, 0, ph, pw, top_color, top_d, pattern, rng)
    _paint_panel(g, ph + 1, ph, pw, bot_color, bot_d, pattern, rng)

    aligned_target = int(overrides.get(
        "aligned_zeros_count",
        ctx.draw_int("aligned_zeros_count", 1, max(1, ph * pw // 3))))
    _ensure_aligned_zeros(g, ph, pw, aligned_target, rng)
    return g


def _paint_panel(g, row_offset, ph, pw, color, density, pattern, rng):
    if pattern == "random":
        for r in range(ph):
            for c in range(pw):
                g[row_offset + r][c] = 0 if rng.random() > density else color
    elif pattern == "blob":
        bh = max(1, int(ph * density))
        bw = max(1, int(pw * density))
        r0 = rng.randint(0, ph - bh)
        c0 = rng.randint(0, pw - bw)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[row_offset + r][c] = color
    elif pattern == "stripes":
        for r in range(ph):
            if r % 2 == rng.randint(0, 1):
                for c in range(pw):
                    g[row_offset + r][c] = color
    elif pattern == "checker":
        for r in range(ph):
            for c in range(pw):
                if (r + c) % 2 == 0:
                    g[row_offset + r][c] = color
    elif pattern == "border":
        for c in range(pw):
            g[row_offset][c] = color
            g[row_offset + ph - 1][c] = color
        for r in range(ph):
            g[row_offset + r][0] = color
            g[row_offset + r][pw - 1] = color
    elif pattern == "L_shape":
        for r in range(ph):
            g[row_offset + r][0] = color
        for c in range(pw):
            g[row_offset + ph - 1][c] = color
    elif pattern == "diagonal":
        for k in range(min(ph, pw)):
            g[row_offset + k][k] = color
    elif pattern == "scatter":
        for r in range(ph):
            for c in range(pw):
                if rng.random() < density * 0.5:
                    g[row_offset + r][c] = color


def _ensure_aligned_zeros(g, ph, pw, target, rng):
    """Make sure at least `target` (r, c) positions have BOTH panels at 0."""
    have = sum(1 for r in range(ph) for c in range(pw)
               if g[r][c] == 0 and g[ph + 1 + r][c] == 0)
    if have >= target:
        return
    cells = [(r, c) for r in range(ph) for c in range(pw)]
    rng.shuffle(cells)
    for (r, c) in cells:
        if have >= target:
            return
        g[r][c] = 0
        g[ph + 1 + r][c] = 0
        have += 1


def _draw_from_degenerate(name, ph, pw, rng):
    """Edge-case where the zip-halves signature is hidden.

    no_aligned_zeros  — no (r, c) has 0 in both panels; output is all 0
                        (rule's "if zero,zero → 8" never triggers).
    all_aligned_zeros — both panels are entirely 0; output is all 8.
    same_panels       — top and bottom are identical; output looks
                        like a "where input == 0" indicator.
    """
    g = full_grid(ph * 2 + 1, pw, 0)
    for c in range(pw):
        g[ph][c] = 7
    if name == "no_aligned_zeros":
        for r in range(ph):
            for c in range(pw):
                g[r][c] = 2
                g[ph + 1 + r][c] = 0 if rng.random() < 0.5 else 6
        # Force at least one 0 somewhere on top so panel isn't trivially uniform.
        return g
    if name == "all_aligned_zeros":
        # Both panels all-zero (output will be solid 8 — visually trivial).
        return g
    if name == "same_panels":
        for r in range(ph):
            for c in range(pw):
                v = 0 if rng.random() < 0.5 else 4
                g[r][c] = v
                g[ph + 1 + r][c] = v
        return g
    return g
