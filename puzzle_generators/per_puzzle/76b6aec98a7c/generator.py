"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_49_rotation_code_mosaic.

Rule: a color-1 frame contains a source motif. A dense code grid of
values 2..5 outside the frame expands into a rotation mosaic of that
motif.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_motif, no_code_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "76b6aec98a7c"
VERSION = "1.1.0"
TASK_ID = "76b6aec98a7c"
SUMMARY = "Expand a 2..5 rotation-code grid into repeated rotations of a framed motif."

INVARIANTS = [
    "there is one hollow color-1 frame",
    "the frame interior contains one nonzero source color",
    "the code grid outside the frame is rectangular and fully filled with values 2..5",
    "each code cell maps to a rotation count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_motif", "no_code_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code_h":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "code_w":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "frame_with_motif_and_code",
                       "valid": "frame_with_motif_and_code"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIF = [(0, 0), (1, 0), (1, 1)]


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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        code_h = ctx.draw_int("code_h", 2, 2)
        code_w = ctx.draw_int("code_w", 2, 2)
    elif difficulty == "hard":
        code_h = ctx.draw_int("code_h", 3, 3)
        code_w = ctx.draw_int("code_w", 3, 3)
    else:
        code_h = ctx.draw_int("code_h", 2, 3)
        code_w = ctx.draw_int("code_w", 2, 3)
    source_color = rng.choice([3, 4, 6, 7, 8])
    g = full_grid(11, 12, 0)
    draw_frame(g, 1, 1, 5, 5, 1)
    for dr, dc in _MOTIF:
        g[2 + dr][2 + dc] = source_color
    for r in range(code_h):
        for c in range(code_w):
            g[7 + r][1 + c] = rng.choice([2, 3, 4, 5])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_frame":
        # motif + code grid but no 1-frame → no mosaic anchor
        for dr, dc in _MOTIF:
            g[2 + dr][2 + dc] = 6
        for r in range(2):
            for c in range(2): g[7 + r][1 + c] = 2
        return g
    if name == "no_motif":
        # frame + code grid but no source motif → nothing to rotate
        draw_frame(g, 1, 1, 5, 5, 1)
        for r in range(2):
            for c in range(2): g[7 + r][1 + c] = 2
        return g
    if name == "no_code_grid":
        # frame + motif but no code grid → no rotation expansion specified
        draw_frame(g, 1, 1, 5, 5, 1)
        for dr, dc in _MOTIF:
            g[2 + dr][2 + dc] = 6
        return g
    return g
