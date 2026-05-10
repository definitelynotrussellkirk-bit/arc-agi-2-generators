"""Generator for puzzle 41e4d17e.

Rule: bg=cyan(8). For each rectangular outline drawn in 1, emit
crosshair rays of 6 from the frame's center — full-grid horizontal +
vertical lines, replacing only bg(=8) cells.

Combinatorial axes (8): grid_h/w, n_frames, frame_h_min, frame_h_max,
frame_w_min, frame_w_max, position_bias, anchor_corner.
Degenerates: tiny_frame, single_frame, full_grid_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "2acfd448f58b"
VERSION = "1.1.0"
TASK_ID = "2acfd448f58b"
SUMMARY = "Cyan(8) bg + 1-frames; rule emits crosshair 6-rays from each frame's center."

INVARIANTS = [
    "background is 8 (cyan)",
    ">=1 rectangular outline frame drawn in 1",
    "frames are non-overlapping with margin >= 1",
    "frame dim >= 3x3 (centers well-defined)",
]

POSITION_BIASES = ("spread", "corners", "diagonal", "row_aligned",
                   "col_aligned")
DEGENERATE_TEXTURES = ("tiny_frame", "single_frame", "full_grid_frame")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "9..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "9..22"},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "frame_h_min":    {"type": "int", "default": "3", "valid": "3..6"},
    "frame_h_max":    {"type": "int", "default": "rng 5..7", "valid": "3..10"},
    "frame_w_min":    {"type": "int", "default": "3", "valid": "3..6"},
    "frame_w_max":    {"type": "int", "default": "rng 5..7", "valid": "3..10"},
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
        h_lo, h_hi = 9, 12
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", 2, 3)))
    n_frames = max(1, min(4, n_frames))
    fh_min = int(overrides.get("frame_h_min", 3))
    fh_max = int(overrides.get("frame_h_max",
                               ctx.draw_int("frame_h_max", 5, 7)))
    fw_min = int(overrides.get("frame_w_min", 3))
    fw_max = int(overrides.get("frame_w_max",
                               ctx.draw_int("frame_w_max", 5, 7)))
    fh_min = max(3, min(fh_min, h - 2))
    fh_max = max(fh_min, min(fh_max, h - 2))
    fw_min = max(3, min(fw_min, w - 2))
    fw_max = max(fw_min, min(fw_max, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 8)
    placed = 0
    placed_boxes = []
    for attempt in range(n_frames * 8):
        if placed >= n_frames:
            break
        fh = rng.randint(fh_min, fh_max)
        fw = rng.randint(fw_min, fw_max)
        if fh > h - 2 or fw > w - 2:
            continue
        rr, rc = _pick_position(bias, h, w, fh, fw, placed, rng)
        if rr is None:
            continue
        ok = all(not (rr - 1 <= or2 and rr + fh >= or1
                       and rc - 1 <= oc2 and rc + fw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok:
            continue
        draw_rect_outline(g, rr, rc, fh, fw, 1)
        placed_boxes.append((rr, rc, rr + fh - 1, rc + fw - 1))
        placed += 1
    if placed == 0:
        rr = max(1, (h - 5) // 2)
        rc = max(1, (w - 5) // 2)
        draw_rect_outline(g, rr, rc, 5, 5, 1)
    return g


def _pick_position(bias, h, w, fh, fw, idx, rng):
    if h - fh - 1 < 1 or w - fw - 1 < 1:
        return None, None
    if bias == "corners":
        corners = [(1, 1), (1, w - fw - 1), (h - fh - 1, 1),
                   (h - fh - 1, w - fw - 1)]
        return corners[idx % 4]
    if bias == "diagonal":
        rr = 1 + idx * (fh + 2)
        rc = 1 + idx * (fw + 2)
        if rr + fh > h - 1 or rc + fw > w - 1:
            return (rng.randint(1, h - fh - 1),
                    rng.randint(1, w - fw - 1))
        return rr, rc
    if bias == "row_aligned":
        rr = max(1, (h - fh) // 2)
        rc = 1 + idx * (fw + 2)
        if rc + fw > w - 1:
            rc = rng.randint(1, w - fw - 1)
        return rr, rc
    if bias == "col_aligned":
        rr = 1 + idx * (fh + 2)
        if rr + fh > h - 1:
            rr = rng.randint(1, h - fh - 1)
        rc = max(1, (w - fw) // 2)
        return rr, rc
    return rng.randint(1, h - fh - 1), rng.randint(1, w - fw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 8)
    if name == "tiny_frame":
        rr = max(1, (h - 3) // 2)
        rc = max(1, (w - 3) // 2)
        draw_rect_outline(g, rr, rc, 3, 3, 1)
        return g
    if name == "single_frame":
        rr = max(1, (h - 5) // 2)
        rc = max(1, (w - 5) // 2)
        draw_rect_outline(g, rr, rc, 5, 5, 1)
        return g
    if name == "full_grid_frame":
        draw_rect_outline(g, 0, 0, h, w, 1)
        return g
    return g
