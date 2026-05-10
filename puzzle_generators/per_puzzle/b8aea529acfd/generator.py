"""Generator for ARC task 7468f01a.

Rule: `(rule! (lambda (g) (flip-lr (crop-to-content g))))`. Crop to the
non-bg bounding box, then flip horizontally.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * shape_h / shape_w   — bbox of the inner shape
  * shape_kind          — what fills the bbox (rect/L/hollow_ring/random_blob/
                          line_h/line_v/cross/scatter/diagonal)
  * fg_palette_size     — how many distinct fg colors (1..3)
  * fill_density        — fraction of bbox cells colored (for blob/scatter)
  * padding_min         — min bg cells around the shape
  * caller-opt-in degenerates: lr_symmetric (flip is no-op), fills_grid,
                               single_cell
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b8aea529acfd"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "b8aea529acfd"
SUMMARY = "A padded foreground shape on black; the rule crops it and flips it horizontally."

INVARIANTS = [
    "background is zero",
    "foreground occupies a bounded rectangle with padding around it",
    "the crop is horizontally asymmetric (flip has visible effect)",
]

HELPFUL_SHAPE_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "line_h", "line_v", "cross", "scatter", "diagonal",
)
DEGENERATE_TEXTURES = ("lr_symmetric", "fills_grid", "single_cell")

AXES = {
    "grid_h":       {"type": "int",   "default": "rng 7..18", "valid": "4..30"},
    "grid_w":       {"type": "int",   "default": "rng 8..18", "valid": "4..30"},
    "shape_h":      {"type": "int",   "default": "rng 3..min(grid_h-2,9)",
                     "valid": "2..grid_h"},
    "shape_w":      {"type": "int",   "default": "rng 3..min(grid_w-2,9)",
                     "valid": "2..grid_w"},
    "shape_kind":   {"type": "str",   "default": "rng helpful",
                     "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
    "fg_palette_size": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "fill_density": {"type": "float", "default": "rng 0.30..0.85",
                     "valid": "0.10..1.00"},
    "padding_min":  {"type": "int",   "default": "rng 1..3", "valid": "0..5"},
    "texture":      {"type": "str",   "default": "alias for shape_kind",
                     "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        g_lo, g_hi, s_lo, s_hi = 7, 10, 3, 5
    elif difficulty == "hard":
        g_lo, g_hi, s_lo, s_hi = 14, 18, 6, 9
    else:
        g_lo, g_hi, s_lo, s_hi = 7, 18, 3, 9

    h = ctx.draw_int("grid_h", g_lo, g_hi)
    w = ctx.draw_int("grid_w", g_lo, g_hi)
    rng = ctx.draw_rng("shape")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    pad = int(overrides.get("padding_min",
                            ctx.draw_int("padding_min", 1, 3)))
    sh = ctx.draw_int("shape_h", s_lo, max(s_lo, min(s_hi, h - 2 * pad)))
    sw = ctx.draw_int("shape_w", s_lo, max(s_lo, min(s_hi, w - 2 * pad)))
    rr = ctx.draw_int("shape_r", pad, max(pad, h - sh - pad))
    rc = ctx.draw_int("shape_c", pad, max(pad, w - sw - pad))

    n_palette = ctx.draw_int("fg_palette_size", 1, 3)
    palette = ctx.draw_distinct_colors("palette", n=n_palette, exclude={0})
    kind = (overrides.get("texture")
            or overrides.get("shape_kind")
            or ctx.draw_choice("shape_kind", list(HELPFUL_SHAPE_KINDS)))
    density = float(overrides.get(
        "fill_density",
        ctx.draw_rng("fill_density").uniform(0.30, 0.85)))

    g = full_grid(h, w, 0)
    _paint_shape(g, kind, rr, rc, sh, sw, palette, density, rng)

    # Pin the four bbox corners so crop dims are stable regardless of kind.
    g[rr][rc] = palette[0]
    g[rr][rc + sw - 1] = palette[-1]
    g[rr + sh - 1][rc] = palette[0]
    g[rr + sh - 1][rc + sw - 1] = palette[-1]

    # Force LR-asymmetry: if the crop is left-right symmetric, perturb
    # one off-axis cell so the flip has visible effect.
    if _is_lr_symmetric(g, rr, rc, sh, sw):
        if sw > 1:
            g[rr][rc] = palette[-1]
            if _is_lr_symmetric(g, rr, rc, sh, sw):
                g[rr + sh - 1][rc + 1 if sw > 2 else rc] = palette[0]
    return g


def _is_lr_symmetric(g, rr, rc, sh, sw):
    for dr in range(sh):
        for dc in range(sw // 2):
            if g[rr + dr][rc + dc] != g[rr + dr][rc + sw - 1 - dc]:
                return False
    return True


def _paint_shape(g, kind, rr, rc, sh, sw, palette, density, rng):
    fg = palette[0]
    if kind == "rect":
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = rng.choice(palette)
    elif kind == "L_shape":
        for dr in range(sh):
            g[rr + dr][rc] = fg
        for dc in range(sw):
            g[rr + sh - 1][rc + dc] = palette[-1]
    elif kind == "hollow_ring":
        for dc in range(sw):
            g[rr][rc + dc] = fg
            g[rr + sh - 1][rc + dc] = palette[-1]
        for dr in range(sh):
            g[rr + dr][rc] = fg
            g[rr + dr][rc + sw - 1] = palette[-1]
    elif kind == "random_blob":
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < density:
                    g[rr + dr][rc + dc] = rng.choice(palette)
    elif kind == "line_h":
        mid = sh // 2
        for dc in range(sw):
            g[rr + mid][rc + dc] = rng.choice(palette)
    elif kind == "line_v":
        mid = sw // 2
        for dr in range(sh):
            g[rr + dr][rc + mid] = rng.choice(palette)
    elif kind == "cross":
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            g[rr + mr][rc + dc] = fg
        for dr in range(sh):
            g[rr + dr][rc + mc] = palette[-1]
    elif kind == "scatter":
        d = max(0.20, density * 0.5)
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < d:
                    g[rr + dr][rc + dc] = rng.choice(palette)
    elif kind == "diagonal":
        for k in range(min(sh, sw)):
            g[rr + k][rc + k] = palette[k % len(palette)]
    else:
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = fg


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the crop+flip signature is hidden.

    lr_symmetric — shape is already LR-symmetric, so the flip is invisible.
    fills_grid   — non-bg touches all four borders, so crop = identity
                   and the flip just reflects the whole grid.
    single_cell  — one fg pixel; crop = 1×1 and flip is invisible.
    """
    g = full_grid(h, w, 0)
    palette = [c for c in [1, 2, 3, 4, 6, 8, 9] if c]
    rng.shuffle(palette)
    if name == "lr_symmetric":
        sh = max(3, h // 3); sw = max(3, w // 3)
        rr = rng.randint(1, h - sh - 1)
        rc = rng.randint(1, w - sw - 1)
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < 0.5:
                    pick = rng.choice(palette[:3])
                    g[rr + dr][rc + dc] = pick
                    g[rr + dr][rc + sw - 1 - dc] = pick
        # Force corners to ensure bbox extent.
        g[rr][rc] = palette[0]
        g[rr][rc + sw - 1] = palette[0]
        g[rr + sh - 1][rc] = palette[1]
        g[rr + sh - 1][rc + sw - 1] = palette[1]
        return g
    if name == "fills_grid":
        fg = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = fg
        g[0][0] = fg; g[0][w - 1] = fg
        g[h - 1][0] = fg; g[h - 1][w - 1] = fg
        g[0][w // 2] = fg; g[h - 1][w // 2] = fg
        return g
    if name == "single_cell":
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        g[r][c] = palette[0]
        return g
    return g
