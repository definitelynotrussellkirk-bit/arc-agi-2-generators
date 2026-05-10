"""Generator for arc_puzzle_bank_21_set22_bundle:hard_p07 — walled BFS through checkpoint with portals.

Rule: outer 8-walls. BFS from start (2) to goal (3) but the path must pass
through checkpoint (5). Color-6 and color-7 form portal pairs. Output paints
the path color 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_checkpoint (no color-5 → BFS via-checkpoint anchor
missing); no_goal (no color-3 → BFS has no destination);
walls_block_path (interior walls fully separate start from goal).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bcac0c8a0478"
VERSION = "1.1.0"
TASK_ID = "bcac0c8a0478"

SUMMARY = "8-walled grid with start (2), goal (3), checkpoint (5), 0-2 portals (6 and 7), interior walls."

INVARIANTS = [
    "background is 0",
    "outer border is color-8 walls",
    "exactly one color-2 start, one color-3 goal, one color-5 checkpoint, all interior",
    "0-1 color-6 portal pair (each appearing exactly 2× if present)",
    "some interior color-8 walls",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_checkpoint", "no_goal", "walls_block_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "n_iw":              {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "use_portal_6":      {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "position_bias":     {"type": "str", "default": "walled_start_goal_checkpoint",
                          "valid": "walled_start_goal_checkpoint"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "4..7"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_iw = ctx.draw_int("n_iw", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n_iw = ctx.draw_int("n_iw", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n_iw = ctx.draw_int("n_iw", 0, 3)
    use_portal_6 = ctx.draw_int("use_portal_6", 0, 1)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8

    def place(value):
        for _ in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = value
            return (r, c)
        return None

    s = place(2)
    if s is None: return g
    cp = None
    for _t in range(80):
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if g[r][c] != 0: continue
        if abs(r - s[0]) + abs(c - s[1]) < 3: continue
        g[r][c] = 5; cp = (r, c); break
    if cp is None: return g
    for _t in range(120):
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if g[r][c] != 0: continue
        if abs(r - cp[0]) + abs(c - cp[1]) < 3: continue
        g[r][c] = 3; break
    if use_portal_6:
        placed = 0
        for _ in range(40):
            if placed == 2: break
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = 6
            placed += 1
    for _ in range(n_iw):
        place(8)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
    if name == "no_checkpoint":
        # No color-5 checkpoint — rule's via-anchor missing.
        g[2][2] = 2; g[5][7] = 3
        return g
    if name == "no_goal":
        # No color-3 goal — BFS has no destination.
        g[2][2] = 2; g[5][5] = 5
        return g
    if name == "walls_block_path":
        # Vertical interior wall fully spans grid.
        g[2][2] = 2; g[3][5] = 5; g[5][7] = 3
        for r in range(1, h - 1):
            if g[r][8] == 0:
                g[r][8] = 8
        return g
    return g
