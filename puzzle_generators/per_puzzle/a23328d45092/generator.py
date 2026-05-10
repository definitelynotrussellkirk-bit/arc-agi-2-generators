"""Generator for puzzle a68b268e.

Rule: full-row of 1s and full-col of 1s split the grid into 4
quadrants; output is a single quadrant-sized grid where each cell takes
the first non-zero value in TL,TR,BL,BR priority across the 4 quadrants.

Combinatorial axes (8): grid_h/w, n_palette, palette_kind,
quadrant_density, sep_position, anchor_corner, asymmetry_force,
include_overlap.
Degenerates: empty_quadrant, all_overlap, missing_separator.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a23328d45092"
VERSION = "1.1.0"
TASK_ID = "a23328d45092"
SUMMARY = "4 quadrants split by 1-row + 1-col; rule overlays them."

INVARIANTS = [
    "exactly 1 full-width row of 1s",
    "exactly 1 full-height col of 1s",
    "each quadrant has at least one cell of its own distinct color",
    "quadrants use 4 distinct colors (not 0 or 1)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DENSITY_KINDS = ("sparse", "medium", "dense", "varied")
SEP_POSITIONS = ("center", "off_center", "near_top_left", "near_bot_right")
DEGENERATE_TEXTURES = ("empty_quadrant", "all_overlap", "missing_separator")
HELPFUL_TEXTURES = DENSITY_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "grid_w":            {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "quadrant_density":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(DENSITY_KINDS)},
    "sep_position":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(SEP_POSITIONS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "include_overlap":   {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for quadrant_density",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 7, 11
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    density = (overrides.get("texture") or
               overrides.get("quadrant_density")
               or ctx.draw_choice("quadrant_density",
                                  list(DENSITY_KINDS)))
    sep_pos = overrides.get("sep_position",
                            ctx.draw_choice("sep_position",
                                            list(SEP_POSITIONS)))
    if sep_pos == "center":
        sep_r, sep_c = h // 2, w // 2
    elif sep_pos == "off_center":
        sep_r = h // 2 + (rng.choice([-1, 1]) if h > 6 else 0)
        sep_c = w // 2 + (rng.choice([-1, 1]) if w > 6 else 0)
    elif sep_pos == "near_top_left":
        sep_r = max(2, h // 3); sep_c = max(2, w // 3)
    else:
        sep_r = min(h - 3, 2 * h // 3); sep_c = min(w - 3, 2 * w // 3)
    sep_r = max(2, min(h - 3, sep_r))
    sep_c = max(2, min(w - 3, sep_c))
    g = full_grid(h, w, 0)
    for c in range(w):
        g[sep_r][c] = 1
    for r in range(h):
        g[r][sep_c] = 1
    palette = _build_palette(palette_kind, rng)
    quads = [
        (0, 0, sep_r, sep_c, palette[0]),
        (0, sep_c + 1, sep_r, w, palette[1]),
        (sep_r + 1, 0, h, sep_c, palette[2]),
        (sep_r + 1, sep_c + 1, h, w, palette[3]),
    ]
    d_lo, d_hi = _density_range(density)
    for r0, c0, r1, c1, color in quads:
        d = rng.uniform(d_lo, d_hi)
        for r in range(r0, r1):
            for c in range(c0, c1):
                if rng.random() < d:
                    g[r][c] = color
        # Ensure quadrant has >=1 cell of its color
        has = any(g[r][c] == color for r in range(r0, r1)
                  for c in range(c0, c1))
        if not has:
            r = rng.randint(r0, r1 - 1)
            c = rng.randint(c0, c1 - 1)
            g[r][c] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < 4:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:4]


def _density_range(name):
    if name == "sparse":
        return 0.15, 0.3
    if name == "medium":
        return 0.3, 0.5
    if name == "dense":
        return 0.5, 0.8
    if name == "varied":
        return 0.1, 0.7
    return 0.3, 0.5


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    sep_r, sep_c = h // 2, w // 2
    for c in range(w):
        g[sep_r][c] = 1
    for r in range(h):
        g[r][sep_c] = 1
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    if name == "empty_quadrant":
        # 3 quadrants populated, 1 empty
        quads = [
            (0, 0, sep_r, sep_c, palette[0]),
            (0, sep_c + 1, sep_r, w, palette[1]),
            (sep_r + 1, 0, h, sep_c, palette[2]),
        ]
        for r0, c0, r1, c1, color in quads:
            for r in range(r0, r1):
                for c in range(c0, c1):
                    if rng.random() < 0.4:
                        g[r][c] = color
        return g
    if name == "all_overlap":
        # All quadrants paint the same cell positions → first hit wins
        for q_idx, (r0, c0, r1, c1) in enumerate([
            (0, 0, sep_r, sep_c),
            (0, sep_c + 1, sep_r, w),
            (sep_r + 1, 0, h, sep_c),
            (sep_r + 1, sep_c + 1, h, w),
        ]):
            color = palette[q_idx]
            for r in range(r0, min(r1, r0 + 2)):
                for c in range(c0, min(c1, c0 + 2)):
                    g[r][c] = color
        return g
    if name == "missing_separator":
        # Only the row, no col → quadrants ill-defined
        g2 = full_grid(h, w, 0)
        for c in range(w):
            g2[sep_r][c] = 1
        for r in range(h):
            for c in range(w):
                if r != sep_r and rng.random() < 0.3:
                    g2[r][c] = palette[0]
        return g2
    return g
