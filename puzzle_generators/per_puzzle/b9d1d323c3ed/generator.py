"""Generator for puzzle 28bf18c6.

Rule: find non-zero color; output is bh × (bw*2) where each cell is the
input cell at (r1+r, c1+(c%bw)). i.e. bbox of non-bg cells, tiled
horizontally twice.

Combinatorial axes (8): grid_h/w, fg_color, bbox_size_kind,
fg_density, bbox_position_bias, fg_layout, palette_purity,
inter_cell_padding.
Degenerates: single_cell, full_grid, no_fg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9d1d323c3ed"
VERSION = "1.1.0"
TASK_ID = "b9d1d323c3ed"
SUMMARY = "Sparse single-color cells; rule extracts bbox + tiles horizontally."

INVARIANTS = [
    "background is 0",
    "exactly one non-bg color used (rule's find-first picks unambiguously)",
    "bbox dims >= 2 × 2",
    "bbox is fully contained inside the grid",
    "non-bg cells span the full bbox (corners painted)",
]

FG_LAYOUTS = ("scattered", "blob", "diagonal", "frame",
              "row", "col", "checker")
BBOX_SIZE_KINDS = ("small", "medium", "large")
DEGENERATE_TEXTURES = ("single_cell", "full_grid", "no_fg")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..14", "valid": "4..18"},
    "grid_w":             {"type": "int", "default": "rng 5..14", "valid": "4..18"},
    "fg_color":           {"type": "color", "default": "rng (≠0)",
                           "valid": "1..9"},
    "bbox_size_kind":     {"type": "str", "default": "rng small|medium|large",
                           "valid": "|".join(BBOX_SIZE_KINDS)},
    "fg_density":         {"type": "float", "default": "rng 0.4..0.7",
                           "valid": "0.1..1"},
    "bbox_position_bias": {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "fg_layout":          {"type": "str", "default": "rng helpful",
                           "valid": "|".join(FG_LAYOUTS)},
    "palette_purity":     {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for fg_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg_color = int(overrides.get("fg_color",
                                 ctx.draw_color("fg_color", exclude={0})))
    size_kind = overrides.get("bbox_size_kind",
                              ctx.draw_choice("bbox_size_kind",
                                              list(BBOX_SIZE_KINDS)))
    if size_kind == "small":
        bh = rng.randint(2, max(2, h // 4))
        bw = rng.randint(2, max(2, w // 4))
    elif size_kind == "large":
        bh = rng.randint(max(3, h // 2), max(3, 2 * h // 3))
        bw = rng.randint(max(3, w // 2), max(3, 2 * w // 3))
    else:
        bh = rng.randint(max(2, h // 4), max(3, h // 2))
        bw = rng.randint(max(2, w // 4), max(3, w // 2))
    bh = max(2, min(h, bh))
    bw = max(2, min(w, bw))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    bias = overrides.get("bbox_position_bias",
                         ctx.draw_choice("bbox_position_bias",
                                         ["spread", "center", "edge"]))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density")
                                  .uniform(0.4, 0.7)))
    if bias == "center":
        rr = max(0, (h - bh) // 2)
        rc = max(0, (w - bw) // 2)
    elif bias == "edge":
        rr = rng.choice([0, h - bh])
        rc = rng.choice([0, w - bw])
    else:
        rr = rng.randint(0, h - bh)
        rc = rng.randint(0, w - bw)
    g = full_grid(h, w, 0)
    g[rr][rc] = fg_color
    g[rr + bh - 1][rc + bw - 1] = fg_color
    g[rr][rc + bw - 1] = fg_color if layout in ("frame", "checker") else g[rr][rc + bw - 1]
    _fill_bbox(g, layout, rr, rc, bh, bw, fg_color, density, rng)
    return g


def _fill_bbox(g, layout, rr, rc, bh, bw, color, density, rng):
    if layout == "blob":
        cr = rr + bh // 2; cc = rc + bw // 2
        for r in range(rr, rr + bh):
            for c in range(rc, rc + bw):
                if abs(r - cr) + abs(c - cc) <= max(2, (bh + bw) // 4) \
                        and rng.random() < density + 0.2:
                    g[r][c] = color
    elif layout == "diagonal":
        for k in range(min(bh, bw)):
            g[rr + k][rc + k] = color
    elif layout == "frame":
        for r in range(rr, rr + bh):
            g[r][rc] = color
            g[r][rc + bw - 1] = color
        for c in range(rc, rc + bw):
            g[rr][c] = color
            g[rr + bh - 1][c] = color
    elif layout == "row":
        target_r = rr + rng.randint(0, bh - 1)
        for c in range(rc, rc + bw):
            g[target_r][c] = color
    elif layout == "col":
        target_c = rc + rng.randint(0, bw - 1)
        for r in range(rr, rr + bh):
            g[r][target_c] = color
    elif layout == "checker":
        for r in range(rr, rr + bh):
            for c in range(rc, rc + bw):
                if (r + c) % 2 == 0:
                    g[r][c] = color
    else:
        for r in range(rr, rr + bh):
            for c in range(rc, rc + bw):
                if rng.random() < density:
                    g[r][c] = color


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_cell":
        g[h // 2][w // 2] = color
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "no_fg":
        return g
    return g
