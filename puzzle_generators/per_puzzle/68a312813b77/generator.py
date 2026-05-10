"""Generator for ARC task 60b61512.

Rule: `(rule! (lambda (g) (fill-object-bboxes-8 g 7)))`. For each
8-connected non-bg object, fill its bounding box with color 7 (orange).

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * n_objects           — how many objects to plant (1..4)
  * object_kind         — shape: diagonal / L_shape / cross / Z_shape /
                          random_blob / hollow_ring / staircase
  * fg_color            — the color the objects are drawn in (≠ 0, ≠ 7)
  * size_distribution   — small / medium / large / mixed
  * placement           — random / corners / row / column
  * caller-opt-in degenerates: rect_object (already its own bbox), single_pixel,
                               touching_objects (overlapping bboxes)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "68a312813b77"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "68a312813b77"
SUMMARY = "Sparse non-rect 8-connected objects; the rule fills each bbox with 7."

INVARIANTS = [
    "background is zero",
    "foreground objects are 8-connected but not rectangular",
    "object bounding boxes don't overlap (so one bbox fill doesn't merge two objects)",
    "no object color is 7 (the fill color) — visible distinction in output",
]

OBJECT_KINDS = (
    "diagonal", "L_shape", "cross", "Z_shape",
    "random_blob", "hollow_ring", "staircase",
)
SIZE_DISTRIBUTIONS = ("small", "medium", "large", "mixed")
PLACEMENTS = ("random", "corners", "row", "column")
DEGENERATE_TEXTURES = ("rect_object", "single_pixel", "touching_objects")
HELPFUL_TEXTURES = OBJECT_KINDS

AXES = {
    "grid_h":            {"type": "int",   "default": "rng 8..15", "valid": "6..20"},
    "grid_w":            {"type": "int",   "default": "rng 8..15", "valid": "6..20"},
    "n_objects":         {"type": "int",   "default": "rng 1..3",  "valid": "1..5"},
    "object_kind":       {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(OBJECT_KINDS)},
    "fg_color":          {"type": "color", "default": "rng",       "valid": "1..9 (≠7)"},
    "size_distribution": {"type": "str",   "default": "rng small|medium|large|mixed",
                          "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "placement":         {"type": "str",   "default": "rng random|corners|row|column",
                          "valid": "|".join(PLACEMENTS)},
    "texture":           {"type": "str",   "default": "alias for object_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 8, 11, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 13, 15, 3, 4
    else:
        h_lo, h_hi, n_lo, n_hi = 8, 15, 1, 3

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    n_obj = int(overrides.get("n_objects",
                              ctx.draw_int("n_objects", n_lo, n_hi)))
    kind = (overrides.get("texture")
            or overrides.get("object_kind")
            or ctx.draw_choice("object_kind", list(OBJECT_KINDS)))
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0, 7})))
    size_dist = overrides.get(
        "size_distribution",
        ctx.draw_choice("size_distribution", list(SIZE_DISTRIBUTIONS)))
    placement = overrides.get(
        "placement",
        ctx.draw_choice("placement", list(PLACEMENTS)))

    g = full_grid(h, w, 0)
    placed_boxes: list[tuple[int, int, int, int]] = []

    anchors = _anchor_pool(placement, h, w, n_obj, rng)
    for anchor in anchors:
        for _ in range(20):
            sh, sw = _shape_dims(size_dist, h, w, rng)
            ar, ac = anchor
            ar = min(max(1, ar), max(1, h - sh - 1))
            ac = min(max(1, ac), max(1, w - sw - 1))
            box = (ar, ac, ar + sh - 1, ac + sw - 1)
            if any(_overlap_bbox(box, ob, gap=1) for ob in placed_boxes):
                continue
            cells = _shape_cells(kind, sh, sw, rng)
            for (dr, dc) in cells:
                g[ar + dr][ac + dc] = fg
            placed_boxes.append(box)
            break
    return g


def _anchor_pool(placement, h, w, n, rng):
    margin = 1
    if placement == "corners":
        return [(margin, margin), (margin, w - margin - 4),
                (h - margin - 4, margin), (h - margin - 4, w - margin - 4)][:n]
    if placement == "row":
        gap = max(1, (w - 2 * margin) // max(1, n))
        return [(rng.randint(margin, max(margin, h // 2)), margin + i * gap)
                for i in range(n)]
    if placement == "column":
        gap = max(1, (h - 2 * margin) // max(1, n))
        return [(margin + i * gap, rng.randint(margin, max(margin, w // 2)))
                for i in range(n)]
    return [(rng.randint(margin, max(margin, h - 5)),
             rng.randint(margin, max(margin, w - 5)))
            for _ in range(n)]


def _shape_dims(size_dist, h, w, rng):
    if size_dist == "small":
        return rng.randint(2, 3), rng.randint(2, 3)
    if size_dist == "medium":
        return rng.randint(3, 5), rng.randint(3, 5)
    if size_dist == "large":
        return rng.randint(5, max(5, h // 3)), rng.randint(5, max(5, w // 3))
    return rng.randint(2, max(3, h // 4)), rng.randint(2, max(3, w // 4))


def _overlap_bbox(a, b, gap=0):
    ar1, ac1, ar2, ac2 = a
    br1, bc1, br2, bc2 = b
    return not (ar2 + gap < br1 or br2 + gap < ar1
                or ac2 + gap < bc1 or bc2 + gap < ac1)


def _shape_cells(kind, sh, sw, rng):
    """Return list of (dr, dc) cells for `kind`. Bbox must be exactly sh × sw
    (touch all four sides) so the rule's bbox fill is non-degenerate."""
    if kind == "diagonal":
        n = min(sh, sw)
        return [(k * (sh - 1) // max(1, n - 1), k * (sw - 1) // max(1, n - 1))
                for k in range(n)] or [(0, 0)]
    if kind == "L_shape":
        out = [(r, 0) for r in range(sh)]
        out += [(sh - 1, c) for c in range(1, sw)]
        return out
    if kind == "cross":
        mr, mc = sh // 2, sw // 2
        out = [(mr, c) for c in range(sw)]
        out += [(r, mc) for r in range(sh) if r != mr]
        # Force corners-touch by adding both endpoints
        out += [(0, mc), (sh - 1, mc), (mr, 0), (mr, sw - 1)]
        return list(set(out))
    if kind == "Z_shape":
        out = [(0, c) for c in range(sw)]
        out += [(sh - 1, c) for c in range(sw)]
        # Diagonal middle
        for k in range(1, sh - 1):
            dc = k * (sw - 1) // max(1, sh - 1)
            out.append((k, dc))
        return out
    if kind == "hollow_ring":
        out = []
        for c in range(sw):
            out.append((0, c))
            out.append((sh - 1, c))
        for r in range(sh):
            out.append((r, 0))
            out.append((r, sw - 1))
        return list(set(out))
    if kind == "staircase":
        out = [(0, 0), (sh - 1, sw - 1)]
        for k in range(1, min(sh, sw) - 1):
            out.append((k, k))
        return out
    # random_blob — connected via 8-conn BFS, covers all bbox extents
    cells = {(0, 0), (sh - 1, sw - 1), (0, sw - 1), (sh - 1, 0)}
    while len(cells) < min(sh * sw, 2 * (sh + sw)):
        r = rng.randint(0, sh - 1)
        c = rng.randint(0, sw - 1)
        cells.add((r, c))
    return list(cells)


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the bbox-fill signature is hidden.

    rect_object       — the object IS already its bbox; rule has no
                        visible effect (object is just recolored).
    single_pixel      — 1×1 object; bbox fill is just that single cell.
    touching_objects  — two objects whose bboxes overlap; the rule
                        merges them into one fill region.
    """
    g = full_grid(h, w, 0)
    fg = ctx.draw_color("fg_color", exclude={0, 7})
    if name == "rect_object":
        rh, rw = max(2, h // 3), max(2, w // 3)
        rr = rng.randint(1, h - rh - 1)
        rc = rng.randint(1, w - rw - 1)
        for r in range(rr, rr + rh):
            for c in range(rc, rc + rw):
                g[r][c] = fg
        return g
    if name == "single_pixel":
        for _ in range(rng.randint(1, 3)):
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 2)
            g[r][c] = fg
        return g
    if name == "touching_objects":
        rh, rw = 3, 3
        rr = rng.randint(1, h - 6)
        rc = rng.randint(1, w - 6)
        for k in range(rh):
            g[rr + k][rc + k] = fg
        # Second object inside the first's bbox-extension.
        for k in range(rh):
            g[rr + k][rc + rw + k] = fg
        return g
    return g
