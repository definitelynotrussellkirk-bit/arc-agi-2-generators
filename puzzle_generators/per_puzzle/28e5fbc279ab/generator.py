"""Generator for v2_meta_puzzles:H1 — stamp color-3 reference at single-cell markers.

Rule: a connected color-3 reference shape + 1-3 single-cell markers in other
colors. Output stamps the reference shape (relative offsets) at each marker
in the marker's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_reference (no color-3 shape → rule's reference selector
finds nothing, no offsets to stamp), no_markers (reference present
but no single-cell markers → rule has no positions to stamp at;
output equals input), reference_at_marker (a marker lands inside the
reference's bbox — rule's stamping overlaps reference, output shows
no clear separation).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28e5fbc279ab"
VERSION = "1.1.0"
TASK_ID = "28e5fbc279ab"

SUMMARY = "1 color-3 reference motif + 1-3 single-cell markers in distinct non-{0, 3} colors."

INVARIANTS = [
    "background is 0",
    "exactly one connected color-3 motif (3-5 cells)",
    "1-3 single-cell markers in distinct non-{0, 3} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_reference", "no_markers", "reference_at_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "n_markers":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "reference_plus_markers",
                          "valid": "reference_plus_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
        n = ctx.draw_int("n_markers", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 12, 12)
        n = ctx.draw_int("n_markers", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n = ctx.draw_int("n_markers", 1, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, max(0, h // 2 - sh - 1))
            c0 = rng.randint(0, max(0, w // 2 - sw))
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = 3
            placed = True; break
        if not placed:
            continue
        marker_colors = rng.sample([1, 2, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in marker_colors:
            placed_m = False
            for _ in range(80):
                r = rng.randint(h // 2, h - sh - 1) if h - sh - 1 > h // 2 else h // 2
                c = rng.randint(w // 2, w - sw)
                if r >= h or c >= w: continue
                if g[r][c] != 0: continue
                if any(g[r + dr][c + dc] != 0 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                       if 0 <= r + dr < h and 0 <= c + dc < w):
                    continue
                g[r][c] = color
                placed_m = True; break
            if not placed_m:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize H1 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_reference":
        # No color-3 shape — rule's reference selector finds nothing.
        g[3][3] = 4
        g[6][7] = 6
        return g
    if name == "no_markers":
        # Reference present but no markers — rule has no positions
        # to stamp; output equals input.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 3
        return g
    if name == "reference_at_marker":
        # Marker lands inside reference's bbox — stamping overlaps;
        # output shows no clear separation.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[2 + dr][2 + dc] = 3
        g[3][3] = 4   # marker inside reference bbox
        return g
    return g
