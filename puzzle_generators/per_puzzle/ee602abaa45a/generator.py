"""Generator for arc_puzzle_bank_tenth_21_bundle:hard_70_decode_local_frame_template_codes.

Each high-color frame contains a local selector color and transform code. The
selected interior template is transformed and recolored by the frame color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code_a,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_codes, no_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "ee602abaa45a"
VERSION = "1.1.0"
TASK_ID = "ee602abaa45a"
SUMMARY = "Decode each frame's selector and transform code into a recolored gallery part."

INVARIANTS = [
    "there are two high-color rectangular frames",
    "each frame has selector and transform-code cells on its lower interior row",
    "template cells above that row use the selected color",
    "output parts are sorted by frame position and recolored by frame color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_codes", "no_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code_a":         {"type": "int", "default": "rng choice 3|4|5|6", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_high_color_frames",
                       "valid": "two_high_color_frames"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATTERN = [(0, 0), (1, 0), (1, 1)]


def _draw_coded_frame(g, top, left, frame_color, selector, code):
    draw_frame(g, top, left, top + 5, left + 5, frame_color)
    for dr, dc in _PATTERN:
        g[top + 1 + dr][left + 1 + dc] = selector
    g[top + 4][left + 1] = selector
    g[top + 4][left + 2] = code


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    code_a = ctx.draw_choice("code_a", [3, 4, 5, 6])
    code_b = ctx.draw_choice("code_b", [3, 4, 5, 6])
    g = full_grid(8, 15, 0)
    _draw_coded_frame(g, 1, 1, 7, 2, code_a)
    _draw_coded_frame(g, 1, 8, 8, 3, code_b)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 15, 0)
    if name == "no_frames":
        # selectors + codes without frames → no container to scope decode
        for dr, dc in _PATTERN:
            g[1 + 1 + dr][1 + 1 + dc] = 2
        g[1 + 4][1 + 1] = 2; g[1 + 4][1 + 2] = 4
        return g
    if name == "no_codes":
        # frames + templates but no transform codes → no transform dispatch
        draw_frame(g, 1, 1, 6, 6, 7)
        draw_frame(g, 1, 8, 6, 13, 8)
        for dr, dc in _PATTERN:
            g[2 + dr][2 + dc] = 2
            g[2 + dr][9 + dc] = 3
        return g
    if name == "no_template":
        # frames + codes but no template cells → nothing to transform
        draw_frame(g, 1, 1, 6, 6, 7)
        draw_frame(g, 1, 8, 6, 13, 8)
        g[5][2] = 2; g[5][3] = 4
        g[5][9] = 3; g[5][10] = 5
        return g
    return g
