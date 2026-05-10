"""Generator for puzzle 15696249.

Rule: 3x3 grid. Find rows/cols that are uniform. Output 9x9 tiles only
at uniform-row blocks or uniform-col blocks.

Combinatorial axes (8): n_uniform_rows, n_uniform_cols, palette_kind,
palette_size, uniform_position, anchor_corner, asymmetry_force,
include_diagonal.
Degenerates: all_uniform, no_uniform, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2082a4577cff"
VERSION = "1.1.0"
TASK_ID = "2082a4577cff"
SUMMARY = "3x3 grid; rule tiles 9x9 at uniform-row/col blocks only."

INVARIANTS = [
    "grid is 3x3",
    ">=1 uniform row OR >=1 uniform col",
    "non-uniform rows/cols have >=2 distinct values",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
UNIFORM_POSITIONS = ("top_row", "middle_row", "bottom_row",
                     "left_col", "middle_col", "right_col", "rng")
DEGENERATE_TEXTURES = ("all_uniform", "no_uniform", "monochrome")
HELPFUL_TEXTURES = UNIFORM_POSITIONS

AXES = {
    "grid_n":           {"type": "int", "default": "3", "valid": "3"},
    "n_uniform_rows":   {"type": "int", "default": "rng 0..1", "valid": "0..3"},
    "n_uniform_cols":   {"type": "int", "default": "rng 0..1", "valid": "0..3"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "palette_size":     {"type": "int", "default": "3", "valid": "2..6"},
    "uniform_position": {"type": "str", "default": "rng helpful",
                         "valid": "|".join(UNIFORM_POSITIONS)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for uniform_position",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n = 3
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size", 3))
    palette_size = max(2, min(6, palette_size))
    palette = _build_palette(palette_kind, palette_size, rng)
    pos = (overrides.get("texture") or
           overrides.get("uniform_position")
           or ctx.draw_choice("uniform_position",
                              list(UNIFORM_POSITIONS)))
    n_urows = int(overrides.get("n_uniform_rows",
                                ctx.draw_int("n_uniform_rows", 0, 1)))
    n_ucols = int(overrides.get("n_uniform_cols",
                                ctx.draw_int("n_uniform_cols", 0, 1)))
    if n_urows + n_ucols == 0:
        # Force at least one
        if rng.random() < 0.5:
            n_urows = 1
        else:
            n_ucols = 1
    g = [[rng.choice(palette) for _ in range(n)] for _ in range(n)]
    # Apply uniform_position
    if pos in ("top_row", "middle_row", "bottom_row"):
        ur = {"top_row": 0, "middle_row": 1, "bottom_row": 2}[pos]
        c = rng.choice(palette)
        for k in range(n):
            g[ur][k] = c
    elif pos in ("left_col", "middle_col", "right_col"):
        uc = {"left_col": 0, "middle_col": 1, "right_col": 2}[pos]
        c = rng.choice(palette)
        for k in range(n):
            g[k][uc] = c
    else:
        # rng with n_urows + n_ucols
        for _ in range(n_urows):
            ur = rng.randint(0, n - 1)
            c = rng.choice(palette)
            for k in range(n):
                g[ur][k] = c
        for _ in range(n_ucols):
            uc = rng.randint(0, n - 1)
            c = rng.choice(palette)
            for k in range(n):
                g[k][uc] = c
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _draw_from_degenerate(name, rng):
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    if name == "all_uniform":
        c = palette[0]
        return [[c] * 3 for _ in range(3)]
    if name == "no_uniform":
        # 3x3 with no uniform row/col
        return [[palette[0], palette[1], palette[2]],
                [palette[1], palette[2], palette[0]],
                [palette[2], palette[0], palette[1]]]
    if name == "monochrome":
        return [[palette[0]] * 3 for _ in range(3)]
    return [[palette[0]] * 3 for _ in range(3)]
