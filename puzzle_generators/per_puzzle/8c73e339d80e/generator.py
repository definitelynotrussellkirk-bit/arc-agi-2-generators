"""Generator for arc_puzzle_bank_21_set10_s:S10_H2 — rotate-stamp at color-1 markers.

Rule: a base shape in some color + color-1 markers; the base is rotated by
each marker's neighbor rotation code and stamped at the marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_base, no_markers, no_rotation_codes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8c73e339d80e"
VERSION = "1.1.0"
TASK_ID = "8c73e339d80e"

SUMMARY = "1 color-3 base shape + 2-3 single-cell color-1 markers (with adjacent rotation-code cells)."

INVARIANTS = [
    "background is 0",
    "exactly one color-3 connected motif (3-5 cells)",
    "2-3 color-1 markers with an adjacent color cell (rotation code, 2 or 4)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_base", "no_markers", "no_rotation_codes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "base_upper_left_markers_right",
                       "valid": "base_upper_left_markers_right"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_markers", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
        n = ctx.draw_int("n_markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n_markers", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = _build_motif(rng, rng.randint(3, 4))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, max(0, h // 2 - sh - 1))
            c0 = rng.randint(0, max(0, w // 3 - sw))
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = 3
            placed = True; break
        if not placed:
            continue
        ok = True
        for _ in range(n):
            placed_m = False
            for _t in range(80):
                r = rng.randint(2, h - 3); c = rng.randint(w // 3, w - 3)
                if g[r][c] != 0: continue
                if g[r][c + 1] != 0: continue
                g[r][c] = rng.choice([2, 4])
                g[r][c + 1] = 1
                placed_m = True; break
            if not placed_m:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_base":
        # Markers but no color-3 base — rule has nothing to stamp.
        g[5][6] = 2; g[5][7] = 1
        return g
    if name == "no_markers":
        # Base but no color-1 markers — rule has no anchors.
        g[1][1] = 3; g[1][2] = 3; g[2][1] = 3
        return g
    if name == "no_rotation_codes":
        # Markers without adjacent rotation codes — rule has no rotation count.
        g[1][1] = 3; g[1][2] = 3; g[2][1] = 3
        g[5][5] = 1; g[5][8] = 1
        return g
    return g
