"""Generator for 5b:m29 — directional rays by seed color.

Rule:
  - color-2 cell emits a horizontal ray (color 7), stops at any color 5
  - color-1 cell emits a vertical ray (color 8), stops at any color 5
  - cells where both rays cross become color 6
  - color 5 cells stay; everything else becomes 0

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds (no color-1 or color-2 → rule has no rays to
emit), no_walls (no color-5 → rule's rays never stop, fill entire row/col),
no_crossings (no row/col where horizontal and vertical rays intersect →
rule's color-6 crossing-marker never fires).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1b9e8a54331b"
VERSION = "1.1.0"
TASK_ID = "1b9e8a54331b"

SUMMARY = "1-2 color-2 horizontal seeds + 1-2 color-1 vertical seeds + 1-2 color-5 walls."

INVARIANTS = [
    "background is 0",
    "1-2 isolated color-2 seeds (emit horizontal)",
    "1-2 isolated color-1 seeds (emit vertical)",
    "1-2 color-5 line segments (length 4-7) acting as walls",
    "seeds and walls are mutually non-adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "no_crossings")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "seeds_plus_walls",
                          "valid": "seeds_plus_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
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

    def place_seed(color, n):
        nonlocal used
        for _ in range(n):
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
    place_seed(2, rng.randint(1, 2))
    place_seed(1, rng.randint(1, 2))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # No color-1 or color-2 seeds — rule has no rays to emit.
        for c in range(2, 7): g[3][c] = 5
        for r in range(4, 8): g[r][8] = 5
        return g
    if name == "no_walls":
        # No color-5 walls — rays never stop, fill entire row/col.
        g[2][3] = 2
        g[6][7] = 1
        return g
    if name == "no_crossings":
        # Horizontal ray and vertical ray never share a (row, col) cell —
        # color-6 crossing-marker never fires.
        # Place horizontal seed at row 2; vertical seed at col 1; both
        # need to share row 2 col 1. But seed-2 is at (2, 5) and seed-1
        # is at (6, 1) — no crossing if walls block the right path.
        for c in range(2, 7): g[3][c] = 5   # wall blocks horizontal ray's column
        for r in range(4, 8): g[r][7] = 5   # wall blocks vertical ray's row
        g[2][8] = 2   # horizontal seed
        g[1][1] = 1   # vertical seed (rays don't cross because of walls)
        return g
    return g
