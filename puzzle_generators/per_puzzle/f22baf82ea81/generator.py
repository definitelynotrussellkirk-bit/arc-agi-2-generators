"""Generator for puzzle b94a9452.

Rule: 2-color region on bg=0. Output crops to bbox and swaps the two
colors (outer = top-left of bbox, inner = first non-outer).

Combinatorial axes (8): grid_h/w, region_h, region_w, palette_kind,
inner_density, position_bias, anchor_corner, asymmetry_force.
Degenerates: single_color, no_region, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f22baf82ea81"
VERSION = "1.1.0"
TASK_ID = "f22baf82ea81"
SUMMARY = "2-color region; rule crops to bbox and swaps colors."

INVARIANTS = [
    "background is 0",
    "single 2-color region (outer + inner)",
    "bbox top-left cell is the outer color",
    ">=1 inner-color cell inside",
]

POSITION_BIASES = ("scattered", "centered", "corners", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_color", "no_region", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "region_h":       {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "region_w":       {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "inner_density":  {"type": "float", "default": "rng 0.4..0.7",
                       "valid": "0.2..1"},
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
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    rh = int(overrides.get("region_h",
                           ctx.draw_int("region_h", 4, 7)))
    rw = int(overrides.get("region_w",
                           ctx.draw_int("region_w", 4, 7)))
    rh = max(3, min(h - 2, rh))
    rw = max(3, min(w - 2, rw))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 2, rng)
    outer, inner = palette[0], palette[1]
    inner_d = float(overrides.get("inner_density",
                                  ctx.draw_rng("inner_density")
                                  .uniform(0.4, 0.7)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    rr, rc = _pick_position(bias, h, w, rh, rw, rng)
    g = full_grid(h, w, 0)
    for r in range(rr, rr + rh):
        for c in range(rc, rc + rw):
            on_edge = (r == rr or r == rr + rh - 1
                       or c == rc or c == rc + rw - 1)
            if on_edge:
                g[r][c] = outer
            else:
                g[r][c] = inner if rng.random() < inner_d else outer
    g[rr + 1][rc + 1] = inner
    g[rr][rc] = outer
    return g


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
    return pool[:n]


def _pick_position(bias, h, w, rh, rw, rng):
    if bias == "centered":
        return max(1, (h - rh) // 2), max(1, (w - rw) // 2)
    if bias == "corners":
        return rng.choice([(1, 1), (1, w - rw - 1),
                            (h - rh - 1, 1),
                            (h - rh - 1, w - rw - 1)])
    if bias == "spread":
        return rng.randint(1, h - rh - 1), rng.randint(1, w - rw - 1)
    return rng.randint(1, h - rh - 1), rng.randint(1, w - rw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_color":
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 3
        return g
    if name == "no_region":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
