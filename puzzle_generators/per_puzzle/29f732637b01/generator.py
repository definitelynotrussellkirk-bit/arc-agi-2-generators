"""Generator for puzzle f25fbde4 — `(rule! (lambda (g) (upscale (crop-to-content g) 2)))`.

Crop the grid to the non-bg bounding box, then upscale by 2 ×.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * shape_h / shape_w   — bbox of the inner shape (cropped output is sh×sw,
                          upscaled output is 2sh × 2sw, must be ≤ 30)
  * shape_kind          — what fills the bbox: rect/L/hollow_ring/random_blob/
                          line_h/line_v/cross/scatter/diagonal
  * fg_palette_size     — distinct fg colors (1..3)
  * fill_density        — fraction of bbox cells colored
  * padding_min         — min bg cells around shape on each side
  * caller-opt-in degenerates: fills_grid (crop = identity), single_cell
                               (output is 2 × 2), monochrome
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "29f732637b01"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "29f732637b01"
SUMMARY = "Sparse non-bg content with bg padding; rule crops to content and upscales 2 ×."

INVARIANTS = [
    "background is 0",
    "≥1 non-bg cell",
    "non-bg content has ≥1 bg margin so cropping shrinks the grid",
    "cropped bbox ≤ 15 × 15 so 2× upscale stays ≤ 30 × 30",
]

HELPFUL_SHAPE_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "line_h", "line_v", "cross", "scatter", "diagonal",
)
DEGENERATE_TEXTURES = ("fills_grid", "single_cell", "monochrome")

AXES = {
    "grid_h":          {"type": "int",   "default": "rng 7..16", "valid": "5..20"},
    "grid_w":          {"type": "int",   "default": "rng 7..16", "valid": "5..20"},
    "shape_h":         {"type": "int",   "default": "rng 2..min(grid_h-2,8)",
                        "valid": "1..15"},
    "shape_w":         {"type": "int",   "default": "rng 2..min(grid_w-2,8)",
                        "valid": "1..15"},
    "shape_kind":      {"type": "str",   "default": "rng helpful",
                        "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
    "fg_palette_size": {"type": "int",   "default": "rng 1..3", "valid": "1..5"},
    "fill_density":    {"type": "float", "default": "rng 0.30..0.85", "valid": "0.10..1.00"},
    "padding_min":     {"type": "int",   "default": "rng 1..3", "valid": "1..5"},
    "texture":         {"type": "str",   "default": "alias for shape_kind",
                        "valid": "|".join(HELPFUL_SHAPE_KINDS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        g_lo, g_hi, s_lo, s_hi = 7, 10, 2, 4
    elif difficulty == "hard":
        g_lo, g_hi, s_lo, s_hi = 13, 16, 5, 8
    else:
        g_lo, g_hi, s_lo, s_hi = 7, 16, 2, 8

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

    n_palette = int(overrides.get("fg_palette_size",
                                  ctx.draw_int("fg_palette_size", 1, 3)))
    palette = ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0})
    kind = (overrides.get("texture")
            or overrides.get("shape_kind")
            or ctx.draw_choice("shape_kind", list(HELPFUL_SHAPE_KINDS)))
    density = float(overrides.get(
        "fill_density",
        ctx.draw_rng("fill_density").uniform(0.30, 0.85)))

    g = full_grid(h, w, 0)
    _paint_shape(g, kind, rr, rc, sh, sw, palette, density, rng)

    # Pin the four bbox corners so the crop bbox extent is unambiguous.
    g[rr][rc] = palette[0]
    g[rr][rc + sw - 1] = palette[-1]
    g[rr + sh - 1][rc] = palette[0]
    g[rr + sh - 1][rc + sw - 1] = palette[-1]
    return g


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
    """Edge-case where the crop+upscale signal collapses.

    fills_grid  — non-bg touches all four borders → crop is identity,
                  output is 2 × upscaled whole grid.
    single_cell — one fg pixel; cropped bbox is 1 × 1, output 2 × 2 of
                  uniform color (visually trivial).
    monochrome  — every cell is fg color; same as fills_grid effectively.
    """
    g = full_grid(h, w, 0)
    palette = [c for c in range(1, 10)]
    rng.shuffle(palette)
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
        rr = rng.randint(1, h - 2)
        rc = rng.randint(1, w - 2)
        g[rr][rc] = palette[0]
        return g
    if name == "monochrome":
        color = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
