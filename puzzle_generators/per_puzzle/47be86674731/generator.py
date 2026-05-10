"""Generator for 9a4bb226.

Rule: find 3×3 sub-block all non-zero with exactly 3 distinct colors;
output that crop.

Combinatorial axes (8): grid_h/w, palette_size, palette_kind,
position_bias, color_distribution, n_decoys, anchor_corner,
asymmetry_force.
Degenerates: no_match, multiple_matches, all_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "47be86674731"
VERSION = "1.1.0"
TASK_ID = "47be86674731"
SUMMARY = "One 3×3 fully-filled block w/ 3 distinct colors; rule outputs that crop."

INVARIANTS = [
    "background is 0",
    "exactly one 3×3 sub-block where all 9 cells non-zero AND uses 3 distinct colors",
    "scattered isolated cells elsewhere don't form another match",
]

POSITION_BIAS = ("center", "spread", "edge")
COLOR_DISTRIBUTIONS = ("balanced", "skewed", "diag", "rows")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_match", "multiple_matches", "all_one_color")
HELPFUL_TEXTURES = COLOR_DISTRIBUTIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":            {"type": "int", "default": "rng 11..16", "valid": "9..20"},
    "palette_size":      {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "position_bias":     {"type": "str", "default": "rng spread|center|edge",
                          "valid": "spread|center|edge"},
    "color_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COLOR_DISTRIBUTIONS)},
    "n_decoys":          {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for color_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 9, 9, 12
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 15, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 14, 11, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [5, 7, 8]
    elif palette_kind == "small":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:3]
    while len(palette) < 3:
        palette.append(palette[0])
    color_dist = (overrides.get("texture") or
                  overrides.get("color_distribution")
                  or ctx.draw_choice("color_distribution",
                                     list(COLOR_DISTRIBUTIONS)))
    pattern_cells = _build_pattern(color_dist, palette, rng)
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 0)
    if bias == "center":
        r0 = (h - 3) // 2; c0 = (w - 3) // 2
    elif bias == "edge":
        r0 = 0; c0 = 0
    else:
        r0 = rng.randint(0, h - 3); c0 = rng.randint(0, w - 3)
    paint_at(g, r0, c0, pattern_cells)
    n_decoys = int(overrides.get("n_decoys",
                                 ctx.draw_int("n_decoys", 0, 3)))
    placed = 0
    for _ in range(n_decoys * 5):
        if placed >= n_decoys:
            break
        for _try in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                # Avoid creating another 3x3 match
                if not _adjacent_to_block(r, c, r0, c0, 4):
                    g[r][c] = rng.choice(palette)
                    placed += 1
                    break
            else:
                continue
    return g


def _build_pattern(dist, palette, rng):
    if dist == "diag":
        pattern = [
            (0, 0, palette[0]), (0, 1, palette[1]), (0, 2, palette[2]),
            (1, 0, palette[1]), (1, 1, palette[2]), (1, 2, palette[0]),
            (2, 0, palette[2]), (2, 1, palette[0]), (2, 2, palette[1]),
        ]
        return pattern
    if dist == "rows":
        return [
            (0, 0, palette[0]), (0, 1, palette[0]), (0, 2, palette[0]),
            (1, 0, palette[1]), (1, 1, palette[1]), (1, 2, palette[1]),
            (2, 0, palette[2]), (2, 1, palette[2]), (2, 2, palette[2]),
        ]
    if dist == "skewed":
        return [
            (0, 0, palette[0]), (0, 1, palette[0]), (0, 2, palette[0]),
            (1, 0, palette[0]), (1, 1, palette[0]), (1, 2, palette[1]),
            (2, 0, palette[1]), (2, 1, palette[2]), (2, 2, palette[2]),
        ]
    return [
        (0, 0, palette[0]), (0, 1, palette[0]), (0, 2, palette[0]),
        (1, 0, palette[1]), (1, 1, palette[2]), (1, 2, palette[2]),
        (2, 0, palette[1]), (2, 1, palette[0]), (2, 2, palette[0]),
    ]


def _adjacent_to_block(r, c, r0, c0, dist):
    return r0 - dist <= r <= r0 + 2 + dist and c0 - dist <= c <= c0 + 2 + dist


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(palette)
    if name == "no_match":
        for r in range(0, h, 3):
            for c in range(0, w, 3):
                if r < h and c < w:
                    g[r][c] = palette[0]
        return g
    if name == "multiple_matches":
        if h >= 5 and w >= 9:
            for dr in range(3):
                for dc in range(3):
                    g[dr][dc] = palette[(dr + dc) % 3]
                    g[dr][6 + dc] = palette[(dr + dc) % 3]
        return g
    if name == "all_one_color":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0]
        return g
    return g
