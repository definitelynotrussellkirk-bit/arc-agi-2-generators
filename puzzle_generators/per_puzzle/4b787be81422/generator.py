"""Generator for ARC task 44f52bb0.

Rule: `(rule! (lambda (g) (grid (list (list (if (symmetric? g "lr") 1 7))))))`
  Output is a 1 × 1 grid: 1 if the input is LR-symmetric, else 7.

Combinatorial axes:
  * grid_h / grid_w     — input dims (canonical is 3 × 3 but axis exposed)
  * symmetric           — bool: force input LR-sym or not
  * fg_color            — the non-bg color
  * fg_density          — fraction of cells that take the fg color
  * pattern             — fg arrangement: random/cluster/border/row/column/diagonal
  * caller-opt-in degenerates: monochrome, empty, single_cell
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4b787be81422"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "4b787be81422"
SUMMARY = "A binary grid; the rule emits 1 × 1 output: 1 if LR-symmetric, else 7."

INVARIANTS = [
    "input is a small rectangular grid",
    "exactly two colors appear (bg=0 and one fg)",
    "samples include both symmetric and asymmetric grids",
]

HELPFUL_PATTERNS = ("random", "cluster", "border", "row", "column", "diagonal")
DEGENERATE_TEXTURES = ("monochrome", "empty", "single_cell")

AXES = {
    "grid_h":      {"type": "int",   "default": "rng 3..6", "valid": "3..8"},
    "grid_w":      {"type": "int",   "default": "rng 3..6", "valid": "3..8"},
    "symmetric":   {"type": "bool",  "default": "rng",      "valid": "true|false"},
    "fg_color":    {"type": "color", "default": "rng",      "valid": "1..9"},
    "fg_density":  {"type": "float", "default": "rng 0.25..0.65", "valid": "0.1..0.9"},
    "pattern":     {"type": "str",   "default": "rng helpful",
                    "valid": "|".join(HELPFUL_PATTERNS)},
    "texture":     {"type": "str",   "default": "alias for pattern",
                    "valid": "|".join(HELPFUL_PATTERNS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 5, 7
    else:
        h_lo, h_hi = 3, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    make_sym = bool(overrides.get(
        "symmetric",
        ctx.draw_choice("symmetric", [True, False])))
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    density = float(overrides.get(
        "fg_density",
        ctx.draw_rng("fg_density").uniform(0.25, 0.65)))
    pattern = (overrides.get("texture")
               or overrides.get("pattern")
               or ctx.draw_choice("pattern", list(HELPFUL_PATTERNS)))

    g = full_grid(h, w, 0)
    half_w = w // 2 + (w % 2)  # cells in left half (incl. middle if odd)
    if pattern == "random":
        for r in range(h):
            for c in range(half_w):
                if rng.random() < density:
                    g[r][c] = fg
    elif pattern == "cluster":
        cr = rng.randint(0, h - 1)
        cc = rng.randint(0, half_w - 1)
        for r in range(h):
            for c in range(half_w):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density:
                    g[r][c] = fg
    elif pattern == "border":
        for c in range(half_w):
            g[0][c] = fg
            g[h - 1][c] = fg
        for r in range(h):
            g[r][0] = fg
    elif pattern == "row":
        r = rng.randint(0, h - 1)
        for c in range(half_w):
            if rng.random() < density:
                g[r][c] = fg
    elif pattern == "column":
        c = rng.randint(0, half_w - 1)
        for r in range(h):
            if rng.random() < density:
                g[r][c] = fg
    elif pattern == "diagonal":
        for k in range(min(h, half_w)):
            g[k][k] = fg

    # Mirror left → right (always; produces symmetric).
    for r in range(h):
        for c in range(w // 2):
            g[r][w - 1 - c] = g[r][c]

    is_sym = all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))
    if make_sym:
        return g

    # Need to break symmetry: flip one off-axis cell.
    if is_sym:
        for r in range(h):
            for c in range(w // 2):  # strictly off-axis
                g[r][c] = 0 if g[r][c] == fg else fg
                # Verify asymmetry now exists.
                if any(g[rr][cc] != g[rr][w - 1 - cc]
                       for rr in range(h) for cc in range(w)):
                    return g
    return g


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the LR-symmetry decision is hidden.

    monochrome  — uniform input is trivially symmetric → output 1.
    empty       — all-bg input is also trivially symmetric.
    single_cell — one fg cell, possibly off-axis → trivially asymmetric.
    """
    fg = ctx.draw_color("fg_color", exclude={0})
    g = full_grid(h, w, 0)
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    if name == "empty":
        return g
    if name == "single_cell":
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if c == w - 1 - c and w > 1:
            c = c - 1 if c > 0 else c + 1
        g[r][c] = fg
        return g
    return g
