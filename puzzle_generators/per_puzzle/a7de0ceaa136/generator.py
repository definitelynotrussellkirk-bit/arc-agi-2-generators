"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:hard_141_decode_dual_code_library_and_center_stamp.

Rule: row 0 holds three control codes (prototype color, transform,
output color); the largest prototype-colored component is transformed
and centered inside an 8-frame, recolored to the output color.

Combinatorial axes (8): shape, transform, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes, no_frame, no_prototype.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a7de0ceaa136"
VERSION = "1.1.0"
TASK_ID = "a7de0ceaa136"
SUMMARY = "Decode prototype color, transform code, and output color, then center the transformed prototype in a frame."

INVARIANTS = [
    "row 0 columns 0..2 hold prototype color, transform code, and output color",
    "one color-8 rectangular frame is the destination canvas",
    "the largest component of the prototype color outside controls is the source shape",
    "the transformed source is recolored and centered inside the cropped frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_frame", "no_prototype")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape":          {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "transform":      {"type": "int", "default": "rng 1..6", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "codes_top_frame_bottom",
                       "valid": "codes_top_frame_bottom"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = ctx.draw_int("shape", 0, 1)
        transform = ctx.draw_int("transform", 1, 3)
    elif difficulty == "hard":
        shape = ctx.draw_int("shape", 2, 4)
        transform = ctx.draw_int("transform", 4, 6)
    else:
        shape = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
        transform = ctx.draw_int("transform", 1, 6)
    proto_color, out_color, distractor = rng.sample([2, 3, 4, 5, 6, 7, 9], 3)

    g = full_grid(12, 16, 0)
    g[0][0] = proto_color
    g[0][1] = transform
    g[0][2] = out_color
    draw_frame(g, 7, 9, 11, 15, 8)
    _paint(g, 2, 1, _SHAPES[shape], proto_color)
    _paint(g, 4, 6, [(0, 0), (1, 0), (1, 1)], distractor)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "no_codes":
        # Prototype + frame present but row 0 codes are empty — rule has
        # no transform code or output color spec to apply.
        draw_frame(g, 7, 9, 11, 15, 8)
        _paint(g, 2, 1, _SHAPES[0], 4)
        return g
    if name == "no_frame":
        # Codes + prototype present but no 8-frame — rule has no
        # destination canvas to center the stamp into.
        g[0][0] = 4; g[0][1] = 2; g[0][2] = 6
        _paint(g, 2, 1, _SHAPES[0], 4)
        return g
    if name == "no_prototype":
        # Codes + frame present but no prototype-color component — rule
        # has nothing to transform.
        g[0][0] = 4; g[0][1] = 2; g[0][2] = 6
        draw_frame(g, 7, 9, 11, 15, 8)
        _paint(g, 4, 6, [(0, 0), (1, 0), (1, 1)], 7)
        return g
    return g
