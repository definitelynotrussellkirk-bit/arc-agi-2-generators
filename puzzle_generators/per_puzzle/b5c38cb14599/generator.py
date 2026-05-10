"""Generator for arc_puzzle_bank_21_set21_bundle:hard_p02 — (0,0) key + 2 motifs in colors 4 and 6.

Rule: (0, 0) holds the op key (1=union, 2=intersect, else=symmetric-diff).
Two largest non-{key, 0} components are taken; their normalized shapes are
combined per the op; output painted color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, missing_motif, identical_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5c38cb14599"
VERSION = "1.1.0"
TASK_ID = "b5c38cb14599"

SUMMARY = "(0,0) holds the op key + color-4 motif + color-6 motif at distinct positions."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds an op key (1, 2, or 3)",
    "≥3 color-4 cells (a connected motif) and ≥3 color-6 cells",
    "no other non-bg colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "missing_motif", "identical_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "key_corner_with_two_motifs",
                       "valid": "key_corner_with_two_motifs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        op = rng.choice([1, 2, 3])
        g[0][0] = op
        for color in (4, 6):
            n = rng.randint(3, 5)
            cells = _build_motif(rng, n)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(80):
                r0 = rng.randint(1, h - sh); c0 = rng.randint(0, w - sw)
                cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
                if any(g[r][c] != 0 for r, c in cells_p): continue
                for r, c in cells_p:
                    g[r][c] = color
                placed = True; break
            if not placed:
                break
        else:
            return g
    raise ValueError("could not realize set21 p02 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_key":
        # Both motifs but (0,0) empty — rule's op key lookup
        # fails; combine undefined.
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 4
        for r, c in [(5, 7), (6, 7), (6, 8)]: g[r][c] = 6
        return g
    if name == "missing_motif":
        # Key + only one of the motifs — rule's binary combine
        # has only one operand.
        g[0][0] = 1
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 4
        return g
    if name == "identical_motifs":
        # Both motifs at the same normalized shape — rule's
        # union/intersect both yield that shape; sym-diff yields
        # empty; rule's branch differentiation collapses.
        g[0][0] = 1
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(5, 7), (5, 8), (6, 7)]: g[r][c] = 6
        return g
    return g
