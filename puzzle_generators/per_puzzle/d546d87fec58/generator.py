"""Generator for b8825c91.

Rule: square grid with 180-rot-symmetric base pattern + 1-2 4-blocks.
For each 4-cell, look at 180/horizontal/vertical mirror counterparts;
first non-4 wins.

Combinatorial axes (8): grid_size, palette_size, n_erase_blocks,
block_size_range, block_position_bias, base_texture, decoy_density,
underlying_symmetry_kind.
Degenerates: no_erase, all_erase, single_color_base.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "d546d87fec58"
VERSION = "1.1.0"
TASK_ID = "d546d87fec58"
SUMMARY = "Square 180-rot-symmetric pattern with 1-2 4-blocks erased."

INVARIANTS = [
    "h = w (even side, in [10, 20])",
    "underlying base pattern is 180-rotation symmetric",
    "1-2 4-blocks erase rectangular regions",
    "each 4-cell has at least one mirror counterpart that is NOT 4",
]

BASE_TEXTURES = ("noise", "blob", "checkerboard", "stripes", "gradient")
DEGENERATE_TEXTURES = ("no_erase", "all_erase", "single_color_base")
HELPFUL_TEXTURES = BASE_TEXTURES

AXES = {
    "grid_size":            {"type": "int", "default": "rng 12..18", "valid": "10..20"},
    "palette_size":         {"type": "int", "default": "rng 4..7",  "valid": "2..8"},
    "n_erase_blocks":       {"type": "int", "default": "rng 1..3",  "valid": "1..4"},
    "block_h":              {"type": "int", "default": "rng 2..4",  "valid": "1..6"},
    "block_w":              {"type": "int", "default": "rng 2..4",  "valid": "1..6"},
    "block_position_bias":  {"type": "str", "default": "rng spread|center|edge",
                             "valid": "spread|center|edge"},
    "base_texture":         {"type": "str", "default": "rng helpful",
                             "valid": "|".join(BASE_TEXTURES)},
    "texture":              {"type": "str", "default": "alias for base_texture",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        s_lo, s_hi, c_lo, c_hi, b_lo, b_hi = 10, 12, 3, 5, 1, 1
    elif difficulty == "hard":
        s_lo, s_hi, c_lo, c_hi, b_lo, b_hi = 16, 20, 5, 8, 2, 3
    else:
        s_lo, s_hi, c_lo, c_hi, b_lo, b_hi = 12, 18, 4, 7, 1, 2
    s = ctx.draw_int("grid_size", s_lo, s_hi)
    if s % 2:
        s += 1
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], s, rng)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", c_lo, c_hi)))
    palette_pool = [c for c in range(1, 10) if c != 4]
    rng.shuffle(palette_pool)
    palette = palette_pool[:max(2, n_palette)]
    base_texture = (overrides.get("texture") or overrides.get("base_texture")
                    or ctx.draw_choice("base_texture", list(BASE_TEXTURES)))
    n_blocks = int(overrides.get("n_erase_blocks",
                                 ctx.draw_int("n_erase_blocks", b_lo, b_hi)))
    n_blocks = max(1, min(4, n_blocks))
    bh_def = int(overrides.get("block_h", ctx.draw_int("block_h", 2, 4)))
    bw_def = int(overrides.get("block_w", ctx.draw_int("block_w", 2, 4)))
    bias = overrides.get("block_position_bias",
                         ctx.draw_choice("block_position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(s, s, 0)
    _fill_base(g, base_texture, s, palette, rng)
    for r in range(s // 2):
        for c in range(s):
            g[s - 1 - r][s - 1 - c] = g[r][c]
    if s % 2 == 1:
        mid = s // 2
        for c in range(mid + 1):
            g[mid][s - 1 - c] = g[mid][c]
    placed_blocks = []
    for _ in range(n_blocks):
        bh = max(1, min(s - 2, bh_def))
        bw = max(1, min(s - 2, bw_def))
        if bias == "center":
            br = max(0, (s - bh) // 2 + rng.randint(-1, 1))
            bc = max(0, (s - bw) // 2 + rng.randint(-1, 1))
        elif bias == "edge":
            choices = [(0, rng.randint(0, s - bw)),
                       (s - bh, rng.randint(0, s - bw)),
                       (rng.randint(0, s - bh), 0),
                       (rng.randint(0, s - bh), s - bw)]
            br, bc = rng.choice(choices)
        else:
            br = rng.randint(0, s - bh)
            bc = rng.randint(0, s - bw)
        fill_box(g, br, bc, br + bh - 1, bc + bw - 1, 4)
        placed_blocks.append((br, bc, bh, bw))
    has_4 = any(g[r][c] == 4 for r in range(s) for c in range(s))
    if not has_4:
        fill_box(g, 0, 0, 1, 1, 4)
    if all(g[r][c] == 4 for r in range(s) for c in range(s)):
        g[0][0] = palette[0]
    return g


def _fill_base(g, texture, s, palette, rng):
    if texture == "noise":
        for r in range(s):
            for c in range(s):
                g[r][c] = rng.choice(palette)
    elif texture == "checkerboard":
        a, b = palette[0], palette[1] if len(palette) > 1 else palette[0]
        for r in range(s):
            for c in range(s):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif texture == "stripes":
        horiz = rng.random() < 0.5
        if horiz:
            for r in range(s):
                color = rng.choice(palette)
                for c in range(s):
                    g[r][c] = color
        else:
            for c in range(s):
                color = rng.choice(palette)
                for r in range(s):
                    g[r][c] = color
    elif texture == "blob":
        bg = palette[0]
        for r in range(s):
            for c in range(s):
                g[r][c] = bg
        for _ in range(rng.randint(2, 4)):
            color = rng.choice(palette)
            bh = rng.randint(2, max(2, s // 3))
            bw = rng.randint(2, max(2, s // 3))
            r0 = rng.randint(0, s - bh)
            c0 = rng.randint(0, s - bw)
            for rr in range(r0, r0 + bh):
                for cc in range(c0, c0 + bw):
                    g[rr][cc] = color
    elif texture == "gradient":
        for r in range(s):
            for c in range(s):
                g[r][c] = palette[(r + c) % len(palette)]


def _draw_from_degenerate(name, s, rng):
    palette = [c for c in range(1, 10) if c != 4]
    rng.shuffle(palette)
    g = full_grid(s, s, palette[0])
    if name == "no_erase":
        for r in range(s // 2):
            for c in range(s):
                v = rng.choice(palette)
                g[r][c] = v
                g[s - 1 - r][s - 1 - c] = v
        return g
    if name == "all_erase":
        return [[4] * s for _ in range(s)]
    if name == "single_color_base":
        c0 = palette[0]
        for r in range(s):
            for c in range(s):
                g[r][c] = c0
        fill_box(g, 1, 1, 3, 3, 4)
        return g
    return g
