"""Generator for 0b148d64.

Rule: find non-bg color with fewest cells; crop input to its bbox.

Combinatorial axes (8): grid_h/w, big_region_size, small_region_size,
big_density, small_density, palette_kind, position_layout,
asymmetry_force.
Degenerates: single_color, equal_counts, no_minority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d17f2bbc0878"
VERSION = "1.1.0"
TASK_ID = "d17f2bbc0878"
SUMMARY = "Two non-overlapping regions of different colors; rule crops to minority bbox."

INVARIANTS = [
    "background is 0",
    "two distinct non-bg colors A, B",
    "A's region has STRICTLY more non-bg cells than B's",
    "regions don't overlap (separated by >=1 empty row/col)",
]

POSITION_LAYOUTS = ("top_left_big", "top_right_big", "bottom_left_big",
                    "bottom_right_big", "stacked", "side_by_side")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("single_color", "equal_counts", "no_minority")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 14..20", "valid": "10..24"},
    "grid_w":            {"type": "int", "default": "rng 14..20", "valid": "10..24"},
    "big_region_size":   {"type": "str", "default": "rng medium|large",
                          "valid": "small|medium|large"},
    "small_region_size": {"type": "str", "default": "rng small|medium",
                          "valid": "small|medium"},
    "big_density":       {"type": "float", "default": "rng 0.5..0.7",
                          "valid": "0.3..1"},
    "small_density":     {"type": "float", "default": "rng 0.3..0.5",
                          "valid": "0.1..0.7"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "position_layout":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_LAYOUTS)},
    "texture":           {"type": "str", "default": "alias for position_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 14, 20
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
        pool = [1, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    colors = pool[:2]
    while len(colors) < 2:
        colors.append(colors[0])
    big_size = overrides.get("big_region_size",
                             ctx.draw_choice("big_region_size",
                                             ["medium", "large"]))
    small_size = overrides.get("small_region_size",
                               ctx.draw_choice("small_region_size",
                                               ["small", "medium"]))
    if big_size == "large":
        bh, bw = rng.randint(6, 8), rng.randint(8, 10)
    elif big_size == "small":
        bh, bw = rng.randint(4, 5), rng.randint(5, 7)
    else:
        bh, bw = rng.randint(5, 7), rng.randint(7, 9)
    if small_size == "small":
        sh, sw = rng.randint(2, 3), rng.randint(3, 4)
    else:
        sh, sw = rng.randint(3, 4), rng.randint(4, 6)
    bh = min(bh, h - sh - 2)
    bw = min(bw, w)
    sh = min(sh, h - bh - 1)
    sw = min(sw, w)
    layout = (overrides.get("texture") or
              overrides.get("position_layout")
              or ctx.draw_choice("position_layout",
                                 list(POSITION_LAYOUTS)))
    big_density = float(overrides.get("big_density",
                                      ctx.draw_rng("big_density")
                                      .uniform(0.5, 0.7)))
    small_density = float(overrides.get("small_density",
                                        ctx.draw_rng("small_density")
                                        .uniform(0.3, 0.5)))
    g = full_grid(h, w, 0)
    br0, bc0, sr0, sc0 = _layout_positions(layout, h, w, bh, bw, sh, sw)
    big_count = 0
    for r in range(br0, br0 + bh):
        for c in range(bc0, bc0 + bw):
            if rng.random() < big_density:
                g[r][c] = colors[0]
                big_count += 1
    small_count = 0
    for r in range(sr0, sr0 + sh):
        for c in range(sc0, sc0 + sw):
            if rng.random() < small_density:
                g[r][c] = colors[1]
                small_count += 1
    while small_count >= big_count:
        cells = [(r, c) for r in range(sr0, sr0 + sh)
                 for c in range(sc0, sc0 + sw)
                 if g[r][c] == colors[1]]
        if not cells:
            break
        r, c = rng.choice(cells)
        g[r][c] = 0
        small_count -= 1
    if small_count == 0:
        g[sr0][sc0] = colors[1]
    if big_count == 0:
        g[br0][bc0] = colors[0]
    return g


def _layout_positions(layout, h, w, bh, bw, sh, sw):
    if layout == "top_left_big":
        return 0, 0, h - sh, w - sw
    if layout == "top_right_big":
        return 0, w - bw, h - sh, 0
    if layout == "bottom_left_big":
        return h - bh, 0, 0, w - sw
    if layout == "bottom_right_big":
        return h - bh, w - bw, 0, 0
    if layout == "stacked":
        return 0, 0, bh + 1, 0
    if layout == "side_by_side":
        return 0, 0, 0, max(bw + 1, w - sw)
    return 0, 0, bh + 1, max(0, w - sw)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_color":
        for r in range(3, 7):
            for c in range(3, 7):
                if r < h and c < w:
                    g[r][c] = 1
        return g
    if name == "equal_counts":
        for r in range(2, 4):
            for c in range(2, 4):
                if r < h and c < w:
                    g[r][c] = 1
        for r in range(h - 4, h - 2):
            for c in range(w - 4, w - 2):
                if 0 <= r < h and 0 <= c < w:
                    g[r][c] = 2
        return g
    if name == "no_minority":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = 1
        return g
    return g
