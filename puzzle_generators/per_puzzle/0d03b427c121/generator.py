"""Generator for arc_puzzle_bank_21_set11_s:S11_H6 — Find blob with target area+boundary; output bbox-cropped boundary mask.

Rule: area = count of 1s in row 0; bcount = count of 2s in row 0. Find
body blob with size=area AND boundary=bcount; output bbox-cropped boundary
in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_distractors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d03b427c121"
VERSION = "1.1.0"
TASK_ID = "0d03b427c121"
SUMMARY = "Row 0 has k 1-cells and m 2-cells; body has blob with matching size+boundary."

INVARIANTS = [
    "row 0 has k 1-cells (area marker)",
    "row 0 has m 2-cells (boundary marker)",
    "exactly one body blob has size=k AND boundary count=m",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "row0_markers_body_blobs",
                       "valid": "row0_markers_body_blobs"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
    h, w = 4, 16
    g = full_grid(h, w, 0)
    # Solid 2x4 (size 8, boundary 8) → k=8, m=8 in row 0
    for c in range(8):
        g[0][c] = 1
    for c in range(8, 16):
        g[0][c] = 2
    # Solid 2x4 blob (size 8, all 8 are boundary)
    color3 = rng.choice([3, 4, 6])
    for r in range(1, 3):
        for c in range(0, 4):
            g[r][c] = color3
    # Distractor: 2x3 solid (size 6)
    color4 = rng.choice([5, 7])
    if color4 == color3: color4 = 9
    for r in range(1, 3):
        for c in range(8, 11):
            g[r][c] = color4
    # Distractor: 3x4 hollow frame (size 10)
    color5 = 9 if color3 != 9 and color4 != 9 else 7
    g[1][12] = color5; g[1][13] = color5; g[1][14] = color5; g[1][15] = color5
    g[2][12] = color5; g[2][15] = color5
    g[3][12] = color5; g[3][13] = color5; g[3][14] = color5; g[3][15] = color5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 16
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 empty → no area/boundary specification, undefined target
        for r in range(1, 3):
            for c in range(0, 4):
                g[r][c] = 4
        return g
    if name == "no_match":
        # markers specify (size=8, boundary=8) but no body blob matches
        for c in range(8): g[0][c] = 1
        for c in range(8, 16): g[0][c] = 2
        # only a small 1x2 blob, no size-8 match
        for r, c in [(2, 0), (2, 1)]: g[r][c] = 4
        return g
    if name == "multiple_matches":
        # 2 blobs both match (size=8, boundary=8) → ambiguous target
        for c in range(8): g[0][c] = 1
        for c in range(8, 16): g[0][c] = 2
        # two 2x4 solid blobs
        for r in range(1, 3):
            for c in range(0, 4): g[r][c] = 4
            for c in range(8, 12): g[r][c] = 6
        return g
    return g
