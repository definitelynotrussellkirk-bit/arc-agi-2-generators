"""Generator for ARC task a9f96cdd.

Rule: for each cell with cell-at(r-1, c-1)=2 → 3; (r-1, c+1)=2 → 6;
(r+1, c-1)=2 → 8; (r+1, c+1)=2 → 7. Else 0.

Combinatorial axes (8): grid_h/w, n_seeds, seed_layout, position_bias,
seed_separation, decoy_density, edge_avoidance, anchor_corner.
Degenerates: no_seeds, single_seed, all_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad52210ad00d"
VERSION = "1.1.0"
TASK_ID = "ad52210ad00d"
SUMMARY = "Sparse 2-seeds; rule paints diagonal neighbors by direction."

INVARIANTS = [
    "background is 0",
    ">=1 color-2 seed cell",
    "seeds in interior so all 4 diagonals exist",
    "no other non-bg colors (rule writes 3/6/7/8)",
]

SEED_LAYOUTS = ("scattered", "diagonal", "anti_diag", "row", "col",
                "corners", "center")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "all_seeds")
HELPFUL_TEXTURES = SEED_LAYOUTS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 5..12", "valid": "4..16"},
    "grid_w":            {"type": "int", "default": "rng 5..14", "valid": "4..18"},
    "n_seeds":           {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "seed_layout":       {"type": "str", "default": "rng helpful",
                          "valid": "|".join(SEED_LAYOUTS)},
    "position_bias":     {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "seed_separation":   {"type": "int", "default": "2", "valid": "1..3"},
    "edge_avoidance":    {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for seed_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 11, 16
    else:
        h_lo, h_hi = 5, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_seeds = int(overrides.get("n_seeds",
                                ctx.draw_int("n_seeds", 2, 4)))
    n_seeds = max(1, min(6, n_seeds))
    layout = (overrides.get("texture") or overrides.get("seed_layout")
              or ctx.draw_choice("seed_layout", list(SEED_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    sep = int(overrides.get("seed_separation", 2))
    edge_avoid = bool(overrides.get("edge_avoidance", True))
    g = full_grid(h, w, 0)
    inset = 1 if edge_avoid else 0
    rmin, rmax = inset, h - 1 - inset
    cmin, cmax = inset, w - 1 - inset
    if rmax < rmin: rmin, rmax = 0, h - 1
    if cmax < cmin: cmin, cmax = 0, w - 1
    cells = _layout_cells(layout, rmin, rmax, cmin, cmax, bias, rng)
    placed = []
    for r, c in cells:
        if all(abs(pr - r) >= sep or abs(pc - c) >= sep
               for pr, pc in placed):
            placed.append((r, c))
            g[r][c] = 2
        if len(placed) >= n_seeds:
            break
    if not placed:
        g[max(1, h // 2)][max(1, w // 2)] = 2
    return g


def _layout_cells(layout, rmin, rmax, cmin, cmax, bias, rng):
    cells = [(r, c) for r in range(rmin, rmax + 1)
             for c in range(cmin, cmax + 1)]
    if layout == "diagonal":
        diag = [(rmin + k, cmin + k)
                for k in range(min(rmax - rmin, cmax - cmin) + 1)]
        rest = [c for c in cells if c not in diag]
        rng.shuffle(rest)
        return diag + rest
    if layout == "anti_diag":
        anti = [(rmin + k, cmax - k)
                for k in range(min(rmax - rmin, cmax - cmin) + 1)]
        rest = [c for c in cells if c not in anti]
        rng.shuffle(rest)
        return anti + rest
    if layout == "row":
        r = (rmin + rmax) // 2
        chosen = [(r, c) for c in range(cmin, cmax + 1)]
        rest = [cc for cc in cells if cc not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "col":
        c = (cmin + cmax) // 2
        chosen = [(r, c) for r in range(rmin, rmax + 1)]
        rest = [cc for cc in cells if cc not in chosen]
        rng.shuffle(rest)
        return chosen + rest
    if layout == "corners":
        corners = [(rmin, cmin), (rmin, cmax),
                   (rmax, cmin), (rmax, cmax)]
        rest = [c for c in cells if c not in corners]
        rng.shuffle(rest)
        return corners + rest
    if layout == "center":
        cr = (rmin + rmax) // 2
        cc = (cmin + cmax) // 2
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if bias == "center":
        cr = (rmin + rmax) // 2
        cc = (cmin + cmax) // 2
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells
    if bias == "edge":
        cells.sort(key=lambda rc: -min(rc[0] - rmin, rmax - rc[0],
                                       rc[1] - cmin, cmax - rc[1]))
        return cells
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[h // 2][w // 2] = 2
        return g
    if name == "all_seeds":
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 2
        return g
    return g
