"""Generator for e3497940.

Rule: full-height col of 5s separates left and right halves. Output is
sep × sep wide. For each (r, c) take right side (mirrored), else left.

Combinatorial axes (8): grid_h, sep_position, palette_size, fg_density,
side_layout, asymmetry_force, decoy_density, fg_balance.
Degenerates: empty_sides, full_sides, no_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7e5824fc1ef"
VERSION = "1.1.0"
TASK_ID = "b7e5824fc1ef"
SUMMARY = "Full-height 5-divider; rule mirror-merges right onto left."

INVARIANTS = [
    "exactly 1 full-height column of 5s",
    "left and right sides have content (so merge is non-trivial)",
    "left half-width = right half-width = sep",
    "no extra 5s outside the divider column",
]

SIDE_LAYOUTS = ("noise", "blob", "frame", "diag", "stripes", "scattered")
DEGENERATE_TEXTURES = ("empty_sides", "full_sides", "no_divider")
HELPFUL_TEXTURES = SIDE_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "sep_position":    {"type": "int", "default": "= w/2", "valid": "2..(w-3)"},
    "palette_size":    {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "fg_density":      {"type": "float", "default": "rng 0.3..0.5",
                        "valid": "0.1..0.7"},
    "side_layout":     {"type": "str", "default": "rng helpful",
                        "valid": "|".join(SIDE_LAYOUTS)},
    "asymmetry_force": {"type": "bool", "default": "true", "valid": "true|false"},
    "fg_balance":      {"type": "str", "default": "rng even|left_heavy|right_heavy",
                        "valid": "even|left_heavy|right_heavy"},
    "side_width":      {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "texture":         {"type": "str", "default": "alias for side_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, sw_lo, sw_hi = 5, 7, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, sw_lo, sw_hi = 11, 16, 6, 8
    else:
        h_lo, h_hi, sw_lo, sw_hi = 7, 12, 4, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)
    sw = int(overrides.get("side_width",
                           ctx.draw_int("side_width", sw_lo, sw_hi)))
    sep = sw
    w = 2 * sw + 1
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 4)))
    pool = [c for c in range(1, 10) if c != 5]
    rng.shuffle(pool)
    palette = pool[:max(1, n_palette)]
    layout = (overrides.get("texture") or overrides.get("side_layout")
              or ctx.draw_choice("side_layout", list(SIDE_LAYOUTS)))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density")
                                  .uniform(0.3, 0.5)))
    balance = overrides.get("fg_balance",
                            ctx.draw_choice("fg_balance",
                                            ["even", "left_heavy", "right_heavy"]))
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][sep] = 5
    left_density = density
    right_density = density
    if balance == "left_heavy":
        right_density *= 0.5
    elif balance == "right_heavy":
        left_density *= 0.5
    _fill_side(g, layout, h, 0, sep, palette, left_density, rng)
    _fill_side(g, layout, h, sep + 1, w, palette, right_density, rng)
    has_left = any(g[r][c] != 0 for r in range(h) for c in range(sep))
    has_right = any(g[r][c] != 0 for r in range(h) for c in range(sep + 1, w))
    if not has_left:
        g[0][0] = palette[0]
    if not has_right:
        g[0][sep + 1] = palette[0]
    return g


def _fill_side(g, layout, h, c_start, c_end, palette, density, rng):
    if layout == "blob":
        cr = rng.randint(0, h - 1)
        cc = rng.randint(c_start, c_end - 1)
        for r in range(h):
            for c in range(c_start, c_end):
                if abs(r - cr) + abs(c - cc) <= 2 and rng.random() < density:
                    g[r][c] = rng.choice(palette)
        return
    if layout == "frame":
        for r in range(h):
            for c in range(c_start, c_end):
                if (r in (0, h - 1) or c == c_start or c == c_end - 1) \
                        and rng.random() < density + 0.2:
                    g[r][c] = rng.choice(palette)
        return
    if layout == "diag":
        for k in range(min(h, c_end - c_start)):
            g[k][c_start + k] = rng.choice(palette)
        return
    if layout == "stripes":
        for r in range(h):
            color = rng.choice(palette)
            for c in range(c_start, c_end):
                if rng.random() < density and r % 2 == 0:
                    g[r][c] = color
        return
    if layout == "scattered":
        for r in range(h):
            for c in range(c_start, c_end):
                if (r + c) % 2 == 0 and rng.random() < density + 0.1:
                    g[r][c] = rng.choice(palette)
        return
    for r in range(h):
        for c in range(c_start, c_end):
            if rng.random() < density:
                g[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, h, rng):
    sw = 4
    w = 2 * sw + 1
    g = full_grid(h, w, 0)
    sep = sw
    for r in range(h):
        g[r][sep] = 5
    if name == "empty_sides":
        return g
    if name == "full_sides":
        color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        for r in range(h):
            for c in range(w):
                if c != sep:
                    g[r][c] = color
        return g
    if name == "no_divider":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        for r in range(h):
            g[r][sep] = 5
        return g
    return g
