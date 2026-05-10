"""Generator for puzzle d5d6de2d.

Rule: `(rule! (lambda (g) (let ((filled (fill-all-enclosed g 3 0))) (recolor filled 2 0))))`.
Fill bg cells enclosed by outlines with green(3), then erase red(2)
outlines. End: outlines vanish, but the green interiors remain.

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * n_outlines             — how many enclosing red shapes to plant
  * frame_kind             — rect_outline / blob_outline / nested / U_shape /
                             irregular_polygon
  * size_distribution      — small / medium / large / mixed
  * decor_density          — extra non-bg, non-red, non-green cells
                             outside outlines (stay unchanged)
  * caller-opt-in degenerates: open_frame, no_outline, full_grid_outline
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "ee5ca325d03d"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "ee5ca325d03d"
SUMMARY = "Red outlines on a 0 bg; rule fills interior with green and erases the red outlines."

INVARIANTS = [
    "background is 0",
    "≥1 rectangular outline drawn in red(2)",
    "each outline encloses ≥1 bg cell",
    "outlines have bg margin from the grid edge",
]

HELPFUL_FRAME_KINDS = (
    "rect_outline", "blob_outline", "nested_rects", "U_shape", "irregular_polygon",
)
SIZE_DISTRIBUTIONS = ("small", "medium", "large", "mixed")
DEGENERATE_TEXTURES = ("open_frame", "no_outline", "full_grid_outline")

AXES = {
    "grid_h":            {"type": "int",   "default": "rng 10..18", "valid": "8..22"},
    "grid_w":            {"type": "int",   "default": "rng 10..18", "valid": "8..22"},
    "n_outlines":        {"type": "int",   "default": "rng 1..3",   "valid": "1..5"},
    "frame_kind":        {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(HELPFUL_FRAME_KINDS)},
    "size_distribution": {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "decor_density":     {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "texture":           {"type": "str",   "default": "alias for frame_kind",
                          "valid": "|".join(HELPFUL_FRAME_KINDS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 10, 12, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 16, 18, 2, 3
    else:
        h_lo, h_hi, n_lo, n_hi = 10, 18, 1, 3

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    n_outlines = int(overrides.get("n_outlines",
                                   ctx.draw_int("n_outlines", n_lo, n_hi)))
    frame_kind = (overrides.get("texture")
                  or overrides.get("frame_kind")
                  or ctx.draw_choice("frame_kind", list(HELPFUL_FRAME_KINDS)))
    size_dist = overrides.get(
        "size_distribution",
        ctx.draw_choice("size_distribution", list(SIZE_DISTRIBUTIONS)))

    g = full_grid(h, w, 0)
    placed_boxes: list[tuple[int, int, int, int]] = []
    for _ in range(n_outlines):
        for _try in range(40):
            fh, fw = _frame_dims(size_dist, h, w, rng)
            rr = rng.randint(2, max(2, h - fh - 2))
            rc = rng.randint(2, max(2, w - fw - 2))
            collide = False
            for (or1, oc1, or2, oc2) in placed_boxes:
                if (rr - 1 <= or2 and rr + fh >= or1
                        and rc - 1 <= oc2 and rc + fw >= oc1):
                    collide = True; break
            if collide:
                continue
            _draw_frame_kind(g, frame_kind, rr, rc, fh, fw, 2, rng)
            placed_boxes.append((rr, rc, rr + fh - 1, rc + fw - 1))
            break

    if not placed_boxes:
        draw_rect_outline(g, 2, 2, 4, 4, 2)

    decor = float(overrides.get(
        "decor_density",
        ctx.draw_rng("decor_density").uniform(0.0, 0.05)))
    if decor > 0.0:
        decor_palette = [c for c in range(10) if c not in {0, 2, 3}]
        for _ in range(max(1, int(h * w * decor))):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] == 0 and not _is_inside_any(r, c, placed_boxes):
                g[r][c] = rng.choice(decor_palette) if decor_palette else 0
    return g


def _is_inside_any(r, c, boxes):
    for (r1, c1, r2, c2) in boxes:
        if r1 <= r <= r2 and c1 <= c <= c2:
            return True
    return False


def _frame_dims(size_dist, h, w, rng):
    if size_dist == "small":
        return rng.randint(3, 5), rng.randint(3, 5)
    if size_dist == "medium":
        return rng.randint(5, max(5, h // 3)), rng.randint(5, max(5, w // 3))
    if size_dist == "large":
        return (rng.randint(max(5, h // 3), max(5, h // 2)),
                rng.randint(max(5, w // 3), max(5, w // 2)))
    return rng.randint(3, max(3, h // 3)), rng.randint(3, max(3, w // 3))


def _draw_frame_kind(g, kind, rr, rc, fh, fw, color, rng):
    if kind == "rect_outline":
        draw_rect_outline(g, rr, rc, fh, fw, color)
    elif kind == "blob_outline":
        draw_rect_outline(g, rr, rc, fh, fw, color)
        for dr, dc in ((-1, fw // 2), (fh, fw // 2)):
            r = rr + dr; c = rc + dc
            if 0 <= r < len(g) and 0 <= c < len(g[0]):
                g[r][c] = color
    elif kind == "nested_rects":
        draw_rect_outline(g, rr, rc, fh, fw, color)
        if fh > 4 and fw > 4:
            draw_rect_outline(g, rr + 2, rc + 2, fh - 4, fw - 4, color)
    elif kind == "U_shape":
        draw_rect_outline(g, rr, rc, fh, fw, color)
    elif kind == "irregular_polygon":
        draw_rect_outline(g, rr, rc, fh, fw, color)
        for dc in range(0, fw, 2):
            r = rr - 1
            if 0 <= r < len(g) and 0 <= rc + dc < len(g[0]):
                g[r][rc + dc] = color
    else:
        draw_rect_outline(g, rr, rc, fh, fw, color)


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the fill-then-erase signature collapses.

    open_frame         — outline touches grid border so interior reaches
                          edge; nothing gets filled with green; only the
                          red outline gets erased.
    no_outline         — random non-bg, non-red cells; no fill, no erase.
    full_grid_outline  — outline touches all four edges → no enclosed bg
                          → no green; just an erase of the outline.
    """
    g = full_grid(h, w, 0)
    if name == "open_frame":
        rh, rw = max(4, h // 3), max(4, w // 3)
        rr = h - rh
        rc = rng.randint(1, w - rw - 1)
        for c in range(rc, rc + rw):
            g[rr][c] = 2
        for r in range(rr, rr + rh):
            g[r][rc] = 2
            g[r][rc + rw - 1] = 2
        return g
    if name == "no_outline":
        for _ in range(rng.randint(3, 8)):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            g[r][c] = rng.choice([1, 4, 5, 6, 7, 8, 9])
        return g
    if name == "full_grid_outline":
        for c in range(w):
            g[0][c] = 2
            g[h - 1][c] = 2
        for r in range(h):
            g[r][0] = 2
            g[r][w - 1] = 2
        return g
    return g
