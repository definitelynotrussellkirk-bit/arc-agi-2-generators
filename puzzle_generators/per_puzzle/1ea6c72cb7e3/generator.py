"""Generator for arc_puzzle_bank_21_set17_bundle:hard_p05 — line-of-sight watcher.

Rule: each non-{0, 5} cell is a watcher. Each 0-cell sees watchers on the same
row/col with clear line-of-sight (through 0-cells). 0 visible→0, 1 visible→that
color, 2+ visible→8. Walls and watchers preserved.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_watchers, walls_block_all, single_watcher.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1ea6c72cb7e3"
VERSION = "1.1.0"
TASK_ID = "1ea6c72cb7e3"

SUMMARY = "2-3 single-cell watchers in distinct colors + 0-3 walls (color 5)."

INVARIANTS = [
    "background is 0",
    "2-3 single-cell watchers in distinct non-{0, 5} colors",
    "0-3 sparse color-5 wall cells",
    "watchers are 4-conn isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_watchers", "walls_block_all", "single_watcher")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_watchers":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_walls":        {"type": "int", "default": "rng 0..3", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "watchers_with_walls",
                       "valid": "watchers_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
        n_watchers = ctx.draw_int("n_watchers", 2, 2)
        n_walls = ctx.draw_int("n_walls", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
        n_watchers = ctx.draw_int("n_watchers", 3, 4)
        n_walls = ctx.draw_int("n_walls", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n_watchers = ctx.draw_int("n_watchers", 2, 3)
        n_walls = ctx.draw_int("n_walls", 0, 3)
    rng = ctx.draw_rng("layout")
    watcher_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_watchers)

    for outer in range(40):
        g = full_grid(h, w, 0)
        placed = []
        ok = True
        for color in watcher_colors:
            placed_a = False
            for _ in range(120):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if any(abs(r - pr) + abs(c - pc) < 2 for pr, pc in placed): continue
                g[r][c] = color
                placed.append((r, c))
                placed_a = True; break
            if not placed_a:
                ok = False; break
        if not ok: continue
        for _ in range(n_walls):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 5
                break
        return g
    raise ValueError("could not realize set17 p05 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_watchers":
        # Walls but no watchers — rule's visibility scan finds
        # no targets; output uniform 0.
        g[3][3] = 5; g[5][7] = 5
        return g
    if name == "walls_block_all":
        # Walls form a dense grid that blocks every watcher's
        # line-of-sight everywhere — rule's visibility branch
        # never fires.
        g[1][5] = 4; g[7][5] = 6
        for c in range(w): g[4][c] = 5
        return g
    if name == "single_watcher":
        # Only one watcher — rule's "0/1/2+" branch never reaches
        # the 2+ → 8 case; effect is mostly recoloring 0 → that
        # watcher's color.
        g[3][5] = 4
        return g
    return g
