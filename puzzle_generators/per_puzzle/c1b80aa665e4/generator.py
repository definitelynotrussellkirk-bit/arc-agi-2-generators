"""Generator for v1_e_m_h_keys:E5 — mark isolated cells with color 9.

Rule: each non-zero cell with no non-zero neighbors (4-cardinal) is recolored
to color 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_iso, n_clus,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_iso, no_clusters, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c1b80aa665e4"
VERSION = "1.1.0"
TASK_ID = "c1b80aa665e4"

SUMMARY = "Mix of isolated cells and small clusters in distinct colors."

INVARIANTS = [
    "background is 0",
    "1-3 isolated single cells (no neighbors) in distinct non-{0, 9} colors",
    "0-2 small connected clusters (2+ cells) in distinct non-{0, 9} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_iso", "no_clusters", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_iso":          {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_clus":         {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "iso_plus_clusters",
                       "valid": "iso_plus_clusters"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n_iso = ctx.draw_int("n_iso", 1, 2)
        n_clus = ctx.draw_int("n_clus", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
        n_iso = ctx.draw_int("n_iso", 2, 4)
        n_clus = ctx.draw_int("n_clus", 1, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
        n_iso = ctx.draw_int("n_iso", 1, 3)
        n_clus = ctx.draw_int("n_clus", 0, 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    used_colors = set()
    iso_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], min(n_iso, 8))
    for color in iso_colors:
        for _t in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            if not _free(g, r, c, r, c): continue
            g[r][c] = color
            used_colors.add(color)
            break
    for _ in range(n_clus):
        for _t in range(40):
            avail = [c for c in [1, 2, 3, 4, 5, 6, 7, 8] if c not in used_colors]
            if not avail: break
            color = rng.choice(avail)
            cells = _build_motif(rng, rng.randint(2, 3))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            for _t2 in range(40):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                used_colors.add(color)
                break
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_iso":
        # Only clusters, no isolated cells — rule recolors nothing to 9.
        g[1][1] = 4; g[1][2] = 4
        g[3][4] = 5; g[3][5] = 5
        return g
    if name == "no_clusters":
        # Only isolated cells — rule recolors all of them to 9.
        g[1][1] = 4; g[3][4] = 5; g[5][2] = 6
        return g
    if name == "all_isolated":
        # All cells are isolated — every non-bg cell becomes 9.
        g[0][0] = 4; g[0][6] = 5; g[3][3] = 6; g[5][1] = 7
        return g
    return g
