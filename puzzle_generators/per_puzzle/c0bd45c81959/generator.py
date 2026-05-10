"""Generator for puzzle af24b4cc.

Rule: 2x3 cell-grid where each cell is 3rows x 2cols. Output is 4x5
with 0-border and mode color of each cell.

Combinatorial axes (8): n_distract_min, n_distract_max, palette_kind,
palette_size, mode_distribution, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: tied_modes, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c0bd45c81959"
VERSION = "1.1.0"
TASK_ID = "c0bd45c81959"
SUMMARY = "9x10 grid w/ 6 cells of 3x2; rule outputs mode of each cell."

INVARIANTS = [
    "h=9, w=10",
    "rows 0, 4, 8 are all 0",
    "cols 0, 3, 6, 9 are all 0",
    "each 3x2 cell has unique majority non-zero color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary", "rng")
DEGENERATE_TEXTURES = ("tied_modes", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_distract_min": {"type": "int", "default": "1", "valid": "0..2"},
    "n_distract_max": {"type": "int", "default": "2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "border_color":   {"type": "color", "default": "0", "valid": "0"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    h = 9; w = 10
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 6, rng)
    n_min = int(overrides.get("n_distract_min", 1))
    n_max = int(overrides.get("n_distract_max", 2))
    n_min = max(0, min(2, n_min))
    n_max = max(n_min, min(3, n_max))
    g = full_grid(h, w, 0)
    cell_idx = 0
    for br in range(2):
        for bc in range(3):
            r1 = 1 + br * 4
            c1 = 1 + bc * 3
            mode_color = palette[cell_idx]
            distract = [v for v in palette if v != mode_color]
            cell_idx += 1
            n_d = rng.randint(n_min, n_max)
            for r in range(r1, r1 + 3):
                for c in range(c1, c1 + 2):
                    g[r][c] = mode_color
            cells = [(r, c) for r in range(r1, r1 + 3)
                     for c in range(c1, c1 + 2)]
            rng.shuffle(cells)
            for (r, c) in cells[:n_d]:
                g[r][c] = rng.choice(distract)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h = 9; w = 10
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 6)
    if name == "tied_modes":
        # Each cell has tied mode → ambiguous
        for br in range(2):
            for bc in range(3):
                r1 = 1 + br * 4
                c1 = 1 + bc * 3
                g[r1][c1] = palette[0]; g[r1][c1 + 1] = palette[1]
                g[r1 + 1][c1] = palette[1]; g[r1 + 1][c1 + 1] = palette[0]
                g[r1 + 2][c1] = palette[0]; g[r1 + 2][c1 + 1] = palette[1]
        return g
    if name == "single_color":
        c = palette[0]
        for r in range(1, 8):
            if r in (4,):
                continue
            for cc in range(1, 9):
                if cc in (3, 6):
                    continue
                g[r][cc] = c
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0]
        return g
    return g
