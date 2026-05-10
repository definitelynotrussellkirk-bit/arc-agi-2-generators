"""Generator for puzzle 23b5c85d.

Rule: `(rule! (lambda (g) (let* ((objs (objects g 2)) (smallest (pick-min objs obj-size))) (crop-object g smallest))))`.
With bg=2, find all 4-connected non-bg objects; pick the smallest;
crop the grid to that object's bbox.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * n_objects           — total non-bg objects (≥2 with strictly distinct sizes)
  * smallest_kind       — shape of the smallest: rect / cross / L / line
  * size_progression    — linear / exponential (controls relative sizes)
  * placement           — random / corners / row / column
  * caller-opt-in degenerates: ties_for_smallest (rule's tie-break is
                               implementation-dep), single_object,
                               all_same_size
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "c235e3da14f4"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "c235e3da14f4"
SUMMARY = "Multiple objects on bg=2; rule crops to the smallest object's bbox."

INVARIANTS = [
    "background is 2",
    "≥2 non-bg objects of strictly distinct sizes",
    "the smallest object is unique",
]

SMALLEST_KINDS = ("rect", "cross", "L_shape", "line_h", "line_v", "single_pixel")
SIZE_PROGRESSIONS = ("linear", "exponential")
PLACEMENTS = ("random", "corners", "row", "column")
DEGENERATE_TEXTURES = ("ties_for_smallest", "single_object", "all_same_size")
HELPFUL_TEXTURES = SMALLEST_KINDS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..18", "valid": "8..22"},
    "grid_w":          {"type": "int", "default": "rng 8..18", "valid": "8..22"},
    "n_objects":       {"type": "int", "default": "rng 2..4",  "valid": "2..6"},
    "smallest_kind":   {"type": "str", "default": "rng helpful",
                        "valid": "|".join(SMALLEST_KINDS)},
    "size_progression": {"type": "str", "default": "rng linear|exponential",
                         "valid": "|".join(SIZE_PROGRESSIONS)},
    "placement":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PLACEMENTS)},
    "texture":         {"type": "str", "default": "alias for smallest_kind",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 8, 11, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 15, 18, 3, 4
    else:
        h_lo, h_hi, n_lo, n_hi = 8, 18, 2, 4

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    n_obj = int(overrides.get("n_objects",
                              ctx.draw_int("n_objects", n_lo, n_hi)))
    n_obj = max(2, min(6, n_obj))
    smallest_kind = (overrides.get("texture")
                     or overrides.get("smallest_kind")
                     or ctx.draw_choice("smallest_kind", list(SMALLEST_KINDS)))
    progression = overrides.get(
        "size_progression",
        ctx.draw_choice("size_progression", list(SIZE_PROGRESSIONS)))
    placement = overrides.get(
        "placement",
        ctx.draw_choice("placement", list(PLACEMENTS)))

    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_obj), exclude={2}))
    sizes = _make_sizes(n_obj, progression, rng)  # ascending
    g = full_grid(h, w, 2)

    anchors = _anchors(placement, h, w, n_obj, rng)
    placed = 0
    for i, ((ar, ac), size, color) in enumerate(zip(anchors, sizes, palette)):
        for _ in range(20):
            sh, sw = _shape_dims_for_size(size, rng)
            if 0 <= ar < h - sh and 0 <= ac < w - sw and \
               _check_clear(g, ar, ac, sh, sw, bg=2):
                if i == 0:
                    _paint_kind(g, smallest_kind, ar, ac, sh, sw, color, rng)
                else:
                    draw_rect(g, ar, ac, sh, sw, color)
                placed += 1
                break
            ar = rng.randint(0, max(0, h - sh))
            ac = rng.randint(0, max(0, w - sw))
    if placed < 2:
        return [[2]]
    return g


def _make_sizes(n, progression, rng):
    """Return n strictly ascending positive sizes (smallest first)."""
    if progression == "linear":
        base = rng.randint(2, 3)
        return [base + i for i in range(n)]
    # exponential
    return [2 + 2 ** i for i in range(n)]


def _shape_dims_for_size(size, rng):
    s = max(2, size)
    return s, s


def _anchors(placement, h, w, n, rng):
    margin = 1
    if placement == "corners":
        cands = [(margin, margin), (margin, w - margin - 5),
                 (h - margin - 5, margin), (h - margin - 5, w - margin - 5)]
        return cands[:n]
    if placement == "row":
        gap = max(1, (w - 2 * margin) // max(1, n))
        return [(rng.randint(margin, h // 2), margin + i * gap) for i in range(n)]
    if placement == "column":
        gap = max(1, (h - 2 * margin) // max(1, n))
        return [(margin + i * gap, rng.randint(margin, w // 2)) for i in range(n)]
    return [(rng.randint(margin, max(margin, h - 6)),
             rng.randint(margin, max(margin, w - 6))) for _ in range(n)]


def _check_clear(g, rr, rc, sh, sw, bg):
    for r in range(max(0, rr - 1), min(len(g), rr + sh + 1)):
        for c in range(max(0, rc - 1), min(len(g[0]), rc + sw + 1)):
            if g[r][c] != bg:
                return False
    return True


def _paint_kind(g, kind, rr, rc, sh, sw, color, rng):
    if kind == "rect":
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color
    elif kind == "cross":
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            g[rr + mr][rc + dc] = color
        for dr in range(sh):
            g[rr + dr][rc + mc] = color
    elif kind == "L_shape":
        for dr in range(sh):
            g[rr + dr][rc] = color
        for dc in range(sw):
            g[rr + sh - 1][rc + dc] = color
    elif kind == "line_h":
        for dc in range(sw):
            g[rr][rc + dc] = color
    elif kind == "line_v":
        for dr in range(sh):
            g[rr + dr][rc] = color
    elif kind == "single_pixel":
        g[rr][rc] = color
    else:
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the smallest-object signal collapses.

    ties_for_smallest — two objects share the smallest size; rule's
                         tie-break is implementation-dependent.
    single_object     — only one object; rule trivially crops to it
                         (no "smallest" decision).
    all_same_size     — every object is the same size; the entire
                         "smallest" choice is ambiguous.
    """
    g = full_grid(h, w, 2)
    palette = list(ctx.draw_distinct_colors("palette", n=4, exclude={2}))
    if name == "ties_for_smallest":
        s = 2
        draw_rect(g, 1, 1, s, s, palette[0])
        draw_rect(g, 1, w - s - 1, s, s, palette[1])
        draw_rect(g, h - 5, max(1, w // 2 - 1), 4, 4, palette[2])
        return g
    if name == "single_object":
        s = rng.randint(3, 5)
        draw_rect(g, 1, 1, s, s, palette[0])
        return g
    if name == "all_same_size":
        s = 3
        anchors = [(1, 1), (1, w - s - 1), (h - s - 1, 1), (h - s - 1, w - s - 1)]
        for i, (r, c) in enumerate(anchors[:4]):
            draw_rect(g, r, c, s, s, palette[i % len(palette)])
        return g
    return g
