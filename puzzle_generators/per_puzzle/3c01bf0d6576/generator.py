"""Generator for arc_additional_puzzles_21_set18_bundle:H121 — transform by example.

Rule: 3 isolated non-bg components sorted by (r1, c1). A and A' (first two)
demonstrate a dihedral transform. Apply the same transform to B (third) and
output the transformed B crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects (no shapes → rule has nothing to learn from);
identity_transform (A == A' → t = identity, output = B unchanged);
no_B_content (only A and A' present, no B → rule's input to t is
empty, output empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3c01bf0d6576"
VERSION = "1.1.0"
TASK_ID = "3c01bf0d6576"

SUMMARY = "3 isolated multicolor components: A, transform(A) of same shape, and an independent B."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated non-bg multicolor components",
    "first two components (sorted by r1, c1) are related by some dihedral transform t in {0..5}",
    "third component is independent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "identity_transform", "no_B_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":            {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "transform":         {"type": "int", "default": "rng 1..5", "valid": "0..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "A_Aprime_B_in_sorted_order",
                          "valid": "A_Aprime_B_in_sorted_order"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform_grid(g, t):
    if t == 0: return [row[:] for row in g]
    if t == 1:
        h, w = len(g), len(g[0])
        return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]
    if t == 2:
        return [row[::-1] for row in g[::-1]]
    if t == 3:
        h, w = len(g), len(g[0])
        return [[g[r][c] for r in range(h)] for c in range(w)]
    if t == 4:
        return [row[::-1] for row in g]
    return g[::-1]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _build_random_motif(rng, k):
    cells = [(0, 0)]
    seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc))
            seen.add((nr, nc))
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    sr0, sc0 = -min(rs), -min(cs)
    sh = max(rs) - min(rs) + 1
    sw = max(cs) - min(cs) + 1
    grid = [[0] * sw for _ in range(sh)]
    palette = [2, 3, 4, 5, 6, 7]
    rng.shuffle(palette)
    for i, (r, c) in enumerate(cells):
        grid[sr0 + r][sc0 + c] = palette[i % len(palette)]
    return grid


def _paint(g, top, left, motif):
    sh, sw = len(motif), len(motif[0])
    for r in range(sh):
        for c in range(sw):
            if motif[r][c] != 0:
                g[top + r][left + c] = motif[r][c]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 13, 16)
    t = ctx.draw_int("transform", 1, 5)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        a = _build_random_motif(rng, rng.randint(3, 5))
        ap = _xform_grid(a, t)
        if a == ap:
            continue
        b = _build_random_motif(rng, rng.randint(3, 5))
        positions = []
        ok = True
        motifs = [a, ap, b]
        for motif in motifs:
            shape_h, shape_w = len(motif), len(motif[0])
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - shape_h)
                c0 = rng.randint(0, w - shape_w)
                if not _free(g, r0, c0, r0 + shape_h - 1, c0 + shape_w - 1):
                    continue
                if positions and (r0, c0) <= positions[-1]:
                    continue
                _paint(g, r0, c0, motif)
                positions.append((r0, c0))
                placed = True
                break
            if not placed:
                ok = False
                break
        if not ok:
            continue
        return g
    raise ValueError("could not place transform-by-example layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "identity_transform":
        # A == A' (same shape, same orientation) — t = identity.
        g[1][1] = 2; g[1][2] = 3; g[2][1] = 4
        g[1][6] = 2; g[1][7] = 3; g[2][6] = 4
        g[6][10] = 5; g[6][11] = 6; g[7][10] = 7
        return g
    if name == "no_B_content":
        # Only A and A', no B — rule's input to t is empty.
        g[1][1] = 2; g[1][2] = 3; g[2][1] = 4
        g[1][6] = 4; g[2][5] = 3; g[2][6] = 2
        return g
    return g
