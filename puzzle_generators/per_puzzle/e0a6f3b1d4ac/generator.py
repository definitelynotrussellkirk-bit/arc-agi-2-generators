"""Generator for v2_meta_puzzles:M3 — paste obj relative to anchor.

Rule: a single-cell anchor in some color + a connected obj in another color.
The obj's offsets relative to its bbox top-left are stamped at (anchor_r+1,
anchor_c+1) in color 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_motif, anchor_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0a6f3b1d4ac"
VERSION = "1.1.0"
TASK_ID = "e0a6f3b1d4ac"

SUMMARY = "1 single-cell anchor + 1 connected motif in another color."

INVARIANTS = [
    "background is 0",
    "exactly one single-cell anchor in some non-zero color",
    "exactly one connected motif (3-5 cells) in some other non-zero color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_motif", "anchor_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "anchor_with_motif",
                       "valid": "anchor_with_motif"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    anchor_color, obj_color = 2, 3
    ar = rng.randint(0, h // 2 - 1); ac = rng.randint(0, w // 2 - 1)
    g[ar][ac] = anchor_color
    cells = _build_motif(rng, rng.randint(3, 5))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    for _ in range(80):
        r0 = rng.randint(h // 2, h - sh); c0 = rng.randint(w // 2, w - sw)
        cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
        if any(g[r][c] != 0 for r, c in cells_p): continue
        for r, c in cells_p:
            g[r][c] = obj_color
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # Motif but no anchor — rule's stamp position has no
        # reference; output is just the motif untouched.
        for r, c in [(4, 4), (4, 5), (5, 4)]: g[r][c] = 3
        return g
    if name == "no_motif":
        # Anchor but no motif — rule has nothing to stamp.
        g[1][1] = 2
        return g
    if name == "anchor_at_corner":
        # Anchor at bottom-right corner — stamp position
        # (anchor_r+1, anchor_c+1) is OOB; rule's stamp drops
        # entirely.
        g[h - 1][w - 1] = 2
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 3
        return g
    return g
