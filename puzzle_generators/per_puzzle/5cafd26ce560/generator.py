"""Generator for puzzle 80af3007.

Rule: 5-cells form 3x3 of 3x3 blocks (all-5 or all-0). Rule reads
3x3 meta pattern, renders 9x9 fractal self-tile.

Combinatorial axes (8): grid_h/w, meta_pattern_kind, meta_density,
position_bias, anchor_corner, asymmetry_force, decoy_density,
n_meta_cells.
Degenerates: empty_meta, full_meta, single_meta_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "5cafd26ce560"
VERSION = "1.1.0"
TASK_ID = "5cafd26ce560"
SUMMARY = "5-block 3×3 meta; rule renders 9×9 fractal self-tile."

INVARIANTS = [
    "background is 0",
    "5-cells form a 3×3 of 3×3 all-5 blocks",
    "meta[0][:] has >=1 five (bbox top row aligned)",
    "meta[:][0] has >=1 five (bbox left col aligned)",
    ">=2 meta cells are 5",
]

META_PATTERN_KINDS = ("scattered", "diag", "anti_diag", "frame",
                      "corners", "X_shape", "plus")
POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("empty_meta", "full_meta", "single_meta_cell")
HELPFUL_TEXTURES = META_PATTERN_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 12..20", "valid": "10..24"},
    "grid_w":             {"type": "int", "default": "rng 12..20", "valid": "10..24"},
    "meta_pattern_kind":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(META_PATTERN_KINDS)},
    "meta_density":       {"type": "float", "default": "rng 0.4..0.7",
                           "valid": "0.2..0.9"},
    "position_bias":      {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_BIAS)},
    "n_meta_cells":       {"type": "int", "default": "rng 2..6", "valid": "2..9"},
    "anchor_corner":      {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for meta_pattern_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 12, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pattern_kind = (overrides.get("texture") or
                    overrides.get("meta_pattern_kind")
                    or ctx.draw_choice("meta_pattern_kind",
                                       list(META_PATTERN_KINDS)))
    density = float(overrides.get("meta_density",
                                  ctx.draw_rng("meta_density")
                                  .uniform(0.4, 0.7)))
    meta = _draw_meta(pattern_kind, density, rng)
    if not any(meta[0]) or not any(meta[r][0] for r in range(3)):
        meta[0][0] = 1
    if sum(sum(row) for row in meta) < 2:
        meta[0][0] = 1; meta[1][1] = 1
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         list(POSITION_BIAS)))
    if bias == "center":
        r0 = (h - 9) // 2
        c0 = (w - 9) // 2
    elif bias == "edge":
        r0 = 0; c0 = 0
    else:
        r0 = rng.randint(0, h - 9)
        c0 = rng.randint(0, w - 9)
    g = full_grid(h, w, 0)
    for br in range(3):
        for bc in range(3):
            if meta[br][bc]:
                draw_rect(g, r0 + 3 * br, c0 + 3 * bc, 3, 3, 5)
    return g


def _draw_meta(kind, density, rng):
    meta = [[0] * 3 for _ in range(3)]
    if kind == "diag":
        meta[0][0] = 1; meta[1][1] = 1; meta[2][2] = 1
    elif kind == "anti_diag":
        meta[0][2] = 1; meta[1][1] = 1; meta[2][0] = 1
    elif kind == "frame":
        for r in range(3):
            for c in range(3):
                if r in (0, 2) or c in (0, 2):
                    meta[r][c] = 1
    elif kind == "corners":
        meta[0][0] = 1; meta[0][2] = 1; meta[2][0] = 1; meta[2][2] = 1
    elif kind == "X_shape":
        meta[0][0] = 1; meta[0][2] = 1
        meta[1][1] = 1
        meta[2][0] = 1; meta[2][2] = 1
    elif kind == "plus":
        meta[0][1] = 1; meta[1][0] = 1; meta[1][1] = 1
        meta[1][2] = 1; meta[2][1] = 1
    else:
        for r in range(3):
            for c in range(3):
                meta[r][c] = 1 if rng.random() < density else 0
    return meta


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "empty_meta":
        return g
    if name == "full_meta":
        for br in range(3):
            for bc in range(3):
                draw_rect(g, 1 + 3 * br, 1 + 3 * bc, 3, 3, 5)
        return g
    if name == "single_meta_cell":
        draw_rect(g, 1, 1, 3, 3, 5)
        return g
    return g
