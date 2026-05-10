"""Generator for arc_puzzle_bank_twentyfirst21:M147 — marker-dispatched transform.

Rule: a marker (8 or 9) selects the transform: 8 → rotate-cw,
else → flip-lr. Apply to the (single) non-marker blob and crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, rectangular_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "97e4de6b44f4"
VERSION = "1.1.0"
TASK_ID = "97e4de6b44f4"
SUMMARY = "Marker (8 or 9) at top + a non-rectangular blob below."

INVARIANTS = [
    "background is 0",
    "exactly one marker (8 or 9) somewhere not in the blob",
    "exactly one non-marker blob, non-rectangular (so transforms differ)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "rectangular_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "marker_top_blob_below",
                       "valid": "marker_top_blob_below"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    marker = rng.choice([8, 9])
    g[0][rng.randint(w // 2, w - 1)] = marker
    used = {(r, c) for r in range(h) for c in range(w) if g[r][c] != 0}
    color = rng.choice([1, 2, 3, 4, 5, 6, 7])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blob without 8/9 marker → no transform dispatch, undefined rule
        for r, c in [(2, 2), (3, 2), (3, 3)]:
            g[r][c] = 4
        return g
    if name == "no_blob":
        # marker alone, no payload to transform
        g[0][5] = 8
        return g
    if name == "rectangular_blob":
        # solid 2x2 blob → both rotate-cw and flip-lr produce same output
        g[0][5] = 8
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 4
        return g
    return g
