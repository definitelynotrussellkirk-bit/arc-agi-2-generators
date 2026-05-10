"""Generator for puzzle f9012d9b.

Rule: periodic pattern (period p) with some cells erased to 0. Output:
zh x zw grid (= 0-region bbox dims) showing what the pattern says.

Combinatorial axes (8): period, n_tiles_h, n_tiles_w, palette_size,
erase_h, erase_w, erase_position, anchor_corner.
Degenerates: no_erase, all_erased, no_period.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "453e406712ce"
VERSION = "1.1.0"
TASK_ID = "453e406712ce"
SUMMARY = "Periodic-tiled grid w/ erased rect; rule outputs the periodic crop."

INVARIANTS = [
    "h, w divisible by p (p in [2, 4])",
    "pxp tile uses 2 distinct non-zero colors",
    "exactly 1 rectangular 0-region (1x1 to 3x3)",
    "non-zero cells respect periodic tile",
]

ERASE_POSITIONS = ("center", "corner", "spread", "edge")
DEGENERATE_TEXTURES = ("no_erase", "all_erased", "no_period")
HELPFUL_TEXTURES = ERASE_POSITIONS

AXES = {
    "period":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_tiles_h":      {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "n_tiles_w":      {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..4"},
    "erase_h":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "erase_w":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "erase_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ERASE_POSITIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for erase_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        p_lo, p_hi = 2, 2
    elif difficulty == "hard":
        p_lo, p_hi = 3, 4
    else:
        p_lo, p_hi = 2, 3
    p = int(overrides.get("period",
                          ctx.draw_int("period", p_lo, p_hi)))
    p = max(2, min(4, p))
    n_h = int(overrides.get("n_tiles_h",
                            ctx.draw_int("n_tiles_h", 2, 4)))
    n_w = int(overrides.get("n_tiles_w",
                            ctx.draw_int("n_tiles_w", 2, 4)))
    h = p * n_h
    w = p * n_w
    palette_size = int(overrides.get("palette_size", 2))
    palette_size = max(2, min(4, palette_size))
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], palette_size)
    while True:
        tile = [[rng.choice(palette) for _ in range(p)] for _ in range(p)]
        flat_set = set(tile[r][c] for r in range(p) for c in range(p))
        if len(flat_set) >= 2:
            break
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % p][c % p]
    eh = int(overrides.get("erase_h",
                           ctx.draw_int("erase_h", 1, 2)))
    ew = int(overrides.get("erase_w",
                           ctx.draw_int("erase_w", 1, 2)))
    eh = max(1, min(3, min(h, eh)))
    ew = max(1, min(3, min(w, ew)))
    pos = (overrides.get("texture") or
           overrides.get("erase_position")
           or ctx.draw_choice("erase_position",
                              list(ERASE_POSITIONS)))
    er, ec = _pick_erase(pos, h, w, eh, ew, rng)
    for r in range(er, er + eh):
        for c in range(ec, ec + ew):
            g[r][c] = 0
    return g


def _pick_erase(pos, h, w, eh, ew, rng):
    if pos == "center":
        return max(0, (h - eh) // 2), max(0, (w - ew) // 2)
    if pos == "corner":
        return rng.choice([(0, 0), (0, w - ew), (h - eh, 0),
                           (h - eh, w - ew)])
    if pos == "edge":
        side = rng.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return 0, rng.randint(0, w - ew)
        if side == "bottom":
            return h - eh, rng.randint(0, w - ew)
        if side == "left":
            return rng.randint(0, h - eh), 0
        return rng.randint(0, h - eh), w - ew
    return rng.randint(0, h - eh), rng.randint(0, w - ew)


def _draw_from_degenerate(name, rng):
    p = 2
    h = w = 6
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    tile = [[palette[(r + c) % 2] for c in range(p)] for r in range(p)]
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % p][c % p]
    if name == "no_erase":
        return g
    if name == "all_erased":
        return full_grid(h, w, 0)
    if name == "no_period":
        # Random pattern with no period
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice(palette)
        # Erase a rect
        g[2][2] = 0
        return g
    return g
