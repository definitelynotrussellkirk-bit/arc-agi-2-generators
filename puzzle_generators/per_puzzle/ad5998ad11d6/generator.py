"""Generator for puzzle 00d62c1b — `(rule! (fill-all-enclosed g 4))`.
Fill every bg(0) region not reachable from the border with yellow(4).

Combinatorial axes:
  * grid_h / grid_w           — outer canvas size
  * n_frames                  — how many enclosing shapes to plant (1..3)
  * frame_kind                — shape: rect_outline / blob_outline /
                                irregular / U_shape / nested
  * frame_color               — color of the enclosing wall (≠ 0, ≠ 4)
  * size_distribution         — frame size mix: small/medium/large/mixed
  * decor_density             — extra non-bg, non-4 cells outside frames
  * caller-opt-in degenerates: open_frame (touches border, no enclosure),
                               solid_frame (no interior), tiny_frame (3×3)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "ad5998ad11d6"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "ad5998ad11d6"
SUMMARY = "Closed shapes on a 0 background; rule fills enclosed bg cells with 4."

INVARIANTS = [
    "background is 0",
    "≥1 closed outline of non-bg, non-yellow color",
    "outline encloses ≥1 bg cell (so the rule has effect)",
    "outline does not touch any grid edge",
]

HELPFUL_FRAME_KINDS = (
    "rect_outline", "blob_outline", "irregular_polygon",
    "U_shape", "nested_rects",
)
SIZE_DISTRIBUTIONS = ("small", "medium", "large", "mixed")
DEGENERATE_TEXTURES = ("open_frame", "solid_frame", "tiny_frame")

AXES = {
    "grid_h":            {"type": "int",   "default": "rng 12..20", "valid": "10..28"},
    "grid_w":            {"type": "int",   "default": "rng 12..20", "valid": "10..28"},
    "n_frames":          {"type": "int",   "default": "rng 1..3",   "valid": "1..5"},
    "frame_kind":        {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(HELPFUL_FRAME_KINDS)},
    "frame_color":       {"type": "color", "default": "rng",        "valid": "1..9 (≠4)"},
    "size_distribution": {"type": "str",   "default": "rng small|medium|large|mixed",
                          "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "decor_density":     {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "texture":           {"type": "str",   "default": "alias for frame_kind",
                          "valid": "|".join(HELPFUL_FRAME_KINDS + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 12, 14, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 18, 20, 2, 3
    else:
        h_lo, h_hi, n_lo, n_hi = 12, 20, 1, 3

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", n_lo, n_hi)))
    frame_kind = (overrides.get("texture")
                  or overrides.get("frame_kind")
                  or ctx.draw_choice("frame_kind", list(HELPFUL_FRAME_KINDS)))
    frame_color = int(overrides.get("frame_color",
                                    ctx.draw_color("frame_color", exclude={0, 4})))
    size_dist = overrides.get(
        "size_distribution",
        ctx.draw_choice("size_distribution", list(SIZE_DISTRIBUTIONS)))

    g = full_grid(h, w, 0)
    placed_boxes: list[tuple[int, int, int, int]] = []

    for _ in range(n_frames):
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
            _draw_frame_kind(g, frame_kind, rr, rc, fh, fw, frame_color, rng)
            placed_boxes.append((rr, rc, rr + fh - 1, rc + fw - 1))
            break

    if not placed_boxes:
        # Fallback: tiny rect to keep invariant.
        draw_rect_outline(g, 2, 2, 4, 4, frame_color)

    decor = float(overrides.get(
        "decor_density",
        ctx.draw_rng("decor_density").uniform(0.0, 0.05)))
    if decor > 0.0:
        decor_palette = [c for c in range(10) if c not in {0, 4, frame_color}]
        for _ in range(max(1, int(h * w * decor))):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] == 0 and not _is_inside_any(r, c, placed_boxes):
                g[r][c] = rng.choice(decor_palette) if decor_palette else 0
    return g


def _is_inside_any(r, c, boxes):
    """True if (r, c) lies strictly inside one of the placed bbox interiors,
    so we don't sprinkle decor inside frames (which would break the rule's
    fill semantics)."""
    for (r1, c1, r2, c2) in boxes:
        if r1 <= r <= r2 and c1 <= c <= c2:
            return True
    return False


def _frame_dims(size_dist, h, w, rng):
    """Pick (frame_h, frame_w) for the requested size distribution."""
    if size_dist == "small":
        return rng.randint(3, 5), rng.randint(3, 5)
    if size_dist == "medium":
        return rng.randint(5, max(5, h // 3)), rng.randint(5, max(5, w // 3))
    if size_dist == "large":
        return (rng.randint(max(5, h // 3), max(5, h // 2)),
                rng.randint(max(5, w // 3), max(5, w // 2)))
    # mixed
    return rng.randint(3, max(3, h // 3)), rng.randint(3, max(3, w // 3))


def _draw_frame_kind(g, kind, rr, rc, fh, fw, color, rng):
    """Paint an enclosing shape into g[rr:rr+fh][rc:rc+fw]."""
    if kind == "rect_outline":
        draw_rect_outline(g, rr, rc, fh, fw, color)
    elif kind == "blob_outline":
        # Rect outline plus a few "bumps" outside the corners.
        draw_rect_outline(g, rr, rc, fh, fw, color)
        for dr, dc in ((-1, fw // 2), (fh, fw // 2)):
            r = rr + dr; c = rc + dc
            if 0 <= r < len(g) and 0 <= c < len(g[0]):
                g[r][c] = color
    elif kind == "irregular_polygon":
        # Rect outline plus irregular zigzag at one edge.
        draw_rect_outline(g, rr, rc, fh, fw, color)
        for dc in range(1, fw - 1, 2):
            r = rr - 1
            if 0 <= r < len(g) and 0 <= rc + dc < len(g[0]):
                g[r][rc + dc] = color
        # close the bumps so they still enclose
        for dc in range(0, fw, 2):
            if 0 <= rr - 1 < len(g):
                g[rr - 1][rc + dc] = color
    elif kind == "U_shape":
        # Closed rect (still encloses) — labelled "U" but actually closed.
        draw_rect_outline(g, rr, rc, fh, fw, color)
    elif kind == "nested_rects":
        # Outer + smaller inner outline; only the inner cells are enclosed.
        draw_rect_outline(g, rr, rc, fh, fw, color)
        if fh > 4 and fw > 4:
            draw_rect_outline(g, rr + 2, rc + 2, fh - 4, fw - 4, color)
    else:
        draw_rect_outline(g, rr, rc, fh, fw, color)


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the fill-all-enclosed signal collapses.

    open_frame  — frame touches grid border, so the "interior" is
                  border-reachable; the rule fills nothing.
    solid_frame — fully-painted rectangle with no interior; rule has
                  no work.
    tiny_frame  — 3×3 outline encloses just one cell; the fill is
                  technically correct but visually subtle.
    """
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    if name == "open_frame":
        # Outline that touches the bottom border (no enclosure).
        rh, rw = max(4, h // 3), max(4, w // 3)
        rr = h - rh
        rc = rng.randint(1, w - rw - 1)
        for c in range(rc, rc + rw):
            g[rr][c] = color
        for r in range(rr, rr + rh):
            g[r][rc] = color
            g[r][rc + rw - 1] = color
        return g
    if name == "solid_frame":
        rh, rw = max(3, h // 4), max(3, w // 4)
        rr = rng.randint(2, h - rh - 2)
        rc = rng.randint(2, w - rw - 2)
        for r in range(rr, rr + rh):
            for c in range(rc, rc + rw):
                g[r][c] = color
        return g
    if name == "tiny_frame":
        rr = rng.randint(2, h - 4)
        rc = rng.randint(2, w - 4)
        draw_rect_outline(g, rr, rc, 3, 3, color)
        return g
    return g
