"""Generator for arc_puzzle_bank_21_set20_bundle:hard_p04 — set-op on color-4 and color-5 cells.

Rule: (0, 0) holds the op (1=union, 2=intersect, 3=xor). The top-right
cell holds the transform for the second shape (6=identity, 7=flip horizontal,
8=rotate 90 degrees). Color-4 cells form set a; color-5 cells form set b.
Both are normalized to bbox top-left, composed, and emitted in color 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_op (cell (0,0) is bg → rule's op selector returns
nothing), no_transform (top-right is bg → rule's transform code
selector returns nothing), missing_color (no color-4 OR no color-5 →
rule's set-op has only one operand).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "655ca4b10a8c"
VERSION = "1.1.0"
TASK_ID = "655ca4b10a8c"

SUMMARY = "(0,0)=op key; top-right transform key; color-4 and color-5 clusters."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds op key 1 for union",
    "top-right holds transform key 6, 7, or 8",
    "at least three color-4 cells and at least three color-5 cells",
    "no other non-bg colors besides the two keys",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_op", "no_transform", "missing_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "op_tf_plus_two_clusters",
                          "valid": "op_tf_plus_two_clusters"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]
    seen = {(0, 0)}
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
        w = ctx.draw_int("grid_w", 11, 11)
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_lo, n_hi = 4, 5
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_lo, n_hi = 3, 5
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        op = 1
        tcode = rng.choice([6, 7, 8])
        g[0][0] = op
        g[0][w - 1] = tcode
        n_a = rng.randint(n_lo, n_hi)
        cells_a = _build_motif(rng, n_a)
        rs = [r for r, _ in cells_a]; cs = [c for _, c in cells_a]
        sh_a = max(rs) - min(rs) + 1; sw_a = max(cs) - min(cs) + 1
        placed_a = False
        for _ in range(80):
            r0 = rng.randint(1, h - sh_a); c0 = rng.randint(0, w - sw_a)
            cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells_a]
            if any(g[r][c] != 0 for r, c in cells_p):
                continue
            for r, c in cells_p:
                g[r][c] = 4
            placed_a = True; break
        if not placed_a:
            continue
        n_b = rng.randint(n_lo, n_hi)
        cells_b = _build_motif(rng, n_b)
        rs = [r for r, _ in cells_b]; cs = [c for _, c in cells_b]
        sh_b = max(rs) - min(rs) + 1; sw_b = max(cs) - min(cs) + 1
        for _ in range(80):
            r0 = rng.randint(1, h - sh_b); c0 = rng.randint(0, w - sw_b)
            cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells_b]
            if any(g[r][c] != 0 for r, c in cells_p):
                continue
            for r, c in cells_p:
                g[r][c] = 5
            return g
    raise ValueError("could not realize set20 p04 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_op":
        # (0,0) is bg — rule's op selector returns nothing.
        g[0][w - 1] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 5
        return g
    if name == "no_transform":
        # Top-right is bg — rule's transform code selector returns nothing.
        g[0][0] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 5
        return g
    if name == "missing_color":
        # No color-5 — rule's set-op has only one operand.
        g[0][0] = 1
        g[0][w - 1] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][3 + dc] = 4
        return g
    return g
