"""Generator for puzzle 7b6016b9.

Rule: `(rule! (lambda (g) (recolor (fill-all-enclosed g 2) 0 3)))`. First
fill bg cells enclosed by outlines with red(2); then replace remaining
bg with green(3). End result: every original bg becomes either red
(inside an outline) or green (outside).

Combinatorial axes:
  * grid_h / grid_w           — outer canvas size
  * n_outlines                — how many enclosing shapes to plant
  * frame_kind                — rect_outline / blob_outline / nested / U_shape
  * outline_color             — color of the wall (≠ 0, ≠ 2, ≠ 3)
  * size_distribution         — small / medium / large / mixed
  * decor_density             — extra cells outside frames (won't be filled
                                with red, but stay non-bg)
  * caller-opt-in degenerates: open_frame, no_outline, full_grid_outline
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "33275a4aae3e"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "33275a4aae3e"
SUMMARY = "Closed outlines on a 0 background; rule fills enclosed bg with red, rest with green."

INVARIANTS = [
    "background is 0",
    "≥1 closed outline drawn in a single non-bg, non-red(2), non-green(3) color",
    "outline encloses ≥1 bg cell",
    "outline has bg margin from the grid edge",
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
    "outline_color":     {"type": "color", "default": "rng",        "valid": "1..9 (≠0,2,3)"},
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
    outline_color = int(overrides.get(
        "outline_color",
        ctx.draw_color("outline_color", exclude={0, 2, 3})))
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
            _draw_frame_kind(g, frame_kind, rr, rc, fh, fw, outline_color, rng)
            placed_boxes.append((rr, rc, rr + fh - 1, rc + fw - 1))
            break

    if not placed_boxes:
        draw_rect_outline(g, 2, 2, 4, 4, outline_color)

    decor = float(overrides.get(
        "decor_density",
        ctx.draw_rng("decor_density").uniform(0.0, 0.05)))
    if decor > 0.0:
        decor_palette = [c for c in range(10) if c not in {0, 2, 3, outline_color}]
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
    """Edge-case where the fill-then-recolor signature collapses.

    open_frame         — frame touches grid border so interior reaches
                          edge; the rule fills the "open" interior with
                          red anyway under fill-all-enclosed semantics?
                          Actually: not enclosed → no red; output ends up
                          all green except outline.
    no_outline         — random non-bg cells without any closed shape;
                          rule fills no red, just green elsewhere.
    full_grid_outline  — outline touches all four edges → no enclosed
                          bg → no red. Output is the outline + all green.
    """
    g = full_grid(h, w, 0)
    color = rng.choice([1, 4, 5, 6, 7, 8, 9])
    if name == "open_frame":
        rh, rw = max(4, h // 3), max(4, w // 3)
        rr = h - rh
        rc = rng.randint(1, w - rw - 1)
        for c in range(rc, rc + rw):
            g[rr][c] = color
        for r in range(rr, rr + rh):
            g[r][rc] = color
            g[r][rc + rw - 1] = color
        return g
    if name == "no_outline":
        for _ in range(rng.randint(3, 8)):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            g[r][c] = color
        return g
    if name == "full_grid_outline":
        for c in range(w):
            g[0][c] = color
            g[h - 1][c] = color
        for r in range(h):
            g[r][0] = color
            g[r][w - 1] = color
        return g
    return g
