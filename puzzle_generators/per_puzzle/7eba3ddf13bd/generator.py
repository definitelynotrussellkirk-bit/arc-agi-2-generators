"""Generator for arc_puzzle_bank_21_set16_bundle:hard_p02 — BFS through 1-walled maze.

Rule: 1-walled grid; BFS from start (2) to color-3 goal via color-4 marker.
Output paints the path color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_iw, texture.
Degenerates: no_start, no_goal, no_checkpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7eba3ddf13bd"
VERSION = "1.1.0"
TASK_ID = "7eba3ddf13bd"

SUMMARY = "1-walled grid + start (2), goal (3), checkpoint (4), and interior 1-walls."

INVARIANTS = [
    "background is 0",
    "outer border is color-1 walls",
    "exactly one each of color-2 start, color-3 goal, color-4 checkpoint, all interior",
    "some interior color-1 wall cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_start", "no_goal", "no_checkpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_iw":           {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "walled_grid_with_3_markers",
                       "valid": "walled_grid_with_3_markers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        n_iw = ctx.draw_int("n_iw", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_iw = ctx.draw_int("n_iw", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
        n_iw = ctx.draw_int("n_iw", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 1; g[h - 1][c] = 1
    for r in range(h): g[r][0] = 1; g[r][w - 1] = 1

    def place(value, exclude=None):
        for _ in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            if exclude and any(abs(r - er) + abs(c - ec) < 2 for er, ec in exclude): continue
            g[r][c] = value
            return (r, c)
        return None

    placed = []
    for v in (2, 3, 4):
        p = place(v, exclude=placed)
        if p: placed.append(p)
    for _ in range(n_iw):
        for _t in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            if any(abs(r - er) + abs(c - ec) < 2 for er, ec in placed): continue
            g[r][c] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 1; g[h - 1][c] = 1
    for r in range(h): g[r][0] = 1; g[r][w - 1] = 1
    if name == "no_start":
        # Goal + checkpoint but no start (color 2) — rule's BFS has
        # no source node.
        g[2][3] = 4; g[5][7] = 3
        return g
    if name == "no_goal":
        # Start + checkpoint but no goal (color 3) — rule's BFS has
        # no terminal.
        g[2][3] = 2; g[4][6] = 4
        return g
    if name == "no_checkpoint":
        # Start + goal but no checkpoint (color 4) — rule's "via
        # checkpoint" routing has no waypoint to enforce.
        g[2][3] = 2; g[5][7] = 3
        return g
    return g
