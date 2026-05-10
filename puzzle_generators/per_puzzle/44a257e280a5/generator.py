"""Generator for puzzle 484b58aa.

Rule: input has translational-periodic pattern with bg(0) holes; rule
fills holes by extending the detected period.

Combinatorial axes (8): grid_h/w, period_r, period_c, palette_size,
n_holes, tile_pattern, anchor_corner, asymmetry_force.
Degenerates: no_holes, all_holes, no_period.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "44a257e280a5"
VERSION = "1.1.0"
TASK_ID = "44a257e280a5"
SUMMARY = "Periodic pattern with holes; rule fills via translational period."

INVARIANTS = [
    "background is 0",
    "non-bg cells follow a translational period (pr, pc) where pr,pc in 2..4",
    ">=2 holes (bg cells) within the periodic interior",
    ">=2 distinct non-bg colors",
]

TILE_PATTERNS = ("rotated", "stripe_h", "stripe_v", "checker",
                 "diagonal", "block")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "no_period")
HELPFUL_TEXTURES = TILE_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "period_r":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "period_c":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "n_holes":        {"type": "int", "default": "rng 2..6", "valid": "1..15"},
    "tile_pattern":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TILE_PATTERNS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for tile_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pr = int(overrides.get("period_r",
                           ctx.draw_int("period_r", 2, 3)))
    pc = int(overrides.get("period_c",
                           ctx.draw_int("period_c", 2, 3)))
    pr = max(2, min(4, pr))
    pc = max(2, min(4, pc))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=palette_size, exclude={0}))
    n_holes = int(overrides.get("n_holes",
                                ctx.draw_int("n_holes", 2, 6)))
    n_holes = max(1, min(15, n_holes))
    pattern = (overrides.get("texture") or
               overrides.get("tile_pattern")
               or ctx.draw_choice("tile_pattern",
                                  list(TILE_PATTERNS)))
    tile = _build_tile(pattern, pr, pc, palette, rng)
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % pr][c % pc]
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    for r, c in cells[:n_holes]:
        g[r][c] = 0
    return g


def _build_tile(pattern, pr, pc, palette, rng):
    if pattern == "rotated":
        return [[palette[(r + c) % len(palette)]
                 for c in range(pc)] for r in range(pr)]
    if pattern == "stripe_h":
        return [[palette[r % len(palette)] for c in range(pc)]
                for r in range(pr)]
    if pattern == "stripe_v":
        return [[palette[c % len(palette)] for c in range(pc)]
                for r in range(pr)]
    if pattern == "checker":
        return [[palette[(r + c) % 2] for c in range(pc)]
                for r in range(pr)]
    if pattern == "diagonal":
        return [[palette[(r * pc + c) % len(palette)]
                 for c in range(pc)] for r in range(pr)]
    if pattern == "block":
        return [[palette[r % len(palette)] if c < pc // 2
                 else palette[-1 % len(palette)]
                 for c in range(pc)] for r in range(pr)]
    return [[palette[(r * pc + c) % len(palette)] for c in range(pc)]
            for r in range(pr)]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    if name == "no_holes":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[(r + c) % 3]
        return g
    if name == "all_holes":
        return g
    if name == "no_period":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        for _ in range(3):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 0
        return g
    return g
