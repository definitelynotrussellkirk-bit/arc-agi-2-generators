"""Generator for additional_scaffolded:M1 — fill seeded 1-frame interior with 4.

Rule: among 1-color rectangle frames, the one whose interior contains
a 2-cell gets its full interior repainted with 4 (covering both 0s and
the 2). Other frames stay unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_frames, texture.
Degenerates: no_frames, no_seed, multi_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "59c2f0a5d4a9"
VERSION = "1.1.0"
TASK_ID = "59c2f0a5d4a9"
SUMMARY = "2-3 1-color rectangle frames; exactly one contains a 2-marker in its interior."

INVARIANTS = [
    "background is 0",
    "all frames are full-perimeter rectangles in color 1",
    "exactly one frame contains a 2-cell in its interior",
    "other frames have empty interiors",
    "frames don't touch each other (≥1 gap of bg)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seed", "multi_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "scattered_1_frames_one_seeded",
                       "valid": "scattered_1_frames_one_seeded"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(60):
        if len(placed) >= n_frames:
            break
        rh = rng.randint(3, 5)
        rw = rng.randint(3, 5)
        r1 = rng.randint(0, h - rh)
        c1 = rng.randint(0, w - rw)
        r2 = r1 + rh - 1
        c2 = c1 + rw - 1
        bb_pad = (r1 - 1, c1 - 1, r2 + 1, c2 + 1)
        if any(bbox_overlaps(bb_pad, (p[0]-1, p[1]-1, p[2]+1, p[3]+1)) for p in placed):
            continue
        placed.append((r1, c1, r2, c2))
    for r1, c1, r2, c2 in placed:
        draw_frame(g, r1, c1, r2, c2, 1)
    if placed:
        sf = rng.choice(placed)
        r1, c1, r2, c2 = sf
        sr = rng.randint(r1 + 1, r2 - 1)
        sc = rng.randint(c1 + 1, c2 - 1)
        g[sr][sc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # 2-seed but no 1-frames — rule has no frame to fill.
        g[3][3] = 2
        return g
    if name == "no_seed":
        # 1-frames but no 2-seed inside any of them — rule's
        # "frame containing a 2" finds none; rule's effect is invisible.
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 5, 6, 8, 10, 1)
        return g
    if name == "multi_seeds":
        # Multiple frames each contain a 2-seed — rule's
        # "exactly one" precondition fails; ambiguous which to fill.
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 5, 6, 8, 10, 1)
        g[2][2] = 2
        g[6][8] = 2
        return g
    return g
