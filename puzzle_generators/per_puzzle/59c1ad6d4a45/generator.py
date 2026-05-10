"""Generator for arc_puzzle_bank_sixth_21_bundle:hard_36_local_diagonal_rays_in_frames.

From local color-2 seeds inside color-5 frames, draw bounded diagonal rays around blockers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_frame, seed_outside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "59c1ad6d4a45"
VERSION = "1.1.0"
TASK_ID = "59c1ad6d4a45"
SUMMARY = "From local color-2 seeds inside color-5 frames, draw bounded diagonal rays around blockers."

INVARIANTS = [
    "color-5 frames define local bounded work areas",
    "color-2 cells inside frame interiors are diagonal ray emitters",
    "color-6 cells block rays but are preserved",
    "emitted diagonal paths are recolored to 8 inside each frame interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_frame", "seed_outside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_frames_with_seeds",
                       "valid": "two_frames_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BLOCKERS = [
    [(1, 1), (3, 3)],
    [(0, 4), (4, 0)],
    [(1, 3), (3, 1)],
    [(0, 0), (4, 4)],
    [(0, 2), (4, 2)],
]


def _add_frame(g, top, left, seed, blockers):
    draw_frame(g, top, left, top + 6, left + 6, 5)
    sr, sc = seed
    g[top + 1 + sr][left + 1 + sc] = 2
    for r, c in blockers:
        g[top + 1 + r][left + 1 + c] = 6


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    variant = (ctx.draw_int("variant", 0, len(_BLOCKERS) - 1) + sample_index) % len(_BLOCKERS)
    g = full_grid(8, 15, 0)
    _add_frame(g, 0, 0, (2, 2), _BLOCKERS[variant])
    _add_frame(g, 0, 8, (1 + variant % 3, 3), _BLOCKERS[-1 - variant][:1])
    g[7][(sample_index * 3 + variant) % 15] = 7 + (sample_index % 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 15, 0)
    if name == "no_seed":
        # frames without color-2 seeds → no rays to draw
        draw_frame(g, 0, 0, 6, 6, 5)
        return g
    if name == "no_frame":
        # color-2 seed without frame → no bounded work area for ray emission
        g[3][3] = 2
        return g
    if name == "seed_outside_frame":
        # color-2 seed outside the frame → ray has no enclosing region
        draw_frame(g, 0, 0, 6, 6, 5)
        g[7][10] = 2  # outside both frame and frame interior
        return g
    return g
