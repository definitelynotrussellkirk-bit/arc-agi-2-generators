"""Generator for d282b262.

Rule: multicolor 8-connected objects on bg=0; rule slides each rightward
(rightmost first), each as far as possible until blocked.

Combinatorial axes (8): grid_h/w, n_objs, obj_h_max, obj_w_max,
palette_kind, position_bias, anchor_corner, asymmetry_force.
Degenerates: single_object, no_room, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "08df98d7e8fa"
VERSION = "1.1.0"
TASK_ID = "08df98d7e8fa"
SUMMARY = "Multicolor objects scattered; rule slides each rightward."

INVARIANTS = [
    "background is 0",
    ">=2 multicolor 8-connected objects",
    "each object has bg cells to its right",
    "objects don't span the full width of the grid",
]

POSITION_BIASES = ("scattered", "stacked", "row_aligned", "left_lean")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_object", "no_room", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "n_objs":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "obj_h_max":      {"type": "int", "default": "3", "valid": "2..4"},
    "obj_w_max":      {"type": "int", "default": "3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 12, 14
        no_lo, no_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 14, 18, 18, 22
        no_lo, no_hi = 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 14, 14, 18
        no_lo, no_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    g = full_grid(h, w, 0)
    n_objs = int(overrides.get("n_objs",
                               ctx.draw_int("n_objs", no_lo, no_hi)))
    n_objs = max(2, min(4, n_objs))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    obj_h_max = int(overrides.get("obj_h_max", 3))
    obj_w_max = int(overrides.get("obj_w_max", 3))
    placed_boxes = []
    placed = 0
    for _try in range(40):
        if placed >= n_objs:
            break
        rh = rng.randint(2, obj_h_max)
        rw = rng.randint(2, obj_w_max)
        rr, rc = _pick_pos(bias, h, w, rh, rw, placed, rng)
        ok = all(not (rr - 1 <= or2 and rr + rh >= or1
                       and rc - 1 <= oc2 and rc + rw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok:
            continue
        for dr in range(rh):
            for dc in range(rw):
                g[rr + dr][rc + dc] = rng.choice(palette)
        placed_boxes.append((rr, rc, rr + rh - 1, rc + rw - 1))
        placed += 1
    if placed < 2:
        return _draw_from_degenerate("single_object", rng)
    return g


def _pick_pos(bias, h, w, rh, rw, idx, rng):
    if bias == "stacked":
        rr = idx * 4
        rc = rng.randint(0, max(0, w // 2 - rw))
    elif bias == "row_aligned":
        rr = max(2, h // 3)
        rc = idx * 4
    elif bias == "left_lean":
        rr = rng.randint(0, h - rh)
        rc = rng.randint(0, max(0, w // 3 - rw))
    else:
        rr = rng.randint(0, h - rh)
        rc = rng.randint(0, max(0, w // 2 - rw))
    rr = max(0, min(rr, h - rh))
    rc = max(0, min(rc, w - rw))
    return rr, rc


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "single_object":
        for dr in range(2):
            for dc in range(2):
                g[3 + dr][3 + dc] = 2
        return g
    if name == "no_room":
        for dr in range(2):
            for dc in range(2):
                g[3 + dr][w - 2 + dc - 1] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 4 + 1
        return g
    return g
