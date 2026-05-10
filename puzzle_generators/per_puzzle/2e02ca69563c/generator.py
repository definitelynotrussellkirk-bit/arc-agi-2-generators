"""Generator for arc_additional_puzzles_21_set8:H55.

Each rectangular frame contains two same-colored endpoints. The rule draws a
horizontal-then-vertical path between each pair.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_pairs, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "2e02ca69563c"
VERSION = "1.1.0"
TASK_ID = "2e02ca69563c"
SUMMARY = "Frames hold endpoint pairs that route as row-first Manhattan paths."

INVARIANTS = [
    "all containers are rectangular frame objects",
    "inside each frame, every routed color appears exactly twice",
    "endpoints are separated in both row and column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_pairs", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14..14"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "framed_endpoint_pairs",
                       "valid": "framed_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_frames = ctx.draw_int("n_frames", 1, 1)
        pairs_per_frame = ctx.draw_int("pairs_per_frame", 1, 1)
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 2, 2)
        pairs_per_frame = ctx.draw_int("pairs_per_frame", 2, 2)
    else:
        n_frames = ctx.draw_int("n_frames", 1, 2)
        pairs_per_frame = ctx.draw_int("pairs_per_frame", 1, 2)
    g = full_grid(14, 18, 0)
    origins = [(1, 1), (1, 10)]
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_frames * (pairs_per_frame + 1))
    for i in range(n_frames):
        r0, c0 = origins[i]
        frame_color = colors[i * (pairs_per_frame + 1)]
        draw_frame(g, r0, c0, r0 + 10, c0 + 6, frame_color)
        pair_colors = colors[i * (pairs_per_frame + 1) + 1:(i + 1) * (pairs_per_frame + 1)]
        endpoints = [((r0 + 2, c0 + 1), (r0 + 7, c0 + 4)),
                     ((r0 + 4, c0 + 1), (r0 + 8, c0 + 5))]
        for color, (a, b) in zip(pair_colors, endpoints):
            g[a[0]][a[1]] = color
            g[b[0]][b[1]] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 18, 0)
    if name == "no_frames":
        # endpoints without containing frame → no container to route inside of
        g[3][3] = 2; g[8][6] = 2
        return g
    if name == "no_pairs":
        # frames without any endpoint pairs → nothing to route
        draw_frame(g, 1, 1, 11, 7, 4)
        return g
    if name == "single_endpoint":
        # frame with 1 endpoint of color → can't form pair
        draw_frame(g, 1, 1, 11, 7, 4)
        g[3][3] = 6
        return g
    return g
