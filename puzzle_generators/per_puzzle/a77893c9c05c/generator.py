"""Generator for arc_puzzle_bank_fourth21:M26 — fill rect-frames + leave non-frames.

Rule: for each blob whose shape is a rect-frame (hollow rect outline),
fill its interior with the frame's color. Non-frame blobs untouched.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, only_2x2, only_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "a77893c9c05c"
VERSION = "1.1.0"
TASK_ID = "a77893c9c05c"
SUMMARY = "1 rect-frame (≥4×4) + 1 non-frame blob, distinct colors."

INVARIANTS = [
    "background is 0",
    "≥1 rect-frame at least 4x4",
    "≥1 non-frame blob (so rule has both branches)",
    "shapes don't overlap (1-cell padding)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "only_2x2", "only_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "frame_with_distractor",
                       "valid": "frame_with_distractor"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    for _ in range(40):
        fh = rng.randint(4, 5); fw = rng.randint(4, 5)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1
        c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            for c in range(c1, c2 + 1):
                g[r1][c] = palette[0]; g[r2][c] = palette[0]
            for r in range(r1, r2 + 1):
                g[r][c1] = palette[0]; g[r][c2] = palette[0]
            break
    used = {(r, c) for r in range(h) for c in range(w) if g[r][c] != 0}
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells is not None:
        for r, c in cells:
            g[r][c] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Only non-frame blobs — rule's "fill frame interior"
        # branch never fires; output equals input.
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 4
        for r, c in [(7, 8), (7, 9), (8, 8)]: g[r][c] = 6
        return g
    if name == "only_2x2":
        # 2x2 solid blocks (not frames, no interior) — rule's
        # frame filter excludes; output equals input.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(7, 9):
            for c in range(8, 10): g[r][c] = 6
        return g
    if name == "only_distractors":
        # Multiple non-rectangular shapes only — rule's frame
        # branch never fires.
        for r, c in [(2, 2), (2, 3), (3, 3), (4, 3)]: g[r][c] = 4
        for r, c in [(6, 7), (7, 6), (7, 7), (7, 8)]: g[r][c] = 6
        return g
    return g
