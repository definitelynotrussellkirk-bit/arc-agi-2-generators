"""Generator for arc_puzzle_bank_21_set17_bundle:medium_p05 — corner-marker mirror.

Rule: (0, 0) holds a 'mirror' marker (1=horizontal mirror to right, 2=vertical
mirror to bottom). A motif elsewhere is mirrored to the opposite half.

Combinatorial axes (8): grid_h, grid_w, palette_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, motif_at_corner, motif_already_mirrored.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4b7b6d3a3a14"
VERSION = "1.1.0"
TASK_ID = "4b7b6d3a3a14"
SUMMARY = "(0,0) marker (1 or 2) + 1 motif in some other color."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds marker 1 or 2",
    "exactly one connected motif (3-5 cells) in some non-{0, 1, 2} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "motif_at_corner", "motif_already_mirrored")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker":         {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "marker_with_motif",
                       "valid": "marker_with_motif"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([1, 2])
    color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    cells = _build_motif(rng, rng.randint(3, 5))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    for _ in range(80):
        r0 = rng.randint(1, max(1, h // 2 - sh))
        c0 = rng.randint(1, max(1, w // 2 - sw))
        cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
        if any(g[r][c] != 0 for r, c in cells_p): continue
        for r, c in cells_p:
            g[r][c] = color
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    g[0][0] = 1   # horizontal mirror marker
    if name == "no_motif":
        # marker but no motif → rule has nothing to mirror, output is the marker alone
        return g
    if name == "motif_at_corner":
        # motif touches the corner cell → marker ambiguously part of motif
        for (r, c) in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 4
        return g
    if name == "motif_already_mirrored":
        # motif AND its mirror already present → rule's mirror operation is identity
        # left motif at (1,1)-(1,3), mirror at (1, w-4)-(1, w-2)
        for c in range(1, 4): g[1][c] = 4
        for c in range(w - 4, w - 1): g[1][c] = 4
        return g
    return g
