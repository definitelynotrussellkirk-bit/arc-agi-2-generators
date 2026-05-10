"""Generator for ARC task 952a094c.

Rule: a single solid rectangle of one color in a uniform-color grid;
the four inside-corner cells of the rectangle have four distinct
non-rect colors. The rule clears the inside corners and places those
same colors at the corresponding diagonally-opposite OUTSIDE corners.

Invariants — see INVARIANTS list.

This is the worked-example puzzle in docs/PUZZLE_GENERATOR_SPEC.md.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "e6cf1120a17d"
VERSION = "1.0.0"
TASK_ID = "e6cf1120a17d"
SUMMARY = (
    "A single solid rectangle of one color in a uniform-color grid; "
    "the four inside-corner cells of the rectangle have four distinct "
    "non-rect colors."
)

INVARIANTS = [
    "exactly one solid rectangle of color rect_color",
    "the rectangle's 4 inside-corner cells have 4 distinct non-rect colors",
    "background is uniform color bg, distinct from rect_color and corner colors",
    "rectangle has at least 1 cell of margin from every grid edge",
    "rectangle dimensions: at least 5x5 (so inside-corner cells are well-defined)",
]

AXES = {
    "bg":            {"type": "color",     "default": "rng",         "valid": "0..9"},
    "rect_color":    {"type": "color",     "default": "rng",         "valid": "0..9 != bg"},
    "corner_colors": {"type": "colors[4]", "default": "rng_distinct",
                      "valid": "0..9 distinct, != bg, != rect_color"},
    # Wider grid range than v1.0.0 — gives the difficulty scorer room to
    # span [easy, hard]. With grid in [7..28], log-area / log(900) varies
    # from ~0.59 (7×7) to ~0.99 (28×28).
    "grid_h":        {"type": "int",       "default": "rng 7..28",   "valid": "7..30"},
    "grid_w":        {"type": "int",       "default": "rng 7..28",   "valid": "7..30"},
    "rect_h":        {"type": "int",       "default": "rng 5..h-3",  "valid": ">=5, <= h-2"},
    "rect_w":        {"type": "int",       "default": "rng 5..w-3",  "valid": ">=5, <= w-2"},
    "rect_rr":       {"type": "int",       "default": "rng with margin",
                      "valid": "1..h-rect_h-1"},
    "rect_rc":       {"type": "int",       "default": "rng with margin",
                      "valid": "1..w-rect_w-1"},
    # When `difficulty="easy"|"hard"`, the generator narrows the grid
    # range to the bottom or top half of the legal range. None = full range.
    "difficulty":    {"type": "enum",      "default": "None",
                      "valid": "easy | medium | hard | None"},
}


VERSION = "1.1.0"


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    bg          = ctx.draw_color("bg")
    rect_color  = ctx.draw_color("rect_color", exclude={bg})
    corners     = ctx.draw_distinct_colors("corner_colors", n=4,
                                            exclude={bg, rect_color})
    # Difficulty narrows the grid range so this one generator naturally
    # spans the score space.
    if difficulty == "easy":
        h_lo, h_hi = 7, 11
    elif difficulty == "hard":
        h_lo, h_hi = 20, 28
    else:
        h_lo, h_hi = 7, 28
    h           = ctx.draw_int("grid_h", h_lo, h_hi)
    w           = ctx.draw_int("grid_w", h_lo, h_hi)
    rh          = ctx.draw_int("rect_h", 5, h - 3)
    rw          = ctx.draw_int("rect_w", 5, w - 3)
    rr          = ctx.draw_int("rect_rr", 1, h - rh - 1)
    rc          = ctx.draw_int("rect_rc", 1, w - rw - 1)

    g = full_grid(h, w, bg)
    draw_rect(g, rr, rc, rh, rw, rect_color)
    g[rr + 1     ][rc + 1     ] = corners[0]   # top-left inside
    g[rr + 1     ][rc + rw - 2] = corners[1]   # top-right inside
    g[rr + rh - 2][rc + 1     ] = corners[2]   # bottom-left inside
    g[rr + rh - 2][rc + rw - 2] = corners[3]   # bottom-right inside
    return g
