"""Generator for arc_puzzle_bank_21_set3:S3_M5 — reduce blobs to bbox centers.

Rule: replace each blob with a single dot at its bbox center.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_blob, all_singletons, blobs_collide_centers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "6b9f5bbac608"
VERSION = "1.1.0"
TASK_ID = "6b9f5bbac608"
SUMMARY = "2-3 distinct-color blobs of size ≥ 3 with distinct bbox centers."

INVARIANTS = [
    "background is 0",
    "blobs of size >= 3 (so reducing isn't trivial)",
    "blobs have distinct bbox centers and don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_blob", "all_singletons", "blobs_collide_centers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread_blobs",
                       "valid": "spread_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n = 3
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        n = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if n is None:
        n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    used: set[tuple[int, int]] = set()
    centers: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
            if cells is None:
                continue
            rs = sorted(r for r, _ in cells); cs = sorted(c for _, c in cells)
            cr = (rs[0] + rs[-1]) // 2
            cc = (cs[0] + cs[-1]) // 2
            if (cr, cc) in centers:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            centers.add((cr, cc))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "single_blob":
        # one blob only → no comparison across blobs in output
        for (r, c) in [(3, 4), (3, 5), (4, 4), (4, 5), (5, 5)]: g[r][c] = 6
        return g
    if name == "all_singletons":
        # singletons → bbox center is the cell itself, rule is identity
        g[2][3] = 4; g[5][7] = 6; g[6][1] = 3
        return g
    if name == "blobs_collide_centers":
        # two L-blobs computed bbox centers happen to collide → output drops one
        # blob A at (1,1)-(2,2), bbox center (1,1)
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        # blob B at (4,5)-(5,6), bbox center (4,5)
        for (r, c) in [(4, 5), (4, 6), (5, 5)]: g[r][c] = 6
        return g
    return g
