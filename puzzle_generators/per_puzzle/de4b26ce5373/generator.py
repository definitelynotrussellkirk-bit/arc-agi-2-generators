"""Generator for 20b:m138 — paint rays from 2-emitters until 8-walls.

Rule: each 2-cell is an emitter. From each emitter, send rays in 4
cardinal directions; paint cells on the ray with 2 until hitting an
8-wall or grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls (no 8-cells → rays propagate to grid edge,
unblocked behavior), no_emitters (no 2-cells → rule's per-emitter
loop is empty), emitter_in_corner (emitter at corner → only 2 rays
fire; per-direction symmetry collapses).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "de4b26ce5373"
VERSION = "1.1.0"
TASK_ID = "de4b26ce5373"
SUMMARY = "1-2 2-emitters + 1-2 short 8-wall segments."

INVARIANTS = [
    "background is 0",
    "exactly 1-2 2-cells (emitters)",
    "1-2 8-wall segments (vertical or horizontal lines, length 3-5)",
    "emitters and walls are not 4-adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_emitters", "emitter_in_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
        n_w_lo, n_w_hi = 1, 1
        n_e_lo, n_e_hi = 1, 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
        n_w_lo, n_w_hi = 2, 3
        n_e_lo, n_e_hi = 2, 3
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
        n_w_lo, n_w_hi = 1, 2
        n_e_lo, n_e_hi = 1, 2
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_w = rng.randint(n_w_lo, n_w_hi)
    for _ in range(n_w):
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(2, h - 3)
                c1 = rng.randint(0, w - 4)
                length = rng.randint(3, min(5, w - c1))
                cells = [(r, c) for c in range(c1, c1 + length)]
            else:
                c = rng.randint(2, w - 3)
                r1 = rng.randint(0, h - 4)
                length = rng.randint(3, min(5, h - r1))
                cells = [(r, c) for r in range(r1, r1 + length)]
            if any(p in used for p in cells): continue
            for r, c in cells:
                g[r][c] = 8
            used |= set(cells)
            break
    n_e = rng.randint(n_e_lo, n_e_hi)
    for _ in range(n_e):
        for _ in range(40):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            if (r, c) in used: continue
            adj_wall = False
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 8:
                    adj_wall = True; break
            if adj_wall: continue
            g[r][c] = 2
            used.add((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # No 8-walls — rays from emitter propagate to grid edge in
        # all 4 directions; rule's blocking branch never fires.
        g[3][4] = 2
        return g
    if name == "no_emitters":
        # No 2-cells — rule's per-emitter loop is empty; output
        # equals input (just walls).
        for c in range(2, 6): g[3][c] = 8
        for r in range(2, 5): g[r][8] = 8
        return g
    if name == "emitter_in_corner":
        # Emitter at corner — only 2 rays fire (the others go OOB
        # immediately); rule's per-direction symmetry collapses.
        g[0][0] = 2
        for c in range(3, 6): g[2][c] = 8
        return g
    return g
