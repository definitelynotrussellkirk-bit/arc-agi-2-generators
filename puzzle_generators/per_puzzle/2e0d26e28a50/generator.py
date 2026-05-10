"""Generator for arc_puzzle_bank_21_set15:S15_H1 — stamp color-2 offsets at color-1 marker.

Rule: a color-2 reference shape + a single-cell color-1 marker. The relative
offsets of the color-2 cells are stamped at the marker's position in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_reference, marker_inside_ref.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e0d26e28a50"
VERSION = "1.1.0"
TASK_ID = "2e0d26e28a50"

SUMMARY = "1 color-2 reference shape (3-5 cells) + 1 single-cell color-1 marker."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 connected motif (3-5 cells)",
    "exactly one single-cell color-1 marker, sufficiently far from the reference",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_reference", "marker_inside_ref")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "ref_upper_left_marker_lower",
                       "valid": "ref_upper_left_marker_lower"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 15)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        # ref in upper-left
        r0 = rng.randint(0, max(0, h // 2 - sh - 1))
        c0 = rng.randint(0, max(0, w // 3 - sw))
        for r, c in cells:
            g[r0 + r - min(rs)][c0 + c - min(cs)] = 2
        # marker in lower-right
        for _ in range(80):
            r = rng.randint(h // 2, h - 2); c = rng.randint(w // 2, w - 2)
            if g[r][c] != 0: continue
            if any(g[r + dr][c + dc] != 0 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                   if 0 <= r + dr < h and 0 <= c + dc < w):
                continue
            g[r][c] = 1
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # Reference shape but no color-1 marker — rule has no anchor to stamp at.
        g[1][1] = 2; g[1][2] = 2; g[2][1] = 2
        return g
    if name == "no_reference":
        # Marker but no color-2 reference — rule has no offsets to stamp.
        g[6][9] = 1
        return g
    if name == "marker_inside_ref":
        # Marker overlaps reference bbox — stamp position is ambiguous.
        g[1][1] = 2; g[1][2] = 2; g[2][1] = 2
        g[1][3] = 1
        return g
    return g
