"""Generator for arc_puzzle_bank_21_set21_bundle:hard_p07 — BFS to goal via checkpoint with portals.

Rule: BFS from start (color 1) to goal (color 3) but the path must also pass
through a checkpoint (color 2). Walls are color 8. Color-4 portal pair (exactly
2 cells) teleport between each other. Output paints the path color 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_checkpoint (rule's must-pass-through-2 has no anchor →
selector returns nothing); no_path (walls fully separate start from
goal → BFS returns no route, output empty path); walls_block_path
(walls form a barrier the rule cannot route around).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4cea2727fcf9"
VERSION = "1.1.0"
TASK_ID = "4cea2727fcf9"

SUMMARY = "Start (1), goal (3), checkpoint (2), walls (8), optional portal pair (4×2)."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 start, one color-3 goal, one color-2 checkpoint",
    "0-N color-8 wall cells (some may form a partial barrier)",
    "0-1 portal pair (exactly 2 color-4 cells if present)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_checkpoint", "no_path", "walls_block_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "start_goal_checkpoint_with_walls",
                          "valid": "start_goal_checkpoint_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n_walls = ctx.draw_int("n_walls", 2, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 13, 13)
        n_walls = ctx.draw_int("n_walls", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n_walls = ctx.draw_int("n_walls", 3, 6)
    use_portal = ctx.draw_int("use_portal", 0, 1)
    rng = ctx.draw_rng("layout")

    def place(g, value):
        for _ in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = value
            return (r, c)
        return None

    for outer in range(40):
        g = full_grid(h, w, 0)
        s = place(g, 1)
        if s is None: continue
        cp = None
        for _t in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            if abs(r - s[0]) + abs(c - s[1]) < 3: continue
            g[r][c] = 2; cp = (r, c); break
        if cp is None: continue
        gpos = None
        for _t in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            if abs(r - cp[0]) + abs(c - cp[1]) < 3: continue
            g[r][c] = 3; gpos = (r, c); break
        if gpos is None: continue
        wcol = rng.randint(2, w - 3)
        for r in range(h):
            if g[r][wcol] == 0 and rng.random() < 0.6:
                g[r][wcol] = 8
        for _ in range(n_walls):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 8
                break
        if use_portal:
            placed = 0
            for _ in range(40):
                if placed == 2: break
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 4
                placed += 1
        return g
    raise ValueError("could not realize set21 p07 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_checkpoint":
        # Start + goal but no color-2 checkpoint — rule's via-2 anchor missing.
        g[2][1] = 1; g[6][10] = 3
        return g
    if name == "no_path":
        # Walls fully isolate start from checkpoint/goal — BFS returns nothing.
        g[2][1] = 1
        for r in range(h):
            g[r][3] = 8
        g[5][8] = 2; g[6][10] = 3
        return g
    if name == "walls_block_path":
        # Vertical wall fully spans grid between start and goal.
        g[2][1] = 1; g[5][5] = 2; g[6][10] = 3
        for r in range(h):
            g[r][7] = 8
        return g
    return g
