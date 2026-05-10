"""Generator for puzzle d47aa2ff.

Rule: vertical 5-column splits grid into halves. Output: left-only → 2,
right-only → 1, else left value.

Combinatorial axes (8): grid_h, half_w, fg_color, fg_density,
shared_fraction, side_layout, asymmetry_force, palette_size.
Degenerates: identical_halves, empty_halves, full_halves.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "625b40fb6218"
VERSION = "1.1.0"
TASK_ID = "625b40fb6218"
SUMMARY = "Halves separated by 5-column; rule highlights left-only/right-only differences."

INVARIANTS = [
    "background is 0",
    "exactly one column is fully gray(5) (the separator)",
    "both halves are width >= 2",
    "halves are NOT identical (so the rule's branches both fire)",
    ">=1 left-only cell AND >=1 right-only cell",
]

SIDE_LAYOUTS = ("scattered", "blob", "diag", "stripes", "frame", "checker")
DEGENERATE_TEXTURES = ("identical_halves", "empty_halves", "full_halves")
HELPFUL_TEXTURES = SIDE_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "half_w":          {"type": "int", "default": "rng 4..8",  "valid": "3..12"},
    "fg_color":        {"type": "color", "default": "rng (≠0,1,2,5)",
                        "valid": "1..9 (≠1,2,5)"},
    "fg_density":      {"type": "float", "default": "rng 0.3..0.5",
                        "valid": "0.15..0.7"},
    "shared_fraction": {"type": "float", "default": "rng 0.3..0.6",
                        "valid": "0..1"},
    "side_layout":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(SIDE_LAYOUTS)},
    "palette_size":    {"type": "int", "default": "1", "valid": "1..3"},
    "min_diffs":       {"type": "int", "default": "2", "valid": "1..5"},
    "texture":         {"type": "str", "default": "alias for side_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, hw_lo, hw_hi = 5, 7, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, hw_lo, hw_hi = 11, 16, 7, 12
    else:
        h_lo, h_hi, hw_lo, hw_hi = 6, 12, 4, 8
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    half_w = ctx.draw_int("half_w", hw_lo, hw_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, half_w, rng)
    fg_color = int(overrides.get("fg_color",
                                 ctx.draw_color("fg_color",
                                                exclude={0, 1, 2, 5})))
    n_palette = int(overrides.get("palette_size", 1))
    pool = [c for c in range(1, 10) if c not in (0, 1, 2, 5, fg_color)]
    rng.shuffle(pool)
    palette = [fg_color] + pool[:max(0, n_palette - 1)]
    layout = (overrides.get("texture") or overrides.get("side_layout")
              or ctx.draw_choice("side_layout", list(SIDE_LAYOUTS)))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density")
                                  .uniform(0.3, 0.5)))
    shared = float(overrides.get("shared_fraction",
                                 ctx.draw_rng("shared_fraction")
                                 .uniform(0.3, 0.6)))
    w = 2 * half_w + 1
    sep = half_w
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][sep] = 5
    left_grid = [[0] * half_w for _ in range(h)]
    right_grid = [[0] * half_w for _ in range(h)]
    _fill_side(left_grid, layout, h, half_w, palette, density, rng)
    _fill_side(right_grid, layout, h, half_w, palette, density, rng)
    for r in range(h):
        for c in range(half_w):
            if rng.random() < shared:
                if left_grid[r][c] != 0:
                    right_grid[r][c] = left_grid[r][c]
                elif right_grid[r][c] != 0:
                    left_grid[r][c] = right_grid[r][c]
    diff_count = 0
    for r in range(h):
        for c in range(half_w):
            if (left_grid[r][c] != 0) ^ (right_grid[r][c] != 0):
                diff_count += 1
    if diff_count < 2:
        left_grid[0][0] = palette[0]; right_grid[0][0] = 0
        right_grid[h - 1][half_w - 1] = palette[0]; left_grid[h - 1][half_w - 1] = 0
    for r in range(h):
        for c in range(half_w):
            g[r][c] = left_grid[r][c]
            g[r][sep + 1 + c] = right_grid[r][c]
    return g


def _fill_side(side, layout, h, hw, palette, density, rng):
    if layout == "blob":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, hw - 1)
        for r in range(h):
            for c in range(hw):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density:
                    side[r][c] = rng.choice(palette)
        return
    if layout == "diag":
        for k in range(min(h, hw)):
            side[k][k] = rng.choice(palette)
        return
    if layout == "stripes":
        for r in range(h):
            color = rng.choice(palette)
            for c in range(hw):
                if r % 2 == 0:
                    side[r][c] = color
        return
    if layout == "frame":
        for r in range(h):
            for c in range(hw):
                if r in (0, h - 1) or c in (0, hw - 1):
                    side[r][c] = rng.choice(palette)
        return
    if layout == "checker":
        for r in range(h):
            for c in range(hw):
                if (r + c) % 2 == 0:
                    side[r][c] = rng.choice(palette)
        return
    for r in range(h):
        for c in range(hw):
            if rng.random() < density:
                side[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, h, half_w, rng):
    w = 2 * half_w + 1
    sep = half_w
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][sep] = 5
    fg = rng.choice([3, 4, 6, 7, 8, 9])
    if name == "identical_halves":
        for r in range(h):
            for c in range(half_w):
                if rng.random() < 0.4:
                    g[r][c] = fg
                    g[r][sep + 1 + c] = fg
        return g
    if name == "empty_halves":
        return g
    if name == "full_halves":
        for r in range(h):
            for c in range(half_w):
                g[r][c] = fg
                g[r][sep + 1 + c] = fg
        return g
    return g
