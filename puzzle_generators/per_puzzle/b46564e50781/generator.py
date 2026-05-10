"""Generator for 8b:m50 — emit rays until 5-blocker.

Rule: each non-{0,5} cell emits 4 cardinal rays in its color until
hitting a 5-blocker or grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_blockers, emitter_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b46564e50781"
VERSION = "1.1.0"
TASK_ID = "b46564e50781"
SUMMARY = "1-2 emitter cells + 1-2 5-blocker line segments."

INVARIANTS = [
    "background is 0",
    "1-2 single non-{0,5} emitter cells",
    "1-2 5-line segments (length 3-5)",
    "emitters and blockers aren't 4-adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_blockers", "emitter_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "emitter_with_blockers",
                       "valid": "emitter_with_blockers"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_w = rng.randint(1, 2)
    for _ in range(n_w):
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(2, h - 3); c1 = rng.randint(0, w - 4)
                length = rng.randint(3, min(5, w - c1))
                cells = [(r, c) for c in range(c1, c1 + length)]
            else:
                c = rng.randint(2, w - 3); r1 = rng.randint(0, h - 4)
                length = rng.randint(3, min(5, h - r1))
                cells = [(r, c) for r in range(r1, r1 + length)]
            if any(p in used for p in cells): continue
            for r, c in cells: g[r][c] = 5
            used |= set(cells); break
    n_e = rng.randint(1, 2)
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], n_e)
    for color in palette:
        for _ in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if (r, c) in used: continue
            adj = False
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 5:
                    adj = True; break
            if adj: continue
            g[r][c] = color; used.add((r, c)); break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # Walls but no emitters — rule has no rays to cast.
        for c in range(2, 6): g[3][c] = 5
        return g
    if name == "no_blockers":
        # Emitter but no walls — rays travel to all 4 edges; rule's
        # blocker-stop branch never triggers.
        g[3][5] = 4
        return g
    if name == "emitter_at_corner":
        # Emitter at grid corner — only 2 rays have any length;
        # rule's 4-direction symmetry collapses.
        g[0][0] = 4
        for c in range(2, 6): g[3][c] = 5
        return g
    return g
