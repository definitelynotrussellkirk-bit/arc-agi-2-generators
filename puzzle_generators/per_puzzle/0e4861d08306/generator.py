"""Generator for 36f9e4ca.

Rule: BFS from 2-seed through cells with v ∈ {1, 2}. Recolor reached
1-cells to 3.

Combinatorial axes (8): grid_h/w, region_size, region_shape,
seed_position, n_disconnected, decoy_density, position_bias,
disconnect_distance.
Degenerates: no_seed, all_connected, no_region.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0e4861d08306"
VERSION = "1.1.0"
TASK_ID = "0e4861d08306"
SUMMARY = "Connected blob of 1s + 2-seed inside + isolated 1-cells; rule recolors reached 1s to 3."

INVARIANTS = [
    "background is 0",
    ">=4 1-cells in a 4-connected blob",
    "exactly one 2-seed (within or adjacent to the 1-blob)",
    ">=1 disconnected 1-cell elsewhere (won't be reached)",
    "the disconnected 1-cell is NOT 4-adjacent to the 1-blob",
    "no color 3 in input (rule writes 3 for output)",
]

REGION_SHAPES = ("blob", "L_shape", "T_shape", "horizontal_strip",
                 "vertical_strip", "cross")
DEGENERATE_TEXTURES = ("no_seed", "all_connected", "no_region")
HELPFUL_TEXTURES = REGION_SHAPES

AXES = {
    "grid_h":           {"type": "int", "default": "rng 7..12", "valid": "6..16"},
    "grid_w":           {"type": "int", "default": "rng 9..16", "valid": "7..20"},
    "region_size":      {"type": "int", "default": "rng 5..12",
                         "valid": "3..18"},
    "region_shape":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(REGION_SHAPES)},
    "seed_position":    {"type": "str", "default": "rng inside|edge",
                         "valid": "inside|edge"},
    "n_disconnected":   {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "position_bias":    {"type": "str", "default": "rng spread|center|edge",
                         "valid": "spread|center|edge"},
    "disconnect_distance": {"type": "int", "default": "2", "valid": "1..4"},
    "texture":          {"type": "str", "default": "alias for region_shape",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, sz_lo, sz_hi = 6, 8, 4, 6
    elif difficulty == "hard":
        h_lo, h_hi, sz_lo, sz_hi = 11, 16, 10, 18
    else:
        h_lo, h_hi, sz_lo, sz_hi = 7, 12, 5, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    region_size = int(overrides.get("region_size",
                                    ctx.draw_int("region_size", sz_lo, sz_hi)))
    shape = (overrides.get("texture") or overrides.get("region_shape")
             or ctx.draw_choice("region_shape", list(REGION_SHAPES)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    n_disc = int(overrides.get("n_disconnected",
                               ctx.draw_int("n_disconnected", 1, 3)))
    disc_dist = int(overrides.get("disconnect_distance", 2))
    g = full_grid(h, w, 0)
    cells = _build_region(shape, region_size, h, w, bias, rng)
    for r, c in cells:
        g[r][c] = 1
    if cells:
        seed_cell = rng.choice(list(cells))
        g[seed_cell[0]][seed_cell[1]] = 2
    placed = 0
    tries = 0
    while placed < n_disc and tries < 60:
        tries += 1
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0:
            continue
        ok = True
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            for d in range(1, disc_dist + 1):
                nr, nc = r + dr * d, c + dc * d
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] in (1, 2):
                    ok = False; break
            if not ok: break
        if ok:
            g[r][c] = 1
            placed += 1
    if placed < 1:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    ok = True
                    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] in (1, 2):
                            ok = False; break
                    if ok:
                        g[r][c] = 1
                        placed += 1; break
            if placed >= 1: break
    return g


def _build_region(shape, target_size, h, w, bias, rng):
    if bias == "center":
        sr, sc = h // 2, w // 2
    elif bias == "edge":
        sr = rng.choice([1, h - 2])
        sc = rng.choice([1, w - 2])
    else:
        sr = rng.randint(1, h - 2)
        sc = rng.randint(1, w // 2)
    if shape == "horizontal_strip":
        return {(sr, c) for c in range(max(0, sc - 1),
                                       min(w, sc + target_size - 1))}
    if shape == "vertical_strip":
        return {(r, sc) for r in range(max(0, sr - 1),
                                       min(h, sr + target_size - 1))}
    if shape == "L_shape":
        cells = set()
        half = target_size // 2
        for c in range(sc, min(w, sc + half + 1)):
            cells.add((sr, c))
        for r in range(sr + 1, min(h, sr + half + 1)):
            cells.add((r, sc))
        return cells
    if shape == "T_shape":
        cells = set()
        half = max(2, target_size // 3)
        for c in range(max(0, sc - half), min(w, sc + half + 1)):
            cells.add((sr, c))
        for r in range(sr + 1, min(h, sr + half + 1)):
            cells.add((r, sc))
        return cells
    if shape == "cross":
        cells = set()
        half = max(2, target_size // 4)
        for k in range(-half, half + 1):
            if 0 <= sr + k < h:
                cells.add((sr + k, sc))
            if 0 <= sc + k < w:
                cells.add((sr, sc + k))
        return cells
    cells = {(sr, sc)}
    frontier = [(sr, sc)]
    while frontier and len(cells) < target_size:
        r, c = frontier.pop(rng.randint(0, len(frontier) - 1))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                continue
            if (nr, nc) in cells:
                continue
            cells.add((nr, nc))
            frontier.append((nr, nc))
            if len(cells) >= target_size:
                break
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_seed":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 1
        return g
    if name == "all_connected":
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 1
        g[3][3] = 2
        return g
    if name == "no_region":
        g[h // 2][w // 2] = 2
        return g
    return g
