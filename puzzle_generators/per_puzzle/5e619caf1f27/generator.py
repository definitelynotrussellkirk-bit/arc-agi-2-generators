"""Generator for 3a301edc.

Rule: outer rectangle of one color + inner rectangle of another;
output adds a frame of inner_color around outer.

Combinatorial axes (8): grid_h/w, outer_h, outer_w, inner_h, inner_w,
position_bias, palette_kind, anchor_corner.
Degenerates: no_inner, no_margin, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "5e619caf1f27"
VERSION = "1.1.0"
TASK_ID = "5e619caf1f27"
SUMMARY = "Outer rectangle + inner rectangle of distinct colors, centered."

INVARIANTS = [
    "exactly 2 non-zero colors",
    "outer rect entirely fills its bbox",
    "inner rect strictly inside outer rect",
    "outer rect has >=inner_dim margin from all grid edges",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_inner", "no_margin", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "outer_h":        {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "outer_w":        {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "inner_h":        {"type": "int", "default": "rng 2..oh-2", "valid": "2..6"},
    "inner_w":        {"type": "int", "default": "rng 2..ow-2", "valid": "2..6"},
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
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 14
        oh_lo, oh_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
        oh_lo, oh_hi = 6, 10
    else:
        h_lo, h_hi = 14, 18
        oh_lo, oh_hi = 5, 8
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    outer_color, inner_color = random_palette(rng, 2)
    oh = int(overrides.get("outer_h",
                           rng.randint(oh_lo, oh_hi)))
    ow = int(overrides.get("outer_w",
                           rng.randint(oh_lo, oh_hi)))
    oh = max(4, min(oh, h - 4))
    ow = max(4, min(ow, w - 4))
    ih = int(overrides.get("inner_h",
                           rng.randint(2, max(2, oh - 2))))
    iw = int(overrides.get("inner_w",
                           rng.randint(2, max(2, ow - 2))))
    ih = max(2, min(ih, oh - 2))
    iw = max(2, min(iw, ow - 2))
    margin = max(ih, iw)
    if h - oh - margin < margin or w - ow - margin < margin:
        margin = max(1, min(h - oh - 1, w - ow - 1) // 2)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        or0 = max(margin, (h - oh) // 2)
        oc0 = max(margin, (w - ow) // 2)
    elif bias == "corner":
        or0 = rng.choice([margin, max(margin, h - oh - margin)])
        oc0 = rng.choice([margin, max(margin, w - ow - margin)])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            or0 = rng.choice([margin, max(margin, h - oh - margin)])
            oc0 = rng.randint(margin, max(margin, w - ow - margin))
        else:
            or0 = rng.randint(margin, max(margin, h - oh - margin))
            oc0 = rng.choice([margin, max(margin, w - ow - margin)])
    else:
        or0 = rng.randint(margin, max(margin, h - oh - margin))
        oc0 = rng.randint(margin, max(margin, w - ow - margin))
    or0 = max(margin, min(or0, h - oh - margin))
    oc0 = max(margin, min(oc0, w - ow - margin))
    fill_box(g, or0, oc0, or0 + oh - 1, oc0 + ow - 1, outer_color)
    ir0 = or0 + (oh - ih) // 2
    ic0 = oc0 + (ow - iw) // 2
    fill_box(g, ir0, ic0, ir0 + ih - 1, ic0 + iw - 1, inner_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_inner":
        fill_box(g, 5, 5, 10, 10, 2)
        return g
    if name == "no_margin":
        fill_box(g, 0, 0, 7, 7, 2)
        fill_box(g, 2, 2, 5, 5, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
