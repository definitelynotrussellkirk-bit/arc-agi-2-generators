"""Generator for ARC task 1f85a75f.

Rule: `(rule! (lambda (g) (crop-object g (largest-object g))))`. Find
the largest connected component (excluding bg=0); crop the grid to its
bbox.

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * largest_kind           — shape of the dominant object
  * largest_h / largest_w  — bbox of the dominant object
  * n_distractors          — number of other objects (1..5)
  * distractor_size_dist   — size mix: tiny / mixed / close
  * placement              — random / center / corner / left_half
  * obj_color              — color of the dominant object
  * caller-opt-in degenerates: ties_for_largest, single_object,
                               distractors_inside_largest_bbox
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "5dedfc297cf5"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "5dedfc297cf5"
SUMMARY = "Several separated colored objects; the rule crops to the largest object's bbox."

INVARIANTS = [
    "background is zero",
    "≥2 non-overlapping objects",
    "largest object is strictly larger than 2nd-largest",
    "all objects fit inside the grid with margin ≥1",
]

LARGEST_KINDS = (
    "rect", "L_shape", "hollow_ring", "random_blob",
    "cross", "line_h", "line_v",
)
DISTRACTOR_SHAPES = ("rect", "single", "line_h", "line_v", "L_shape")
SIZE_DISTRIBUTIONS = ("tiny", "mixed", "close")
PLACEMENTS = ("random", "left_half", "center", "corner")
DEGENERATE_TEXTURES = ("ties_for_largest", "single_object")
HELPFUL_TEXTURES = LARGEST_KINDS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 11..18", "valid": "10..25"},
    "grid_w":          {"type": "int", "default": "rng 11..18", "valid": "10..25"},
    "largest_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(LARGEST_KINDS)},
    "largest_h":       {"type": "int", "default": "rng 4..9",   "valid": "3..12"},
    "largest_w":       {"type": "int", "default": "rng 4..9",   "valid": "3..12"},
    "n_distractors":   {"type": "int", "default": "rng 1..4",   "valid": "1..6"},
    "distractor_size_dist": {"type": "str", "default": "rng tiny|mixed|close",
                             "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "placement":       {"type": "str", "default": "rng random|left_half|center|corner",
                        "valid": "|".join(PLACEMENTS)},
    "obj_color":       {"type": "color", "default": "rng",     "valid": "1..9"},
    "texture":         {"type": "str", "default": "alias for largest_kind",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi = 11, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 18
    else:
        h_lo, h_hi = 11, 18

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    kind = (overrides.get("texture")
            or overrides.get("largest_kind")
            or ctx.draw_choice("largest_kind", list(LARGEST_KINDS)))
    color = int(overrides.get("obj_color",
                              ctx.draw_color("obj_color", exclude={0})))
    lh = ctx.draw_int("largest_h", 4, min(9, h - 4))
    lw = ctx.draw_int("largest_w", 4, min(9, w // 2))
    n_dist = int(overrides.get("n_distractors",
                               ctx.draw_int("n_distractors", 1, 4)))
    placement = overrides.get(
        "placement",
        ctx.draw_choice("placement", list(PLACEMENTS)))
    size_dist = overrides.get(
        "distractor_size_dist",
        ctx.draw_choice("distractor_size_dist", list(SIZE_DISTRIBUTIONS)))

    g = full_grid(h, w, 0)
    lr, lc = _place_largest(placement, h, w, lh, lw, rng)
    _paint_object(g, kind, lr, lc, lh, lw, color, rng)
    largest_area = sum(1 for r in range(lr, lr + lh) for c in range(lc, lc + lw)
                       if g[r][c] == color)

    _plant_distractors(g, n_dist, color, size_dist, largest_area, rng,
                       largest_box=(lr, lc, lr + lh - 1, lc + lw - 1))
    return g


def _place_largest(placement, h, w, lh, lw, rng):
    if placement == "left_half":
        return (rng.randint(1, h - lh - 1),
                rng.randint(1, max(1, (w // 2) - lw - 1)))
    if placement == "center":
        return ((h - lh) // 2, (w - lw) // 2)
    if placement == "corner":
        corners = [(1, 1), (1, w - lw - 1),
                   (h - lh - 1, 1), (h - lh - 1, w - lw - 1)]
        return rng.choice(corners)
    return (rng.randint(1, h - lh - 1),
            rng.randint(1, w - lw - 1))


def _paint_object(g, kind, rr, rc, sh, sw, color, rng):
    if kind == "rect":
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color
    elif kind == "L_shape":
        for dr in range(sh):
            g[rr + dr][rc] = color
        for dc in range(sw):
            g[rr + sh - 1][rc + dc] = color
    elif kind == "hollow_ring":
        for dc in range(sw):
            g[rr][rc + dc] = color
            g[rr + sh - 1][rc + dc] = color
        for dr in range(sh):
            g[rr + dr][rc] = color
            g[rr + dr][rc + sw - 1] = color
    elif kind == "random_blob":
        for dr in range(sh):
            for dc in range(sw):
                if rng.random() < 0.65:
                    g[rr + dr][rc + dc] = color
        # corners pinned for stable bbox
        g[rr][rc] = color
        g[rr][rc + sw - 1] = color
        g[rr + sh - 1][rc] = color
        g[rr + sh - 1][rc + sw - 1] = color
    elif kind == "cross":
        mr, mc = sh // 2, sw // 2
        for dc in range(sw):
            g[rr + mr][rc + dc] = color
        for dr in range(sh):
            g[rr + dr][rc + mc] = color
    elif kind == "line_h":
        for dc in range(sw):
            g[rr][rc + dc] = color
    elif kind == "line_v":
        for dr in range(sh):
            g[rr + dr][rc] = color
    else:
        for dr in range(sh):
            for dc in range(sw):
                g[rr + dr][rc + dc] = color


def _plant_distractors(g, n, dom_color, size_dist, largest_area, rng,
                       largest_box):
    h, w = len(g), len(g[0])
    if size_dist == "close":
        max_size = max(2, int(largest_area * 0.7))
    elif size_dist == "tiny":
        max_size = 2
    else:
        max_size = max(2, int(largest_area * 0.4))

    other_colors = [c for c in range(1, 10) if c != dom_color]
    rng.shuffle(other_colors)
    lr1, lc1, lr2, lc2 = largest_box

    placed = 0
    for i in range(n):
        for _try in range(20):
            ds = rng.randint(1, max_size)
            dh = max(1, min(rng.randint(1, ds + 1), h - 2))
            dw = max(1, min(max(1, ds // max(dh, 1)), w - 2))
            rr = rng.randint(1, max(1, h - dh - 1))
            rc = rng.randint(1, max(1, w - dw - 1))
            # Exclude largest object's bbox to keep cropping clean.
            if not (rr > lr2 + 1 or rr + dh < lr1 - 1
                    or rc > lc2 + 1 or rc + dw < lc1 - 1):
                continue
            collide = False
            for r in range(max(0, rr - 1), min(h, rr + dh + 1)):
                for c in range(max(0, rc - 1), min(w, rc + dw + 1)):
                    if g[r][c] != 0:
                        collide = True; break
                if collide:
                    break
            if collide:
                continue
            color = other_colors[i % len(other_colors)] if other_colors else 1
            for r in range(rr, rr + dh):
                for c in range(rc, rc + dw):
                    g[r][c] = color
            placed += 1
            break


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the largest-object signature collapses.

    ties_for_largest — two objects of identical area; tie-break is
                       implementation-dependent.
    single_object    — only one foreground object; the "largest" is
                       trivially that object — no rule signal.
    """
    g = full_grid(h, w, 0)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    if name == "ties_for_largest":
        size = 4
        draw_rect(g, 1, 1, size, size, colors[0])
        draw_rect(g, 1, w - size - 1, size, size, colors[1])
        draw_rect(g, h - 3, max(1, w // 2 - 1), 2, 2, colors[2])
        return g
    if name == "single_object":
        size = rng.randint(3, max(3, min(7, h - 2, w - 2)))
        draw_rect(g, 1, 1, size, size, colors[0])
        return g
    return g
