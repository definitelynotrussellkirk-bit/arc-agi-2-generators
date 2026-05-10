"""Generator for 13b:m87 — cast rays from emitters until wall.

Rule: each emitter cell (color 2) casts 4 cardinal rays (color 8)
that travel until they hit a wall cell (color 5) or the grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_walls, emitter_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "022556f7ee2c"
VERSION = "1.1.0"
TASK_ID = "022556f7ee2c"
SUMMARY = "2-3 emitter cells (color 2) + 1-2 wall line segments (color 5)."

INVARIANTS = [
    "background is 0",
    "2-3 single emitter cells in color 2",
    "1-2 line segments (length 4-7) of color 5 (walls)",
    "emitters and walls are not 4-adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_walls", "emitter_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "emitters_with_walls",
                       "valid": "emitters_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_walls = rng.randint(1, 2)
    for _ in range(n_walls):
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(2, h - 3)
                c1 = rng.randint(1, w - 5)
                length = rng.randint(4, min(7, w - 1 - c1))
                cells = [(r, c) for c in range(c1, c1 + length)]
            else:
                c = rng.randint(2, w - 3)
                r1 = rng.randint(1, h - 5)
                length = rng.randint(4, min(7, h - 1 - r1))
                cells = [(r, c) for r in range(r1, r1 + length)]
            if any(p in used for p in cells): continue
            for r, c in cells: g[r][c] = 5
            used |= set(cells); break
    n_emitters = rng.randint(2, 3)
    for _ in range(n_emitters):
        for _ in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if (r, c) in used: continue
            adj_wall = False
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 5:
                    adj_wall = True; break
            if adj_wall: continue
            g[r][c] = 2; used.add((r, c)); break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # Walls but no emitters — rule has no rays to cast.
        for c in range(2, 7): g[4][c] = 5
        return g
    if name == "no_walls":
        # Emitter but no walls — rays travel to grid edges; rule's
        # "stop on wall" branch never fires.
        g[5][5] = 2
        return g
    if name == "emitter_at_corner":
        # Emitter at grid corner — only 2 of 4 rays have any
        # length; rule's 4-direction symmetry collapses.
        g[0][0] = 2
        for c in range(2, 7): g[3][c] = 5
        return g
    return g
