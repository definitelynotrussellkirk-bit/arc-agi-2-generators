"""Generator for v3_rich_schema:medium_03_fill_keyed_rectangle_holes — fill keyed-frame interior with 8.

Rule: 2 hollow rectangle frames in distinct colors. A lone marker
elsewhere matches one of the frame colors — that frame's interior
gets filled with 8. The other frame is unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_match, marker_matches_both.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "d95f9ada9be5"
VERSION = "1.1.0"
TASK_ID = "d95f9ada9be5"
SUMMARY = "2 hollow rect frames in distinct colors + 1 lone marker matching one frame's color."

INVARIANTS = [
    "background is 0",
    "exactly 2 full-perimeter rectangle frames (each ≥4×4) in distinct non-bg, non-8 colors",
    "exactly one isolated single-cell marker matching the color of exactly one frame",
    "frames and marker don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_match", "marker_matches_both")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "two_frames_one_marker",
                       "valid": "two_frames_one_marker"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 2, exclude={8}))
    placed: list[tuple[int, int, int, int]] = []
    for color in palette:
        for _ in range(80):
            rh = rng.randint(4, 5)
            rw = rng.randint(4, 5)
            r1 = rng.randint(0, h - rh)
            c1 = rng.randint(0, w - rw)
            r2 = r1 + rh - 1
            c2 = c1 + rw - 1
            bb_pad = (r1 - 1, c1 - 1, r2 + 1, c2 + 1)
            if any(bbox_overlaps(bb_pad, (p[0]-1, p[1]-1, p[2]+1, p[3]+1)) for p in placed):
                continue
            draw_frame(g, r1, c1, r2, c2, color)
            placed.append((r1, c1, r2, c2))
            break
    keyed = palette[rng.randint(0, 1)]
    for _ in range(80):
        mr = rng.randint(0, h - 1)
        mc = rng.randint(0, w - 1)
        if g[mr][mc] != 0: continue
        if any(p[0]-1 <= mr <= p[2]+1 and p[1]-1 <= mc <= p[3]+1 for p in placed): continue
        g[mr][mc] = keyed
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # Frames present but no marker — rule has no frame to select.
        draw_frame(g, 1, 1, 4, 5, 3)
        draw_frame(g, 1, 7, 4, 11, 4)
        return g
    if name == "no_match":
        # Marker color matches neither frame — rule has no frame to fill.
        draw_frame(g, 1, 1, 4, 5, 3)
        draw_frame(g, 1, 7, 4, 11, 4)
        g[8][3] = 6
        return g
    if name == "marker_matches_both":
        # Two frames share the same color — marker matches both, ambiguous.
        draw_frame(g, 1, 1, 4, 5, 3)
        draw_frame(g, 1, 7, 4, 11, 3)
        g[8][3] = 3
        return g
    return g
