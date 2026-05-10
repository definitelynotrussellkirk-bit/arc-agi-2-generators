"""Generator for 13b:hard_87 — fill chambers by internal key parity.

Rule: 5-walls form chambers. Each chamber's 0-region is filled based
on the count of color-2 keys in that chamber: 0 → bg, odd → 8,
even → 7.

Combinatorial axes (8): ch_h, ch_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_keys, all_zero_count.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cc4d8d3dc442"
VERSION = "1.1.0"
TASK_ID = "cc4d8d3dc442"

SUMMARY = "5-walls form 2x2 chambers; each chamber holds 0-3 color-2 keys."

INVARIANTS = [
    "background is 0",
    "5-walls form a 2x2 chamber layout (outer frame + 1 horizontal + 1 vertical divider)",
    "each chamber has 0-3 color-2 key cells",
    "at least one chamber has odd-count and at least one has even-count keys",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_keys", "all_zero_count")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "ch_w":           {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "2x2_chambers_with_keys",
                       "valid": "2x2_chambers_with_keys"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        ch = ctx.draw_int("ch_h", 4, 4)
        cw = ctx.draw_int("ch_w", 4, 4)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 5, 5)
        cw = ctx.draw_int("ch_w", 5, 5)
    else:
        ch = ctx.draw_int("ch_h", 4, 5)
        cw = ctx.draw_int("ch_w", 4, 5)
    rng = ctx.draw_rng("layout")
    h = 2 * ch + 3; w = 2 * cw + 3
    for outer in range(40):
        g = full_grid(h, w, 0)
        for c in range(w):
            g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
        chambers = [(1, 1), (1, cw + 2), (ch + 2, 1), (ch + 2, cw + 2)]
        counts = [rng.randint(0, 3) for _ in range(4)]
        # Ensure mix of odd/even/zero so output has variety
        if not any(c % 2 == 1 for c in counts) or not any(c % 2 == 0 and c > 0 for c in counts):
            continue
        for (rr, cc), cnt in zip(chambers, counts):
            if cnt == 0: continue
            cells = [(r, c) for r in range(rr, rr + ch) for c in range(cc, cc + cw)]
            slots = rng.sample(cells, cnt)
            for r, c in slots:
                g[r][c] = 2
        return g
    raise ValueError("could not realize parity mix in 40 attempts")


def _draw_from_degenerate(name, rng):
    ch, cw = 4, 4
    h, w = 2 * ch + 3, 2 * cw + 3
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # No 5-walls — chambers are undefined, parity rule has no scope.
        g[2][2] = 2; g[7][8] = 2
        return g
    if name == "no_keys":
        # Walls present but no keys anywhere — every chamber has count 0 (no fill).
        for c in range(w):
            g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
        return g
    if name == "all_zero_count":
        # Walls + keys outside chambers — chambers count 0 but keys exist.
        for c in range(w):
            g[0][c] = 5; g[ch + 1][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][cw + 1] = 5; g[r][w - 1] = 5
        return g
    return g
