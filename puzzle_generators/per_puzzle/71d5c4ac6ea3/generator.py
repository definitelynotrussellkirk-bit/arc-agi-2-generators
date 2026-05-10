"""Generator for arc_puzzle_bank_21_set17_s:S17_H1 — anchor + offset pattern + seeds.

Rule: a color-9 anchor cell + color-1 cells defining a relative offset
pattern + color-2 seed cells. Output stamps the color-1 offset pattern
(in color 8) at each color-2 seed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor (no color-9 cell → rule's anchor selector
returns nothing, offsets undefined), no_offsets (anchor present but
no color-1 cells → rule's offset pattern is empty, stamping is a
no-op), no_seeds (no color-2 cells → rule has nothing to stamp,
output equals input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "71d5c4ac6ea3"
VERSION = "1.1.0"
TASK_ID = "71d5c4ac6ea3"

SUMMARY = "1 color-9 anchor + 2-4 color-1 cells (offset pattern) + 1-3 color-2 seed cells."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 anchor cell",
    "2-4 color-1 cells near the anchor (defining the relative offset pattern)",
    "1-3 single-cell color-2 seeds at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_offsets", "no_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "n_seeds":           {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "anchor_offsets_seeds",
                          "valid": "anchor_offsets_seeds"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
        n_seeds = ctx.draw_int("n_seeds", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
        n_seeds = ctx.draw_int("n_seeds", 1, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ar = rng.randint(1, h // 2)
        ac = rng.randint(1, w // 3)
        g[ar][ac] = 9
        offsets = []
        n_off = rng.randint(2, 4)
        for _ in range(n_off):
            for _t in range(40):
                dr = rng.randint(-1, 2); dc = rng.randint(-1, 2)
                if (dr, dc) == (0, 0): continue
                r, c = ar + dr, ac + dc
                if not (0 <= r < h and 0 <= c < w): continue
                if g[r][c] != 0: continue
                g[r][c] = 1
                offsets.append((dr, dc))
                break
        if not offsets: continue
        placed = 0
        for _ in range(120):
            if placed >= n_seeds: break
            r = rng.randint(h // 2 + 1, h - 2); c = rng.randint(w // 2, w - 2)
            if g[r][c] != 0: continue
            ok = True
            for dr, dc in offsets:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < h and 0 <= nc < w) or g[nr][nc] != 0:
                    ok = False; break
            if not ok: continue
            g[r][c] = 2
            placed += 1
        if placed > 0:
            return g
    raise ValueError("could not realize S17_H1 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # No color-9 anchor — rule's anchor selector finds nothing;
        # offsets undefined.
        g[3][3] = 1; g[3][4] = 1
        g[7][7] = 2
        return g
    if name == "no_offsets":
        # Anchor present but no color-1 cells — rule's offset pattern
        # is empty; stamping is a no-op.
        g[2][2] = 9
        g[7][7] = 2
        return g
    if name == "no_seeds":
        # No color-2 seeds — rule has nothing to stamp; output = input.
        g[2][2] = 9
        g[2][3] = 1; g[3][2] = 1
        return g
    return g
