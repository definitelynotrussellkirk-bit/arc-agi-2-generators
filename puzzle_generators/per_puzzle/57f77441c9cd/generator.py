"""Generator for puzzle e7b06bea.

Rule: col 0 has a vertical 5-segment (height gh); right-side colored
columns start at cs. Output unrolls colored columns into cycling pattern.

Combinatorial axes (8): grid_h/w, gh, cs, palette_kind, palette_size,
column_density, anchor_corner, asymmetry_force.
Degenerates: no_segment, no_colored_cols, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57f77441c9cd"
VERSION = "1.1.0"
TASK_ID = "57f77441c9cd"
SUMMARY = "Col-0 5-segment + right-side colored cols; rule unrolls them."

INVARIANTS = [
    "background is 0",
    "col 0 rows 0..gh-1 are 5; rows gh..h-1 are 0",
    "rows 0 of cols 1..cs-1 are 0",
    "row 0 of col cs is non-0 non-5",
    "cols cs..w-1 each have non-bg non-5 cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_segment", "no_colored_cols", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "gh":             {"type": "int", "default": "rng 2..h-2",
                       "valid": "1..h-1"},
    "cs":             {"type": "int", "default": "rng 2..w-3",
                       "valid": "1..w-1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "column_density": {"type": "float", "default": "rng 0.3..0.7",
                       "valid": "0.1..1"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    gh = int(overrides.get("gh",
                           ctx.draw_int("gh", 2, max(2, h - 2))))
    gh = max(1, min(h - 1, gh))
    cs = int(overrides.get("cs",
                           ctx.draw_int("cs", 2, max(2, w - 3))))
    cs = max(1, min(w - 1, cs))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    palette = _build_palette(palette_kind, palette_size, rng)
    density = float(overrides.get("column_density",
                                  ctx.draw_rng("column_density")
                                  .uniform(0.3, 0.7)))
    g = full_grid(h, w, 0)
    for r in range(gh):
        g[r][0] = 5
    for c in range(cs, w):
        for r in range(h):
            if rng.random() < density:
                g[r][c] = rng.choice(palette)
        if g[0][c] in (0, 5):
            g[0][c] = palette[0]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_segment":
        # Col 0 has no 5s
        for c in range(2, w):
            for r in range(h):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "no_colored_cols":
        # Just the segment, no right-side colored columns
        for r in range(h // 2):
            g[r][0] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([1, 2, 3, 4, 5])
        return g
    return g
