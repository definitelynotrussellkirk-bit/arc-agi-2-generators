"""Generator for arc_puzzle_bank_eleventh21:M75 — point-reflect through anchor (keep 8 fixed).

Rule: 8-cell is fixed point. Each non-{0,8} cell stays AND its
reflection through the 8-cell is also painted (in same color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, multiple_anchors, blob_through_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef82795e0087"
VERSION = "1.1.0"
TASK_ID = "ef82795e0087"
SUMMARY = "8-anchor + a small blob whose reflection lands in-bounds without overlap."

INVARIANTS = [
    "background is 0",
    "exactly one 8-cell at grid center",
    "the (single) non-8 blob's reflection is fully in-bounds",
    "blob and reflection are disjoint (so output != input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "multiple_anchors", "blob_through_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "centered_anchor_with_offset_blob",
                       "valid": "centered_anchor_with_offset_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    ar = h // 2; ac = w // 2
    g[ar][ac] = 8
    used = {(ar, ac)}
    color = rng.choice([2, 3, 4, 5, 6, 7, 9])
    for _ in range(40):
        ulr = ar - 1; ulc = ac - 1
        if ulr < 1 or ulc < 1: break
        seed_pt = (rng.randint(0, ulr), rng.randint(0, ulc))
        if seed_pt in used: continue
        cells = {seed_pt}
        frontier = [seed_pt]
        target = rng.randint(2, 4)
        while frontier and len(cells) < target:
            r0, c0 = frontier.pop(rng.randint(0, len(frontier) - 1))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r0 + dr, c0 + dc
                if 0 <= nr <= ulr and 0 <= nc <= ulc and (nr, nc) not in cells:
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
    ar, ac = h // 2, w // 2
    if name == "no_anchor":
        # missing 8-cell → no reflection center, rule undefined
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "multiple_anchors":
        # two 8-cells → ambiguous which is the reflection center
        g[2][2] = 8
        g[6][6] = 8
        g[1][1] = 4; g[1][2] = 4
        return g
    if name == "blob_through_anchor":
        # blob symmetric through anchor → reflection equals original (rule is identity)
        g[ar][ac] = 8
        # symmetric pair: (ar-1, ac) and (ar+1, ac) are reflections of each other; if both present
        g[ar - 1][ac] = 4; g[ar + 1][ac] = 4
        g[ar][ac - 1] = 6; g[ar][ac + 1] = 6
        return g
    return g
