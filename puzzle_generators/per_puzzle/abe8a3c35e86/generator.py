"""Generator for arc_puzzle_bank_twentythird21:M155 — mirror objects across color-9 anchor.

Rule: a single color-9 anchor cell + a connected motif on one side of it.
Output mirrors the motif's cells to the other side around the anchor's row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor (no color-9 cell → rule's mirror axis is
undefined), no_motif (anchor present but no motif → rule has nothing
to mirror; output equals input), motif_at_anchor_row (motif spans
anchor row → rule's "one side" condition violated, mirror lands on
top of original).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "abe8a3c35e86"
VERSION = "1.1.0"
TASK_ID = "abe8a3c35e86"

SUMMARY = "1 color-9 anchor + 1 connected non-{0,9} motif entirely on one side of the anchor (vertical)."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 single-cell anchor",
    "exactly one connected motif (3-5 cells) in some non-{0, 9} color, entirely above or below the anchor row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_motif", "motif_at_anchor_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "anchor_plus_one_side_motif",
                          "valid": "anchor_plus_one_side_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 8, 8)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        max_motif_r = max(0, h // 2 - sh - 1)
        if max_motif_r < 0:
            continue
        r0 = rng.randint(0, max_motif_r)
        c0 = rng.randint(0, w - sw)
        for r, c in cells:
            g[r0 + r - min(rs)][c0 + c - min(cs)] = color
        motif_max_r = r0 + sh - 1
        anchor_min = motif_max_r + 2
        anchor_max = h - 2
        anchor_min_for_mirror = motif_max_r + (sh + 1) // 2 + 1
        anchor_min = max(anchor_min, anchor_min_for_mirror)
        if anchor_min > anchor_max:
            continue
        placed = False
        for _ in range(120):
            ar = rng.randint(anchor_min, anchor_max)
            ac = rng.randint(0, w - 1)
            if g[ar][ac] != 0: continue
            ok = True
            for r, c in cells:
                mr = 2 * ar - (r0 + r - min(rs))
                if not (0 <= mr < h): ok = False; break
            if not ok: continue
            g[ar][ac] = 9
            placed = True; break
        if placed:
            return g
    raise ValueError("could not realize M155 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 7
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # No color-9 cell — rule's mirror axis is undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_motif":
        # Anchor present but no motif — rule has nothing to mirror.
        g[5][3] = 9
        return g
    if name == "motif_at_anchor_row":
        # Motif spans anchor row — rule's "one side" condition violated;
        # mirror lands on top of original.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[4 + dr][2 + dc] = 4   # spans rows 4-5
        g[4][5] = 9   # anchor on same row
        return g
    return g
