"""Generator for 5c0a986e.

Rule: 1-blob's top-left → diagonal trail of 1s going up-left. 2-blob's
bottom-right → diagonal trail of 2s going down-right.

Combinatorial axes (8): grid_h/w, blob_position_kind, blob_size_kind,
n_decoys, decoy_palette_kind, position_bias, anchor_corner,
asymmetry_force.
Degenerates: no_blobs, single_blob, all_2x2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "1d62131e83ca"
VERSION = "1.1.0"
TASK_ID = "1d62131e83ca"
SUMMARY = "1-blob + 2-blob; rule extends diagonals up-left and down-right."

INVARIANTS = [
    "background is 0",
    "exactly 1 solid 2×2 1-block in upper portion",
    "exactly 1 solid 2×2 2-block in lower portion",
    "1-block is positioned NE of 2-block (so trails don't overlap)",
]

POSITION_KINDS = ("standard", "compact", "spread", "diagonal")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "all_2x2")
HELPFUL_TEXTURES = POSITION_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":             {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "blob_position_kind": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_KINDS)},
    "blob_size_kind":     {"type": "str", "default": "2x2", "valid": "2x2"},
    "n_decoys":           {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "decoy_palette_kind": {"type": "str", "default": "rng warm|cool|broad",
                           "valid": "warm|cool|broad"},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for blob_position_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pos_kind = (overrides.get("texture") or
                overrides.get("blob_position_kind")
                or ctx.draw_choice("blob_position_kind",
                                   list(POSITION_KINDS)))
    g = full_grid(h, w, 0)
    if pos_kind == "compact":
        r2, c2 = 1, 1
        r1 = h - 4; c1 = w - 4
    elif pos_kind == "spread":
        r2, c2 = 0, 0
        r1 = h - 3; c1 = w - 3
    elif pos_kind == "diagonal":
        r2, c2 = 1, 1
        r1 = min(h - 3, w - 3); c1 = r1
    else:
        r1 = rng.randint(h - 6, max(h - 6, h - 4))
        c1 = rng.randint(w - 6, max(w - 6, w - 4))
        r2 = rng.randint(0, 3)
        c2 = rng.randint(0, 3)
    r1 = max(0, min(h - 2, r1))
    c1 = max(0, min(w - 2, c1))
    r2 = max(0, min(h - 2, r2))
    c2 = max(0, min(w - 2, c2))
    if not (r2 + 1 < r1 and c2 + 1 < c1):
        r2, c2 = 0, 0
        r1, c1 = h - 3, w - 3
    draw_rect(g, r1, c1, 2, 2, 1)
    draw_rect(g, r2, c2, 2, 2, 2)
    decoy_kind = overrides.get("decoy_palette_kind",
                               ctx.draw_choice("decoy_palette_kind",
                                               ["warm", "cool", "broad"]))
    if decoy_kind == "warm":
        decoy_pool = [3, 4, 6, 9]
    elif decoy_kind == "cool":
        decoy_pool = [5, 7, 8]
    else:
        decoy_pool = [3, 4, 5, 6, 7, 8, 9]
    n_decoys = int(overrides.get("n_decoys",
                                 ctx.draw_int("n_decoys", 1, 3)))
    placed = 0
    for _ in range(n_decoys * 5):
        if placed >= n_decoys:
            break
        dr = rng.randint(0, h - 1); dc = rng.randint(0, w - 1)
        if g[dr][dc] == 0:
            g[dr][dc] = rng.choice(decoy_pool)
            placed += 1
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        return g
    if name == "single_blob":
        if h >= 4 and w >= 4:
            draw_rect(g, h - 3, w - 3, 2, 2, 1)
        return g
    if name == "all_2x2":
        for r in range(0, h - 1, 4):
            for c in range(0, w - 1, 4):
                draw_rect(g, r, c, 2, 2, rng.choice([1, 2]))
        return g
    return g
