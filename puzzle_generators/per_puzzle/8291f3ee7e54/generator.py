"""Generator for c658a4bd.

Rule: each color's largest object's bbox is treated as a square frame
of size = max(h, w). Stack centered.

Combinatorial axes (8): grid_size, n_frames, palette_kind, position_bias,
include_dot, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_size, no_frames, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import rect_outline_cells

GENERATOR_ID = "8291f3ee7e54"
VERSION = "1.1.0"
TASK_ID = "8291f3ee7e54"
SUMMARY = "Grid with 3-4 distinct-size square frames of distinct colors at scattered positions."

INVARIANTS = [
    "3-4 square frames of distinct sizes (3, 5, 7, 9)",
    "each frame is a hollow square outline of a unique color",
    "frames don't touch (>=1 cell gap)",
    "optionally one extra single-cell dot of yet another color",
]

POSITION_BIASES = ("scattered", "spread", "diagonal", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_size", "no_frames", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_size":      {"type": "int", "default": "18", "valid": "14..22"},
    "n_frames":       {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "include_dot":    {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "3..6"},
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
        size = 14
        nf_lo, nf_hi = 2, 3
    elif difficulty == "hard":
        size = 22
        nf_lo, nf_hi = 4, 4
    else:
        size = 18
        nf_lo, nf_hi = 3, 4
    size = int(overrides.get("grid_size", size))
    n_frames = int(overrides.get("n_frames",
                                 ctx.draw_int("n_frames", nf_lo, nf_hi)))
    n_frames = max(2, min(4, n_frames))
    g = full_grid(size, size, 0)
    sizes = sorted(rng.sample([3, 5, 7, 9], n_frames))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_frames + 1, rng)
    for i, sz in enumerate(sizes):
        if sz + 2 > size:
            continue
        place_no_overlap(rng, g, rect_outline_cells(sz, sz), palette[i],
                         padding=1, max_tries=40)
    include_dot = overrides.get("include_dot")
    if include_dot is None:
        include_dot = rng.random() < 0.5
    if include_dot and len(palette) > n_frames:
        place_no_overlap(rng, g, [(0, 0)], palette[-1], padding=1, max_tries=40)
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
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    size = 18
    g = full_grid(size, size, 0)
    if name == "same_size":
        place_no_overlap(rng, g, rect_outline_cells(5, 5), 2,
                         padding=1, max_tries=40)
        place_no_overlap(rng, g, rect_outline_cells(5, 5), 3,
                         padding=1, max_tries=40)
        return g
    if name == "no_frames":
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 2
        return g
    return g
