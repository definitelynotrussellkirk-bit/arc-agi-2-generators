"""Generator for da2b0fe3.

Rule: mode-color shape (excl. 0). Crop bbox. If lr-symmetric and
(not ud-symmetric or odd height), draw horizontal middle row of 3s.
Else draw vertical middle col of 3s.

Combinatorial axes (8): grid_size, color, shape_size_kind,
position_bias, fill_density, palette_kind, asymmetry_force,
anchor_corners.
Degenerates: empty_grid, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f99497dd2d28"
VERSION = "1.1.0"
TASK_ID = "f99497dd2d28"
SUMMARY = "Mode-colored shape; rule draws 3-line based on shape symmetry."

INVARIANTS = [
    "h = w = 10",
    "exactly one non-zero color (mode color)",
    "shape has >=5 cells",
    "no 3-cells in input (rule writes 3 for output)",
]

SHAPE_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "single_cell")
HELPFUL_TEXTURES = SHAPE_SIZE_KINDS

AXES = {
    "grid_size":         {"type": "int", "default": "10", "valid": "10"},
    "color":             {"type": "color", "default": "rng (≠0,3)",
                          "valid": "1..9 (≠3)"},
    "shape_size_kind":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(SHAPE_SIZE_KINDS)},
    "position_bias":     {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "fill_density":      {"type": "float", "default": "rng 0.5..0.9",
                          "valid": "0.3..1"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "anchor_corners":    {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for shape_size_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = w = 10
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2]
    else:
        pool = [1, 2, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    color = int(overrides.get("color", pool[0]))
    if color == 3 or color == 0:
        color = pool[0]
    size_kind = (overrides.get("texture") or
                 overrides.get("shape_size_kind")
                 or ctx.draw_choice("shape_size_kind",
                                    list(SHAPE_SIZE_KINDS)))
    ph, pw = _shape_dims(size_kind, rng)
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    if bias == "center":
        pr = max(0, (h - ph) // 2)
        pc = max(0, (w - pw) // 2)
    elif bias == "edge":
        pr = 0; pc = 0
    else:
        pr = rng.randint(0, h - ph)
        pc = rng.randint(0, w - pw)
    density = float(overrides.get("fill_density",
                                  ctx.draw_rng("fill_density")
                                  .uniform(0.5, 0.9)))
    g = full_grid(h, w, 0)
    cells_pool = [(r, c) for r in range(pr, pr + ph)
                  for c in range(pc, pc + pw)]
    if bool(overrides.get("anchor_corners", True)):
        g[pr][pc] = color
        g[pr][pc + pw - 1] = color
        g[pr + ph - 1][pc] = color
        g[pr + ph - 1][pc + pw - 1] = color
    n = max(5, int(len(cells_pool) * density))
    chosen = rng.sample(cells_pool, min(n, len(cells_pool)))
    for r, c in chosen:
        g[r][c] = color
    return g


def _shape_dims(kind, rng):
    if kind == "small":
        return 3, 3
    if kind == "medium":
        return rng.randint(3, 5), rng.randint(3, 5)
    if kind == "large":
        return rng.randint(5, 7), rng.randint(5, 7)
    if kind == "wide":
        return rng.randint(3, 4), rng.randint(5, 7)
    if kind == "tall":
        return rng.randint(5, 7), rng.randint(3, 4)
    return rng.randint(3, 6), rng.randint(3, 6)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 4, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_cell":
        g[h // 2][w // 2] = color
        return g
    return g
