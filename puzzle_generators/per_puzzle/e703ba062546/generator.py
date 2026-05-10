"""Generator for arc_additional_puzzles_21_set18_bundle:H122 — canonical packing by perimeter.

Rule: each non-bg connected component is cropped to its bbox; sort components
by (4-neighbor perimeter desc, size desc, then row/col tiebreak), and pack
crops left-to-right with one blank column gap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components (no shapes → output is empty);
single_component (only 1 → trivial pack, no contrast); equal_perimeters
(all 3 components share same perimeter → primary sort key collapses).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e703ba062546"
VERSION = "1.1.0"
TASK_ID = "e703ba062546"

SUMMARY = "3 isolated multicolor components with varied perimeters."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated 4-connected non-bg components",
    "each component is multicolor (3-6 cells, 1-3 colors)",
    "components have differing perimeters/sizes (so output is non-trivially ordered)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_component", "equal_perimeters")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":            {"type": "int", "default": "rng 14..16", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..6", "valid": "2..6"},
    "position_bias":     {"type": "str", "default": "three_components_distinct_sizes",
                          "valid": "three_components_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "2..6"},
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
    cells = [(0, 0)]
    seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sr0, sc0 = -min(rs), -min(cs)
    sh = max(rs) - min(rs) + 1
    sw = max(cs) - min(cs) + 1
    grid = [[0] * sw for _ in range(sh)]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(3, k))
    for i, (r, c) in enumerate(cells):
        grid[sr0 + r][sc0 + c] = palette[i % len(palette)]
    return grid, sh, sw


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        sizes = [3, 5, 7]
        rng.shuffle(sizes)
        for k in sizes:
            motif, sh, sw = _build_motif(rng, k)
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1):
                    continue
                for r in range(sh):
                    for c in range(sw):
                        if motif[r][c] != 0:
                            g[r0 + r][c0 + c] = motif[r][c]
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place 3 isolated motifs in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 11, 15
    g = full_grid(h, w, 0)
    if name == "no_components":
        return g
    if name == "single_component":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][6 + dc] = 4
        return g
    if name == "equal_perimeters":
        # Three identical 2x2 squares — same perimeter (8) and size (4).
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(2):
                g[1 + r][7 + c] = 2
        for r in range(2):
            for c in range(2):
                g[7 + r][4 + c] = 3
        return g
    return g
