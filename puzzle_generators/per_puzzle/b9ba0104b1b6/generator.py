"""Generator for ARC task 1cf80156.

Rule: `(rule! crop-to-content)`.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * shape_h / shape_w   — bbox of the inner foreground shape
  * shape_kind          — what fills the bbox (rect / L / hollow_ring / random_blob /
                          line_h / line_v / cross / single_pixel / scatter)
  * fg_color            — color of the shape
  * fill_density        — fraction of bbox cells colored (for blob/scatter shapes)
  * shape_pos           — top-left of the shape in the canvas
  * texture overrides   — degenerates `fills_grid` and `single_cell` hide the crop
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9ba0104b1b6"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "b9ba0104b1b6"
SUMMARY = "A single colored shape embedded in black padding; the rule crops to it."

INVARIANTS = [
    "background is zero",
    "there is exactly one foreground color",
    "shape's bbox is smaller than the grid in at least one dimension (else degenerate)",
]

# 9 helpful shape_kinds, each producing a structurally different fg footprint.
# crop-to-content's bbox extracts the same shape regardless of kind, but the
# model sees diverse intra-bbox patterns (filled vs hollow vs sparse vs linear).
HELPFUL_SHAPE_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "line_h", "line_v", "cross", "scatter", "diagonal",
)
DEGENERATE_TEXTURES = ("fills_grid", "single_cell")

AXES = {
    "grid_h":     {"type": "int",   "default": "rng 5..25", "valid": "4..30"},
    "grid_w":     {"type": "int",   "default": "rng 5..25", "valid": "4..30"},
    "shape_h":    {"type": "int",   "default": "rng 2..min(grid_h-2,15)", "valid": "1..grid_h"},
    "shape_w":    {"type": "int",   "default": "rng 2..min(grid_w-2,15)", "valid": "1..grid_w"},
    "shape_kind": {"type": "str",   "default": "rng helpful",
                   "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
    "fg_color":   {"type": "color", "default": "rng",       "valid": "1..9"},
    "fill_density": {"type": "float", "default": "rng 0.30..0.85",
                     "valid": "0.10..1.00 (fraction of bbox cells colored)"},
    "padding_min": {"type": "int", "default": "rng 1..3",
                    "valid": "0..5 (min padding around shape on each side)"},
    "texture":    {"type": "str",   "default": "helpful only",
                   "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        g_lo, g_hi, s_lo, s_hi = 6, 10, 2, 4
    elif difficulty == "hard":
        g_lo, g_hi, s_lo, s_hi = 15, 25, 6, 12
    else:
        g_lo, g_hi, s_lo, s_hi = 5, 25, 2, 12

    h = ctx.draw_int("grid_h", g_lo, g_hi)
    w = ctx.draw_int("grid_w", g_lo, g_hi)
    fg = ctx.draw_color("fg_color", exclude={0})
    rng = ctx.draw_rng("shape")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, fg, rng)

    # Optional padding constraint: ensure shape has ≥padding_min cells of bg
    # on every side (default 1, can be widened for "thick padding" variants).
    pad = int(overrides.get("padding_min", ctx.draw_int("padding_min", 1, 3)))
    sh = ctx.draw_int("shape_h", s_lo, max(s_lo, min(s_hi, h - 2 * pad)))
    sw = ctx.draw_int("shape_w", s_lo, max(s_lo, min(s_hi, w - 2 * pad)))
    rr = ctx.draw_int("shape_r", pad, max(pad, h - sh - pad))
    rc = ctx.draw_int("shape_c", pad, max(pad, w - sw - pad))

    # Pick shape kind (controls bbox interior pattern).
    kind = overrides.get("shape_kind", ctx.draw_choice(
        "shape_kind", list(HELPFUL_SHAPE_KINDS)))
    density = float(overrides.get(
        "fill_density", ctx.draw_rng("fill_density").uniform(0.30, 0.85)))

    g = full_grid(h, w, 0)
    _paint_shape(g, kind, rr, rc, sh, sw, fg, density, rng)

    # Always force the four bbox corners so the bbox extent stays unambiguous
    # regardless of shape_kind (crop-to-content uses the bbox of all fg cells).
    g[rr][rc] = fg
    g[rr][rc + sw - 1] = fg
    g[rr + sh - 1][rc] = fg
    g[rr + sh - 1][rc + sw - 1] = fg
    return g


def _paint_shape(g, kind, rr, rc, sh, sw, fg, density, rng):
    """Paint shape `kind` into g[rr:rr+sh, rc:rc+sw] using color fg."""
    if kind == "rect":
        # Solid filled rectangle.
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = fg
    elif kind == "L_shape":
        # L: full first column + full last row.
        for dr in range(sh):
            g[rr + dr][rc] = fg
        for dc in range(sw):
            g[rr + sh - 1][rc + dc] = fg
    elif kind == "hollow_ring":
        # Just the perimeter of the bbox.
        for dc in range(sw):
            g[rr][rc + dc] = fg
            g[rr + sh - 1][rc + dc] = fg
        for dr in range(sh):
            g[rr + dr][rc] = fg
            g[rr + dr][rc + sw - 1] = fg
    elif kind == "random_blob":
        # Random sparse blob with given density.
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < density:
                    g[rr + dr][rc + dc] = fg
    elif kind == "line_h":
        # Single horizontal line, middle of bbox.
        mid = sh // 2
        for dc in range(sw):
            g[rr + mid][rc + dc] = fg
    elif kind == "line_v":
        # Single vertical line, middle of bbox.
        mid = sw // 2
        for dr in range(sh):
            g[rr + dr][rc + mid] = fg
    elif kind == "cross":
        # Plus-sign through bbox middle.
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            g[rr + mr][rc + dc] = fg
        for dr in range(sh):
            g[rr + dr][rc + mc] = fg
    elif kind == "scatter":
        # Sparse scatter (lower density), for "barely there" visual.
        d = max(0.20, density * 0.5)
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < d:
                    g[rr + dr][rc + dc] = fg
    elif kind == "diagonal":
        # Single diagonal stroke from top-left of bbox to bottom-right.
        n = min(sh, sw)
        for k in range(n):
            g[rr + k][rc + k] = fg
    else:
        # Unknown kind → rect fallback.
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = fg


def _draw_from_degenerate(name, h, w, fg, rng):
    """Edge-case input where the crop's effect is hidden.

    fills_grid  — the foreground shape touches all four borders, so
                  crop-to-content returns the same grid (output == input).
    single_cell — one foreground pixel; crop-to-content yields a 1x1 grid.
                  The signature is correct but visually subtle, easy to miss.
    """
    g = full_grid(h, w, 0)
    if name == "fills_grid":
        # Random fg cells but ensure all four borders touch fg.
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = fg
        # Force corners + edge midpoints to fg.
        g[0][0] = fg
        g[0][w - 1] = fg
        g[h - 1][0] = fg
        g[h - 1][w - 1] = fg
        g[0][w // 2] = fg
        g[h - 1][w // 2] = fg
        return g
    if name == "single_cell":
        rr = rng.randrange(h)
        rc = rng.randrange(w)
        g[rr][rc] = fg
        return g
    return g
