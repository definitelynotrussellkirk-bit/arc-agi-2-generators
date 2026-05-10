"""Generator for arc_puzzle_bank_21_set20_bundle:medium_p04 — axis-key reflect.

Rule: at(0,0) = key. key=1 → flip-lr the rest, key=2 → flip-ud, else
identity. Output is the cropped result.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, blob_already_symmetric, blob_outside_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "1e92a4eef51d"
VERSION = "1.1.0"
TASK_ID = "1e92a4eef51d"
SUMMARY = "Key 1 or 2 at (0,0) + a non-symmetric blob away from corner."

INVARIANTS = [
    "background is 0",
    "(0,0) holds key in {1, 2} (so flip is non-identity)",
    "the rest of the grid has a non-symmetric blob (so flip output != identity output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "blob_already_symmetric", "blob_outside_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "corner_key",
                       "valid": "corner_key"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    key = rng.choice([1, 2])
    g[0][0] = key
    used = {(0, 0)}
    palette = rng.sample([3, 4, 5, 6, 7, 8, 9], 2)
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(4, 5), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb_h = max(rs) - min(rs) + 1
        bb_w = max(cs) - min(cs) + 1
        if bb_h * bb_w == len(cells):
            continue
        for r, c in cells:
            g[r][c] = palette[0]
        used |= cells
        for r, c in sorted(cells)[:1]:
            g[r][c] = palette[1]
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_key":
        # (0,0) is 0 (or some color other than 1/2) → rule defaults to identity, no flip
        g[0][0] = 5
        for r, c, v in [(2, 3, 4), (3, 3, 4), (3, 4, 4), (4, 5, 7)]:
            g[r][c] = v
        return g
    if name == "blob_already_symmetric":
        # blob is LR-symmetric already → flip-lr produces same output as identity
        g[0][0] = 1
        for r, c in [(3, 3), (3, 4), (3, 5), (4, 4)]:
            g[r][c] = 6
        return g
    if name == "blob_outside_corner":
        # extra non-bg cells in row 0 / col 0 (besides key) confuse "key vs blob" decomposition
        g[0][0] = 2
        g[0][3] = 5
        g[2][0] = 5
        for r, c in [(4, 5), (4, 6), (5, 5)]:
            g[r][c] = 4
        return g
    return g
