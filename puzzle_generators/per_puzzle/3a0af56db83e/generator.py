"""Generator for 3d31c5b3.

Rule: 12-row grid as 4 stacked 3-row bands. Output is one 3-row band
where each cell takes the first non-0 value across band priorities
0 > 1 > 3 > 2.

Combinatorial axes (8): grid_w, band_density, band_layout,
band_color_distinct, overlap_kind, decoy_density, position_bias,
sparsity_kind.
Degenerates: single_band_only, all_zero_bands, full_band_first.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3a0af56db83e"
VERSION = "1.1.0"
TASK_ID = "3a0af56db83e"
SUMMARY = "12×W grid as 4 stacked 3-row bands of distinct colors; rule overlays them."

INVARIANTS = [
    "h = 12 (exactly 4 bands of 3 rows)",
    "each band has >=1 non-zero cell",
    "the 4 bands use 4 distinct non-zero colors (so output traces back uniquely)",
    "each cell of priority-0 band may be 0 OR non-0 (so lower bands matter sometimes)",
]

BAND_LAYOUTS = ("uniform", "sparse", "dense", "stripe", "diag", "checker")
DEGENERATE_TEXTURES = ("single_band_only", "all_zero_bands", "full_band_first")
HELPFUL_TEXTURES = BAND_LAYOUTS

AXES = {
    "grid_w":             {"type": "int", "default": "rng 5..10", "valid": "4..12"},
    "band_density":       {"type": "float", "default": "rng 0.3..0.7",
                           "valid": "0..1"},
    "band_layout":        {"type": "str", "default": "rng helpful",
                           "valid": "|".join(BAND_LAYOUTS)},
    "overlap_kind":       {"type": "str", "default": "rng disjoint|partial|full",
                           "valid": "disjoint|partial|full"},
    "position_bias":      {"type": "str", "default": "rng spread|left|right",
                           "valid": "spread|left|right"},
    "min_band_cells":     {"type": "int", "default": "2", "valid": "1..6"},
    "color_distinct":     {"type": "bool", "default": "true", "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for band_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi = 4, 6
    elif difficulty == "hard":
        w_lo, w_hi = 9, 12
    else:
        w_lo, w_hi = 5, 10
    h = 12
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    layout = (overrides.get("texture") or overrides.get("band_layout")
              or ctx.draw_choice("band_layout", list(BAND_LAYOUTS)))
    density = float(overrides.get("band_density",
                                  ctx.draw_rng("band_density")
                                  .uniform(0.3, 0.7)))
    overlap = overrides.get("overlap_kind",
                            ctx.draw_choice("overlap_kind",
                                            ["disjoint", "partial", "full"]))
    min_cells = int(overrides.get("min_band_cells", 2))
    band_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g = full_grid(h, w, 0)
    band_cells_assigned = []
    for j in range(4):
        cells = _layout_band(layout, j, w, density, rng)
        if overlap == "disjoint":
            forbidden = set()
            for prev in band_cells_assigned:
                forbidden.update(prev)
            cells = [(r, c) for (r, c) in cells if (r, c) not in forbidden]
        elif overlap == "full" and band_cells_assigned:
            shared = list(band_cells_assigned[0])
            cells = list(set(cells) | set(shared))
        if len(cells) < min_cells:
            extra_pool = [(r, c) for r in range(j * 3, j * 3 + 3)
                          for c in range(w) if (r, c) not in cells]
            rng.shuffle(extra_pool)
            for cell in extra_pool[:min_cells - len(cells)]:
                cells.append(cell)
        for r, c in cells:
            g[r][c] = band_colors[j]
        band_cells_assigned.append(cells)
    return g


def _layout_band(layout, j, w, density, rng):
    base_r = j * 3
    cells = []
    if layout == "stripe":
        target_r = base_r + (j % 3)
        for c in range(w):
            cells.append((target_r, c))
    elif layout == "diag":
        for k in range(min(3, w)):
            cells.append((base_r + k, k))
    elif layout == "checker":
        for r in range(base_r, base_r + 3):
            for c in range(w):
                if (r + c) % 2 == j % 2:
                    cells.append((r, c))
    elif layout == "dense":
        for r in range(base_r, base_r + 3):
            for c in range(w):
                if rng.random() < min(0.85, density + 0.2):
                    cells.append((r, c))
    elif layout == "sparse":
        for r in range(base_r, base_r + 3):
            for c in range(w):
                if rng.random() < max(0.15, density - 0.2):
                    cells.append((r, c))
    else:  # uniform
        for r in range(base_r, base_r + 3):
            for c in range(w):
                if rng.random() < density:
                    cells.append((r, c))
    return cells


def _draw_from_degenerate(name, w, rng):
    h = 12
    g = full_grid(h, w, 0)
    band_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    if name == "single_band_only":
        for c in range(w):
            g[0][c] = band_colors[0]
        return g
    if name == "all_zero_bands":
        # Need ≥1 cell per band per invariant; use sparse pattern
        for j in range(4):
            g[j * 3][0] = band_colors[j]
        return g
    if name == "full_band_first":
        # First band fully fills — others irrelevant
        for r in range(0, 3):
            for c in range(w):
                g[r][c] = band_colors[0]
        for j in range(1, 4):
            g[j * 3][0] = band_colors[j]
        return g
    return g
