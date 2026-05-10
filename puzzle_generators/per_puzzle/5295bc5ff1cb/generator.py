"""Generator for caa06a1f.

Rule: top pattern + bottom cover region; output shifts pattern one step
left, fills over the cover.

Combinatorial axes (8): grid_h/w, top_h, palette_size, palette_kind,
pattern_kind, anchor_corner, asymmetry_force, include_decoy.
Degenerates: no_cover, no_pattern, full_cover.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5295bc5ff1cb"
VERSION = "1.1.0"
TASK_ID = "5295bc5ff1cb"
SUMMARY = "Top pattern + bottom cover region; rule outputs the pattern shifted left."

INVARIANTS = [
    "cover color at cell (h-1, w-1)",
    "rows 0..top_h-1 have a non-cover pattern in col 0",
    "cover fills the bottom region from row top_h onward",
    "top pattern uses a small palette (2-3 colors)",
]

PATTERN_KINDS = ("diag", "stripe", "checker", "blocks")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cover", "no_pattern", "full_cover")
HELPFUL_TEXTURES = PATTERN_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "top_h":          {"type": "int", "default": "rng 2..6", "valid": "2..8"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "pattern_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATTERN_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for pattern_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
        ps_lo, ps_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
        ps_lo, ps_hi = 3, 4
    else:
        h_lo, h_hi = 8, 12
        ps_lo, ps_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size",
                                                  ps_lo, ps_hi)))
    palette_size = max(2, min(4, palette_size))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, palette_size + 1, rng)
    cover = palette[0]
    pattern_palette = palette[1:]
    if not pattern_palette:
        pattern_palette = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != cover]
    g = full_grid(h, w, cover)
    top_h = int(overrides.get("top_h", rng.randint(2, max(2, h // 2))))
    top_h = max(2, min(top_h, h - 1))
    pattern_kind = (overrides.get("texture") or
                    overrides.get("pattern_kind")
                    or ctx.draw_choice("pattern_kind", list(PATTERN_KINDS)))
    for r in range(top_h):
        for c in range(w):
            g[r][c] = _paint_cell(pattern_kind, r, c, pattern_palette)
    return g


def _paint_cell(kind, r, c, pal):
    if kind == "stripe":
        return pal[r % len(pal)]
    if kind == "checker":
        return pal[(r + c) % len(pal)]
    if kind == "blocks":
        return pal[(c // 2) % len(pal)]
    return pal[(r + c) % len(pal)]


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [0, 1, 5, 7, 8]
    elif kind == "primary":
        pool = [0, 1, 2, 3, 4]
    else:
        pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_cover":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 3 + 1
        return g
    if name == "no_pattern":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    if name == "full_cover":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
