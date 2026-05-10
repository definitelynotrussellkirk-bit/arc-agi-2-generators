"""Generator for arc_additional_puzzles_21_set16_bundle:M108 — flood 5-frame interior with the lone marker color.

Rule: each 5-color rectangle frame whose strict interior contains
exactly one non-0, non-5 color value gets its entire interior painted
with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_frames, texture.
Degenerates: no_frames, no_marker, multiple_marker_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "79fa065ed7aa"
VERSION = "1.1.0"
TASK_ID = "79fa065ed7aa"
SUMMARY = "2 5-color rectangle frames with one non-0/5 marker in each strict interior."

INVARIANTS = [
    "background is 0",
    "exactly 2 full-perimeter 5-color rectangle frames (each ≥4×4)",
    "each frame's strict interior holds exactly one non-0, non-5 marker cell",
    "frames don't touch each other (bbox padding ≥1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_marker", "multiple_marker_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_5_frames_with_marker",
                       "valid": "two_5_frames_with_marker"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 16)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        if len(placed) >= n_frames: break
        rh = rng.randint(4, 6)
        rw = rng.randint(4, 6)
        r1 = rng.randint(0, h - rh)
        c1 = rng.randint(0, w - rw)
        r2 = r1 + rh - 1
        c2 = c1 + rw - 1
        bb_pad = (r1 - 1, c1 - 1, r2 + 1, c2 + 1)
        if any(bbox_overlaps(bb_pad, (p[0]-1, p[1]-1, p[2]+1, p[3]+1)) for p in placed):
            continue
        placed.append((r1, c1, r2, c2))
    for r1, c1, r2, c2 in placed:
        draw_frame(g, r1, c1, r2, c2, 5)
        marker = rng.choice(list(random_palette(rng, 4, exclude={5})))
        sr = rng.randint(r1 + 1, r2 - 1)
        sc = rng.randint(c1 + 1, c2 - 1)
        g[sr][sc] = marker
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Markers but no 5-frames — rule's frame-finder has no
        # candidates; interiors don't exist.
        g[3][3] = 4; g[5][8] = 6
        return g
    if name == "no_marker":
        # 5-frame but interior is empty — rule's "exactly one marker
        # color" precondition fails (zero markers).
        draw_frame(g, 1, 1, 6, 8, 5)
        return g
    if name == "multiple_marker_colors":
        # 5-frame with TWO distinct marker colors inside — rule's
        # "exactly one marker color" precondition fails; flood color
        # is ambiguous.
        draw_frame(g, 1, 1, 6, 8, 5)
        g[3][3] = 4; g[4][6] = 7
        return g
    return g
