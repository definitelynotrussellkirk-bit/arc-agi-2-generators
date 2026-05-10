"""Generator for arc_puzzle_bank_eighth21:M54 — point-reflect blob around 1-anchor.

Rule: a 1-cell is the anchor. Each non-1, non-0 cell stays at (r,c) AND
also gets duplicated at (2*ar - r, 2*ac - c). Anchor stays 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor (no 1-cell → rule's anchor selector finds
nothing, no reflection), no_blob (anchor present but no non-1,
non-0 cells → rule has nothing to reflect), point_symmetric_blob
(blob is already point-symmetric around the anchor → reflection lands
on existing cells, output equals input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "406402d6defb"
VERSION = "1.1.0"
TASK_ID = "406402d6defb"
SUMMARY = "Single 1-anchor + a small blob whose reflection lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 1-cell (anchor)",
    "the (single) non-1 blob's reflected image is fully in-bounds",
    "blob and its reflection don't overlap (so output is clearly different from input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_blob", "point_symmetric_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "blob_size":         {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "anchor_plus_blob",
                          "valid": "anchor_plus_blob"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target_lo, target_hi = 2, 3
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        target_lo, target_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        target_lo, target_hi = 2, 4
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    ar = h // 2; ac = w // 2
    g[ar][ac] = 1
    used = {(ar, ac)}
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    for _ in range(40):
        ulr = ar - 1
        ulc = ac - 1
        if ulr < 1 or ulc < 1: break
        seed_pos = (rng.randint(1, ulr), rng.randint(1, ulc))
        if seed_pos in used: continue
        cells = {seed_pos}
        frontier = [seed_pos]
        target = rng.randint(target_lo, target_hi)
        while frontier and len(cells) < target:
            r0, c0 = frontier.pop(rng.randint(0, len(frontier) - 1))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r0 + dr, c0 + dc
                if 1 <= nr <= ulr and 1 <= nc <= ulc and (nr, nc) not in cells and (nr, nc) not in used:
                    cells.add((nr, nc))
                    frontier.append((nr, nc))
                    if len(cells) >= target: break
        if len(cells) < 2: continue
        ok = True
        for r, c in cells:
            mr = 2 * ar - r; mc = 2 * ac - c
            if not (0 <= mr < h and 0 <= mc < w):
                ok = False; break
            if (mr, mc) in cells or (mr, mc) == (ar, ac):
                ok = False; break
        if not ok: continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # No 1-cell → rule's anchor selector finds nothing; no reflection.
        g[2][2] = 4; g[2][3] = 4; g[3][2] = 4
        return g
    if name == "no_blob":
        # Anchor present but no non-1, non-0 cells — rule has nothing
        # to reflect.
        g[4][4] = 1
        return g
    if name == "point_symmetric_blob":
        # Blob is already point-symmetric around (4,4) — reflecting
        # lands on existing cells; output equals input.
        g[4][4] = 1
        g[2][2] = 6; g[6][6] = 6   # symmetric pair
        g[2][6] = 6; g[6][2] = 6   # symmetric pair
        return g
    return g
