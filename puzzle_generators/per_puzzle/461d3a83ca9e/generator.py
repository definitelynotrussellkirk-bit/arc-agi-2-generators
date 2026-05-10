"""Generator for 14b:m95 — cast diagonal rays until wall.

Rule: each non-bg, non-5 cell casts 4 diagonal rays (NE, NW, SE, SW)
in its own color. Rays travel through bg cells until hitting any
non-bg cell or the grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_walls, emitter_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "461d3a83ca9e"
VERSION = "1.1.0"
TASK_ID = "461d3a83ca9e"

SUMMARY = "2-4 isolated diagonal-ray emitters; optional 1-2 walls (color 5)."

INVARIANTS = [
    "background is 0",
    "2-4 isolated single emitter cells in distinct colors (none of color 5)",
    "0-2 walls of color 5 (line segments of length 3-5)",
    "all non-bg cells are pairwise non-adjacent (4-conn) so rays start cleanly",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_walls", "emitter_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "isolated_emitters_optional_walls",
                       "valid": "isolated_emitters_optional_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_walls = rng.randint(0, 2)
    for _ in range(n_walls):
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(2, h - 3)
                c1 = rng.randint(1, w - 4)
                length = rng.randint(3, min(5, w - 1 - c1))
                cells = [(r, c) for c in range(c1, c1 + length)]
            else:
                c = rng.randint(2, w - 3)
                r1 = rng.randint(1, h - 4)
                length = rng.randint(3, min(5, h - 1 - r1))
                cells = [(r, c) for r in range(r1, r1 + length)]
            if any(p in used for p in cells): continue
            for r, c in cells: g[r][c] = 5
            used |= set(cells); break
    n_em = rng.randint(2, 4)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_em)
    for color in palette:
        for _ in range(60):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if (r, c) in used: continue
            adj = False
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                        adj = True; break
                if adj: break
            if adj: continue
            g[r][c] = color; used.add((r, c)); break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # No emitters — rule has nothing to ray from.
        for c in range(2, 5): g[3][c] = 5
        return g
    if name == "no_walls":
        # Emitters but no walls — every ray reaches grid edge (no early stops).
        g[3][3] = 4; g[5][7] = 6
        return g
    if name == "emitter_at_edge":
        # Emitter on a corner — only 1 of 4 diagonal rays is visible.
        g[0][0] = 4
        return g
    return g
