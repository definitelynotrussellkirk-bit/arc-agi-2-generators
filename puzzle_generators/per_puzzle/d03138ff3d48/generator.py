"""Generator for 6f473927.

Rule: if col 0 has any non-zero, output places 8s at mirror of zeros
on LEFT and original on right. Else mirror on right.

Combinatorial axes (8): grid_h/w, col0_has_nonzero, palette_size,
fg_density, fg_layout, palette_kind, decoy_density, anchor_corner.
Degenerates: empty_grid, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d03138ff3d48"
VERSION = "1.1.0"
TASK_ID = "d03138ff3d48"
SUMMARY = "h×w grid; rule outputs 2w with 8-mask of zeros + mirror."

INVARIANTS = [
    "h, w in [3, 6]",
    ">=2 non-bg cells (so output is non-trivial)",
    ">=1 bg cell (so 8-mask is visible)",
    "no color 8 in input (rule writes 8 for output)",
]

FG_LAYOUTS = ("scattered", "blob", "diag", "row", "col",
              "checker", "frame")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "single_cell")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "grid_w":          {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "col0_has_nonzero": {"type": "bool", "default": "rng true|false",
                         "valid": "true|false"},
    "palette_size":    {"type": "int", "default": "rng 1..3", "valid": "1..7"},
    "fg_density":      {"type": "float", "default": "rng 0.3..0.6",
                        "valid": "0.1..1"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "texture":         {"type": "str", "default": "alias for fg_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 5, 7
    else:
        h_lo, h_hi = 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 1, 3)))
    palette = pool[:max(1, n_palette)]
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density")
                                  .uniform(0.3, 0.6)))
    col0_nonzero = bool(overrides.get("col0_has_nonzero",
                                      rng.random() < 0.5))
    g = full_grid(h, w, 0)
    _fill(g, layout, h, w, palette, density, rng)
    if col0_nonzero:
        if all(g[r][0] == 0 for r in range(h)):
            g[h // 2][0] = palette[0]
    else:
        for r in range(h):
            g[r][0] = 0
    has_fg = any(g[r][c] != 0 for r in range(h) for c in range(w))
    has_bg = any(g[r][c] == 0 for r in range(h) for c in range(w))
    if not has_fg:
        g[1][1] = palette[0]
    if not has_bg:
        g[0][0] = 0
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = palette[0]
    return g


def _fill(g, layout, h, w, palette, density, rng):
    if layout == "blob":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        for r in range(h):
            for c in range(w):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density + 0.2:
                    g[r][c] = rng.choice(palette)
        return
    if layout == "diag":
        for k in range(min(h, w)):
            g[k][k] = rng.choice(palette)
        return
    if layout == "row":
        r = rng.randint(0, h - 1)
        for c in range(w):
            g[r][c] = rng.choice(palette)
        return
    if layout == "col":
        c = rng.randint(0, w - 1)
        for r in range(h):
            g[r][c] = rng.choice(palette)
        return
    if layout == "checker":
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0:
                    g[r][c] = rng.choice(palette)
        return
    if layout == "frame":
        for r in range(h):
            for c in range(w):
                if r in (0, h - 1) or c in (0, w - 1):
                    g[r][c] = rng.choice(palette)
        return
    for r in range(h):
        for c in range(w):
            if rng.random() < density:
                g[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 9])
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
