"""Generator for ARC task 22425bda — z-order of crossing lines on bg=7.

Rule: bg=7. Two crossing lines (1 vertical + 1 horizontal) of distinct
colors. At intersection, the "front" color is shown. Output is a 1×2
grid: [back_color, front_color].

Combinatorial axes:
  * grid_size              — odd-side length of the square (5..13)
  * row_position           — which row the horizontal line lives on
  * col_position           — which col the vertical line lives on
  * row_color / col_color  — the two distinct line colors
  * front_choice           — which of the two is rendered at the crossing
  * extra_decor            — single-cell decoy dots that don't form lines
  * caller-opt-in degenerates: missing_intersection, third_line, same_color
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00af0f134576"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "00af0f134576"
SUMMARY = "bg=7; one full horizontal + one full vertical line of distinct colors crossing once."

INVARIANTS = [
    "bg = 7",
    "exactly one full row and one full col, both inside the grid",
    "row and col have distinct colors ≠ 7",
    "intersection cell is one of the two line colors (the 'front')",
]

HELPFUL_TEXTURES = ("plain", "with_decor")
DEGENERATE_TEXTURES = ("missing_intersection", "third_line", "same_color")
PALETTE = (1, 2, 3, 4, 5, 6, 8, 9)  # all colors except bg=7

AXES = {
    "grid_size":     {"type": "int",   "default": "rng 5..11 odd", "valid": "5..13"},
    "row_position":  {"type": "int",   "default": "rng 1..size-2", "valid": "1..size-2"},
    "col_position":  {"type": "int",   "default": "rng 1..size-2", "valid": "1..size-2"},
    "row_color":     {"type": "color", "default": "rng",           "valid": "1..9 (≠7)"},
    "col_color":     {"type": "color", "default": "rng (≠row)",    "valid": "1..9 (≠7, ≠row)"},
    "front_choice":  {"type": "str",   "default": "rng row|col",   "valid": "row|col"},
    "extra_decor":   {"type": "int",   "default": "rng 0..3",      "valid": "0..6"},
    "texture":       {"type": "str",   "default": "plain",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        s_lo, s_hi = 5, 7
    elif difficulty == "hard":
        s_lo, s_hi = 9, 13
    else:
        s_lo, s_hi = 5, 11

    s = ctx.draw_int("grid_size", s_lo, s_hi)
    if s % 2 == 0:
        s += 1
    rng = ctx.draw_rng("layout")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], s, rng)

    palette = list(PALETTE)
    rng.shuffle(palette)
    row_color = int(overrides.get("row_color", palette[0]))
    col_color = int(overrides.get("col_color",
                                  palette[1] if palette[1] != row_color else palette[2]))
    if col_color == row_color:
        col_color = next(c for c in palette if c != row_color)

    row_r = int(overrides.get("row_position", rng.randint(1, s - 2)))
    col_c = int(overrides.get("col_position", rng.randint(1, s - 2)))
    front = overrides.get(
        "front_choice",
        ctx.draw_choice("front_choice", ["row", "col"]))

    g = full_grid(s, s, 7)
    for c in range(s):
        g[row_r][c] = row_color
    for r in range(s):
        g[r][col_c] = col_color
    g[row_r][col_c] = row_color if front == "row" else col_color

    # Optional decor: stray cells of OTHER colors that don't span the grid
    # (so they aren't picked up as lines by the rule).
    n_decor = int(overrides.get(
        "extra_decor",
        ctx.draw_int("extra_decor", 0, 3)))
    decor_palette = [c for c in PALETTE if c not in {row_color, col_color}]
    placed = 0
    for _ in range(40):
        if placed >= n_decor:
            break
        r = rng.randint(0, s - 1)
        c = rng.randint(0, s - 1)
        # Skip cells on either of the two lines so they aren't extended.
        if r == row_r or c == col_c:
            continue
        if g[r][c] != 7:
            continue
        g[r][c] = rng.choice(decor_palette) if decor_palette else 7
        placed += 1
    return g


def _draw_from_degenerate(name, s, rng):
    """Edge-case where the line-z-order signature is hidden.

    missing_intersection — only one of the two lines is drawn, so there
                           is no crossing to disambiguate front/back.
    third_line          — three lines instead of two; the rule's
                           assumption of a single crossing breaks.
    same_color          — both lines share a color; the crossing is
                           visually indistinguishable.
    """
    g = full_grid(s, s, 7)
    palette = list(PALETTE)
    rng.shuffle(palette)
    if name == "missing_intersection":
        # Just one full line — front is meaningless.
        if rng.random() < 0.5:
            r = rng.randint(1, s - 2)
            for c in range(s):
                g[r][c] = palette[0]
        else:
            c = rng.randint(1, s - 2)
            for r in range(s):
                g[r][c] = palette[0]
        return g
    if name == "third_line":
        r1 = rng.randint(1, s - 2)
        r2 = (r1 + 2) % (s - 1) or 1
        c1 = rng.randint(1, s - 2)
        for c in range(s):
            g[r1][c] = palette[0]
            g[r2][c] = palette[1]
        for r in range(s):
            g[r][c1] = palette[2]
        return g
    if name == "same_color":
        color = palette[0]
        r = rng.randint(1, s - 2)
        c = rng.randint(1, s - 2)
        for cc in range(s):
            g[r][cc] = color
        for rr in range(s):
            g[rr][c] = color
        return g
    return g
