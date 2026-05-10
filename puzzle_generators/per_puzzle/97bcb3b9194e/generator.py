"""Generator for puzzle 7bb29440.

Rule: 1-bordered rectangular boxes with marks. Output is the box with
the FEWEST non-1 marks inside.

Combinatorial axes (8): grid_h/w, n_boxes, box_h_min, box_h_max,
box_w_min, box_w_max, mark_palette, position_bias.
Degenerates: tied_marks, single_box, no_marks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "97bcb3b9194e"
VERSION = "1.1.0"
TASK_ID = "97bcb3b9194e"
SUMMARY = "1-outlined boxes w/ marks; rule outputs box with fewest marks."

INVARIANTS = [
    "background is 0",
    ">=2 1-outlined rectangular boxes",
    "boxes >=4x4 (with >=2x2 interior)",
    "boxes have distinct mark counts",
    "boxes don't overlap (>=1 cell apart)",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal",
                   "corners")
DEGENERATE_TEXTURES = ("tied_marks", "single_box", "no_marks")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..22", "valid": "12..28"},
    "grid_w":         {"type": "int", "default": "rng 14..22", "valid": "12..28"},
    "n_boxes":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "box_h_min":      {"type": "int", "default": "4", "valid": "4..8"},
    "box_h_max":      {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "box_w_min":      {"type": "int", "default": "4", "valid": "4..8"},
    "box_w_max":      {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "mark_palette":   {"type": "str", "default": "rng",
                       "valid": "warm|cool|broad"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 22, 28
    else:
        h_lo, h_hi = 14, 22
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_boxes = int(overrides.get("n_boxes",
                                ctx.draw_int("n_boxes", 2, 3)))
    n_boxes = max(2, min(4, n_boxes))
    bh_min = int(overrides.get("box_h_min", 4))
    bh_max = int(overrides.get("box_h_max",
                               ctx.draw_int("box_h_max", 5, 7)))
    bw_min = int(overrides.get("box_w_min", 4))
    bw_max = int(overrides.get("box_w_max",
                               ctx.draw_int("box_w_max", 5, 7)))
    bh_min = max(4, min(bh_min, h - 2))
    bh_max = max(bh_min, min(bh_max, h - 2))
    bw_min = max(4, min(bw_min, w - 2))
    bw_max = max(bw_min, min(bw_max, w - 2))
    mark_palette_kind = overrides.get("mark_palette", "broad")
    mark_palette = _build_mark_palette(mark_palette_kind, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    boxes_placed = []
    target_n_marks = list(range(n_boxes))
    rng.shuffle(target_n_marks)
    for idx, n_marks in enumerate(target_n_marks):
        for _ in range(40):
            bh = rng.randint(bh_min, bh_max)
            bw = rng.randint(bw_min, bw_max)
            rr, rc = _pick_position(bias, h, w, bh, bw, idx, rng)
            if rr is None:
                continue
            ok = all(not (rr - 1 <= or2 and rr + bh >= or1
                          and rc - 1 <= oc2 and rc + bw >= oc1)
                     for (or1, oc1, or2, oc2) in boxes_placed)
            if not ok:
                continue
            draw_rect_outline(g, rr, rc, bh, bw, 1)
            interior_cells = [(r, c) for r in range(rr + 1, rr + bh - 1)
                              for c in range(rc + 1, rc + bw - 1)]
            rng.shuffle(interior_cells)
            for k in range(min(n_marks, len(interior_cells))):
                r, c = interior_cells[k]
                g[r][c] = rng.choice(mark_palette)
            boxes_placed.append((rr, rc, rr + bh - 1, rc + bw - 1))
            break
    if len(boxes_placed) < 2:
        return _draw_from_degenerate("single_box", h, w, rng)
    return g


def _build_mark_palette(kind, rng):
    if kind == "warm":
        return [3, 4, 6, 9]
    if kind == "cool":
        return [5, 7, 8]
    return [4, 6]


def _pick_position(bias, h, w, bh, bw, idx, rng):
    if h - bh - 1 < 1 or w - bw - 1 < 1:
        return None, None
    if bias == "stacked":
        rr = 1 + idx * (bh + 2)
        if rr + bh > h - 1:
            rr = rng.randint(1, h - bh - 1)
        return rr, max(1, (w - bw) // 2)
    if bias == "row_aligned":
        rr = max(1, (h - bh) // 2)
        rc = 1 + idx * (bw + 2)
        if rc + bw > w - 1:
            rc = rng.randint(1, w - bw - 1)
        return rr, rc
    if bias == "diagonal":
        rr = 1 + idx * 4
        rc = 1 + idx * 4
        if rr + bh > h - 1 or rc + bw > w - 1:
            return rng.randint(1, h - bh - 1), rng.randint(1, w - bw - 1)
        return rr, rc
    if bias == "corners":
        corners = [(1, 1), (1, w - bw - 1), (h - bh - 1, 1),
                   (h - bh - 1, w - bw - 1)]
        return corners[idx % 4]
    return rng.randint(1, h - bh - 1), rng.randint(1, w - bw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_marks":
        for r0, c0 in [(2, 2), (2, w - 7)]:
            draw_rect_outline(g, r0, c0, 5, 5, 1)
            g[r0 + 1][c0 + 1] = 4
        return g
    if name == "single_box":
        draw_rect_outline(g, 2, 2, 5, 5, 1)
        return g
    if name == "no_marks":
        for r0, c0 in [(2, 2), (2, w - 7)]:
            draw_rect_outline(g, r0, c0, 5, 5, 1)
        return g
    return g
