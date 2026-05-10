"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m05 — nearest-top-marker recolor.

Rule: row 0 has K colored markers at distinct cols. Each non-row-0 blob
is recolored by the row-0 marker whose column is closest to the blob's
bbox center column. Ties break by smaller marker col.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_blobs, equidistant_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "fd68649aabf7"
VERSION = "1.1.0"
TASK_ID = "fd68649aabf7"
SUMMARY = "Row 0 has 3 distinct markers + 2-3 non-row-0 blobs in different colors."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly 3 markers (distinct colors, distinct cols)",
    "below row 0: 2-3 blobs in distinct colors that differ from any row-0 marker",
    "each blob's center col has a strictly nearest row-0 marker (no ties)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_blobs", "equidistant_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "row0_markers_blobs_below",
                       "valid": "row0_markers_blobs_below"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    marker_palette = rng.sample([2, 4, 6, 8, 9], 3)
    blob_palette = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in marker_palette], 3)
    marker_cols = sorted(rng.sample(range(w), 3))
    for c, color in zip(marker_cols, marker_palette):
        g[0][c] = color
    used = {(0, c) for c in marker_cols}
    for c in range(w):
        used.add((1, c))
    for color in blob_palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # Blobs but row 0 is empty — rule has no markers to compute
        # nearest-distance against.
        for r, c in [(3, 2), (3, 3)]: g[r][c] = 4
        for r, c in [(6, 8), (6, 9)]: g[r][c] = 7
        return g
    if name == "no_blobs":
        # Markers but no blobs — rule has nothing to recolor.
        g[0][1] = 2; g[0][5] = 4; g[0][9] = 6
        return g
    if name == "equidistant_marker":
        # Blob's center column is exactly midway between two markers
        # — strict-nearest pick is ambiguous.
        g[0][2] = 2; g[0][8] = 4
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 7
        return g
    return g
