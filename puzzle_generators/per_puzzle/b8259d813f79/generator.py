"""Generator for arc_puzzle_bank_21_set15_bundle:medium_o01 — mark blob's bbox-center.

Rule: replace each blob with a single dot at its bbox center
(integer-divided), in that blob's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, single_blob, centers_collide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "b8259d813f79"
VERSION = "1.1.0"
TASK_ID = "b8259d813f79"
SUMMARY = "2-4 distinct-color blobs of size >= 3 with distinct bbox centers."

INVARIANTS = [
    "background is 0",
    "blobs have size >= 3 (so single-cell isn't trivially identity)",
    "bbox-center cells of different blobs are distinct positions",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "single_blob", "centers_collide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 4)
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
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # all blobs are single cells → bbox center is the cell itself, rule is identity
        for r, c, v in [(2, 2, 4), (4, 5, 5), (6, 8, 6)]:
            g[r][c] = v
        return g
    if name == "single_blob":
        # one blob → no comparison among objects, rule still works trivially
        for r, c in [(3, 3), (3, 4), (4, 3), (4, 4), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "centers_collide":
        # multiple blobs share the same bbox center → "distinct centers" invariant violated, output ambiguous
        for r, c in [(2, 2), (2, 4), (4, 2), (4, 4)]:
            g[r][c] = 4
        for r, c in [(2, 3), (3, 2), (3, 4), (4, 3)]:
            g[r][c] = 6
        return g
    return g
