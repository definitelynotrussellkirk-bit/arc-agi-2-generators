"""Generator for arc_puzzle_bank_21_set2:S2_M1 — recolor nearest 1-object to 7.

Rule: marker = single cell of color 6. Of the color-1 objects (4-conn),
the closest one (Manhattan distance from marker to any cell of obj)
gets recolored to 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blobs, tied_distances.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f1ee291071fd"
VERSION = "1.1.0"
TASK_ID = "f1ee291071fd"
SUMMARY = "One 6-marker + 2-4 color-1 blobs at strictly distinct distances."

INVARIANTS = [
    "background is 0",
    "exactly one color-6 cell (the marker)",
    "2-4 color-1 blobs, all 4-disjoint from each other and from the marker",
    "minimum Manhattan distances from marker to each blob are strictly distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blobs", "tied_distances")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "marker_with_distinct_distance_blobs",
                       "valid": "marker_with_distinct_distance_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _man_to_cells(p, cells):
    return min(abs(p[0] - r) + abs(p[1] - c) for r, c in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    marker = (rng.randint(2, h - 3), rng.randint(2, w - 3))
    g[marker[0]][marker[1]] = 6
    used.add(marker)
    n = rng.randint(2, 4)
    blobs = []
    distances = set()
    for _ in range(n * 4):
        if len(blobs) == n:
            break
        cells = grow_blob(rng, h, w, used, rng.randint(1, 4), max_attempts=30)
        if cells is None:
            continue
        d = _man_to_cells(marker, cells)
        if d in distances or d == 0:
            continue
        distances.add(d)
        blobs.append(cells)
        used |= cells
    for cells in blobs:
        for r, c in cells:
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # 1-blobs but no 6-marker — rule has no anchor for distance.
        g[2][2] = 1; g[2][3] = 1
        g[6][7] = 1; g[7][7] = 1
        return g
    if name == "no_blobs":
        # Marker but no 1-blobs — rule has nothing to recolor.
        g[5][5] = 6
        return g
    if name == "tied_distances":
        # Two blobs at the same Manhattan distance — rule's nearest
        # selection is ambiguous.
        g[5][5] = 6
        g[5][2] = 1; g[6][2] = 1
        g[5][8] = 1; g[6][8] = 1
        return g
    return g
