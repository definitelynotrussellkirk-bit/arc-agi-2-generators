"""Generator for arc_additional_puzzles_21_set13_bundle:M85 — token-kernel paint inside 1-frames.

Rule: each 1-color rectangle frame ≥3x3 has interior cells. The last
non-zero interior cell with value in {2,3,4} is the kernel token; the
last interior cell with another non-zero value is the seed. Output
keeps only the frames; for each frame, paints the seed-color into the
seed's offsets given by the kernel (2=plus, 3=X, 4=full3x3),
restricted to strict interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-1 frames → rule has no chambers);
no_token (frames but no token cell → rule has no kernel); no_seed
(frames + token but no seed cell → rule has no source color).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "d4ea5a7deae6"
VERSION = "1.1.0"
TASK_ID = "d4ea5a7deae6"
SUMMARY = "2 1-color rectangle frames; each holds a token (2/3/4) and a seed in its interior."

INVARIANTS = [
    "background is 0",
    "exactly 2 full-perimeter 1-color rectangle frames (each ≥4×4 so interior is non-trivial)",
    "each frame's interior has 1 token cell with value in {2, 3, 4} and 1 seed cell with another color",
    "frames don't touch each other (bbox padding ≥1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_token", "no_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "n_frames":          {"type": "int", "default": "rng 2..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "frames_with_token_and_seed",
                          "valid": "frames_with_token_and_seed"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
    n_frames = ctx.draw_int("n_frames", 2, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        if len(placed) >= n_frames: break
        rh = rng.randint(4, 5)
        rw = rng.randint(4, 5)
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
        interior_cells = [(r, c) for r in range(r1 + 1, r2)
                                  for c in range(c1 + 1, c2)]
        if len(interior_cells) < 2:
            continue
        rng.shuffle(interior_cells)
        token_pos = interior_cells[0]
        seed_pos = interior_cells[1]
        token = rng.choice([2, 3, 4])
        seed_color = rng.choice([5, 6, 7, 8, 9])
        g[token_pos[0]][token_pos[1]] = token
        g[seed_pos[0]][seed_pos[1]] = seed_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No 1-frames — rule has no chambers.
        g[3][4] = 2; g[3][5] = 5
        g[6][8] = 3; g[6][9] = 6
        return g
    if name == "no_token":
        # Frames but interiors have no kernel token (no {2,3,4}).
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 1, 7, 4, 11, 1)
        g[2][2] = 5; g[2][8] = 6
        return g
    if name == "no_seed":
        # Frames + token but no seed of distinct color.
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 1, 7, 4, 11, 1)
        g[2][2] = 2; g[2][8] = 3
        return g
    return g
