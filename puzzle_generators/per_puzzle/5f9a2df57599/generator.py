"""Generator for puzzle e73095fd.

Rule: for each 0-region, check if its 4 bbox-edge sides are all 5.
If yes, paint it 4.

Combinatorial axes (8): grid_h/w, n_rooms, room_h_min, room_h_max,
room_w_min, room_w_max, n_lines, position_bias.
Degenerates: no_rooms, all_rooms, no_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5f9a2df57599"
VERSION = "1.1.0"
TASK_ID = "5f9a2df57599"
SUMMARY = "Enclosed 5-rooms + decoy 5-lines; rule fills enclosed with 4."

INVARIANTS = [
    "background is 0",
    ">=1 rectangular 5-frame whose interior is enclosed",
    "scattered partial 5-walls don't form extra enclosures",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "diagonal")
DEGENERATE_TEXTURES = ("no_rooms", "all_rooms", "no_lines")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "10..24"},
    "n_rooms":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "room_h_min":     {"type": "int", "default": "4", "valid": "3..6"},
    "room_h_max":     {"type": "int", "default": "rng 5..6", "valid": "4..8"},
    "room_w_min":     {"type": "int", "default": "4", "valid": "3..6"},
    "room_w_max":     {"type": "int", "default": "rng 5..6", "valid": "4..8"},
    "n_lines":        {"type": "int", "default": "rng 2..4", "valid": "0..6"},
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
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rooms = int(overrides.get("n_rooms",
                                ctx.draw_int("n_rooms", 1, 3)))
    n_rooms = max(1, min(4, n_rooms))
    rh_min = int(overrides.get("room_h_min", 4))
    rh_max = int(overrides.get("room_h_max",
                               ctx.draw_int("room_h_max", 5, 6)))
    rw_min = int(overrides.get("room_w_min", 4))
    rw_max = int(overrides.get("room_w_max",
                               ctx.draw_int("room_w_max", 5, 6)))
    n_lines = int(overrides.get("n_lines",
                                ctx.draw_int("n_lines", 2, 4)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    placed_boxes = []
    for idx in range(n_rooms):
        for _ in range(40):
            rh = rng.randint(rh_min, rh_max)
            rw = rng.randint(rw_min, rw_max)
            rr, rc = _pick_room_position(bias, h, w, rh, rw, idx, rng)
            if rr is None:
                continue
            ok = True
            for prev in placed_boxes:
                if not (rr + rh + 1 <= prev[0] or
                        prev[0] + prev[2] + 1 <= rr or
                        rc + rw + 1 <= prev[1] or
                        prev[1] + prev[3] + 1 <= rc):
                    ok = False; break
            if not ok:
                continue
            draw_frame(g, rr, rc, rr + rh - 1, rc + rw - 1, 5)
            placed_boxes.append((rr, rc, rh, rw))
            break
    for _ in range(n_lines):
        is_h = rng.choice([True, False])
        for _ in range(20):
            if is_h:
                r = rng.randint(0, h - 1)
                c1 = rng.randint(0, w - 5)
                c2 = c1 + rng.randint(2, 4)
                if any(g[r][c] != 0 for c in range(c1, c2 + 1)):
                    continue
                for c in range(c1, c2 + 1):
                    g[r][c] = 5
                break
            else:
                c = rng.randint(0, w - 1)
                r1 = rng.randint(0, h - 5)
                r2 = r1 + rng.randint(2, 4)
                if any(g[r][c] != 0 for r in range(r1, r2 + 1)):
                    continue
                for r in range(r1, r2 + 1):
                    g[r][c] = 5
                break
    return g


def _pick_room_position(bias, h, w, rh, rw, idx, rng):
    if h - rh - 2 < 1 or w - rw - 2 < 1:
        return None, None
    if bias == "stacked":
        rr = 1 + idx * (rh + 2)
        if rr + rh > h - 2:
            rr = rng.randint(1, h - rh - 2)
        return rr, rng.randint(1, w - rw - 2)
    if bias == "row_aligned":
        rr = max(1, (h - rh) // 2)
        rc = 1 + idx * (rw + 2)
        if rc + rw > w - 2:
            rc = rng.randint(1, w - rw - 2)
        return rr, rc
    if bias == "diagonal":
        rr = 1 + idx * 4
        rc = 1 + idx * 4
        if rr + rh > h - 2 or rc + rw > w - 2:
            return rng.randint(1, h - rh - 2), rng.randint(1, w - rw - 2)
        return rr, rc
    return rng.randint(1, h - rh - 2), rng.randint(1, w - rw - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_rooms":
        for c in range(2, w - 2, 2):
            g[2][c] = 5
        return g
    if name == "all_rooms":
        # Many adjacent rooms
        for rr in range(1, h - 5, 6):
            for rc in range(1, w - 5, 6):
                draw_frame(g, rr, rc, rr + 4, rc + 4, 5)
        return g
    if name == "no_lines":
        draw_frame(g, 2, 2, 6, 6, 5)
        return g
    return g
