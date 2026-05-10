"""Generator for fe45cba4.

Rule: for each non-bg color split into multiple components, keep the
larger one (lower/right) and fill one column left of its bbox.

Combinatorial axes (8): grid_h/w, color, big_h, big_w, position_bias,
palette_kind, palette_size, anchor_corner.
Degenerates: same_size, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "ad5a6c1521b3"
VERSION = "1.1.0"
TASK_ID = "ad5a6c1521b3"
SUMMARY = "A color split into 2 components; rule keeps larger + fills one col left."

INVARIANTS = [
    "bg is the most common color",
    ">=1 non-bg color forms 2 separate components of different sizes",
    "the larger component has bg cells to its left",
]

POSITION_BIASES = ("right_heavy", "spread", "stacked", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_size", "single_component", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "color":          {"type": "color", "default": "rng 1..9", "valid": "1..9"},
    "big_h":          {"type": "int", "default": "3", "valid": "3..5"},
    "big_w":          {"type": "int", "default": "3", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
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
        h_lo, h_hi, w_lo, w_hi = 10, 12, 12, 14
        bh, bw = 3, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 16, 20, 18, 22
        bh, bw = 4, 5
    else:
        h_lo, h_hi, w_lo, w_hi = 12, 16, 14, 18
        bh, bw = 3, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", rng.choice(pal)))
    bh = int(overrides.get("big_h", bh))
    bw = int(overrides.get("big_w", bw))
    g = full_grid(h, w, 0)
    small_cells = normalize(rect_cells(2, 2))
    place_no_overlap(rng, g, small_cells, color, bg=0, margin=1, max_tries=20)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed_big = False
    for _try in range(30):
        if bias == "right_heavy":
            rr = rng.randint(2, h - bh - 1)
            rc = rng.randint(w - bw - 3, w - bw - 1)
        elif bias == "stacked":
            rr = rng.randint(h - bh - 3, h - bh - 1)
            rc = rng.randint(w // 2 + 2, w - bw - 1)
        elif bias == "spread":
            rr = rng.randint(2, h - bh - 1)
            rc = rng.randint(w // 2 + 2, w - bw - 1)
        else:
            rr = rng.randint(2, h - bh - 1)
            rc = rng.randint(w // 2 + 2, w - bw - 1)
        ok = all(g[rr + dr][rc + dc] == 0
                 for dr in range(bh) for dc in range(bw))
        if ok:
            for dr in range(bh):
                for dc in range(bw):
                    g[rr + dr][rc + dc] = color
            placed_big = True
            break
    if not placed_big:
        return _draw_from_degenerate("single_component", rng)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "same_size":
        for dr in range(2):
            for dc in range(2):
                g[2 + dr][2 + dc] = 3
                g[8 + dr][10 + dc] = 3
        return g
    if name == "single_component":
        for dr in range(3):
            for dc in range(3):
                g[5 + dr][7 + dc] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
