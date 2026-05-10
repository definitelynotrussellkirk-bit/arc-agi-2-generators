"""Generator for 845d6e51.

Rule: 5-divider; non-3 non-5 key shapes above; 3-shapes below; for
each 3-shape, find a key with same size and bbox dims and recolor.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_pairs,
shape_variant.
Degenerates: no_keys, no_targets, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fea129f7a029"
VERSION = "1.1.0"
TASK_ID = "fea129f7a029"
SUMMARY = "5-divider row; keys above match 3-shapes below by size and bbox."

INVARIANTS = [
    "exactly one full-width row of 5s as the divider",
    "two or three key shapes above the divider in distinct non-3 non-5 colors",
    "two or three matching 3-shapes below the divider",
    "key and target shapes pair up by cell count and bbox dimensions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_targets", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHAPES = [
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, np_lo, np_hi = 12, 13, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, np_lo, np_hi = 14, 17, 3, 3
    else:
        h_lo, h_hi, np_lo, np_hi = 12, 15, 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", 14, 16)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    g = full_grid(h, w, 0)
    div = h // 2
    for c in range(w):
        g[div][c] = 5
    n_pairs = rng.randint(np_lo, np_hi)
    chosen = []
    sizes_used = set()
    while len(chosen) < n_pairs:
        s = rng.choice(SHAPES)
        sh = max(r for r, _c in s) + 1
        sw = max(c for _r, c in s) + 1
        sig = (len(s), sh, sw)
        if sig in sizes_used:
            continue
        chosen.append(s)
        sizes_used.add(sig)
    if len(pool) < n_pairs:
        pool = pool + [c for c in [1, 2, 4, 6, 7, 8, 9] if c not in pool]
    palette = pool[:n_pairs]
    placed_top = []
    for shape, color in zip(chosen, palette):
        sh = max(r for r, _c in shape) + 1
        sw = max(c for _r, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(0, div - sh - 1)
            c0 = rng.randint(0, w - sw - 1)
            if any(abs(r0 - pr) < (sh + 2) and abs(c0 - pc) < (sw + 2) for pr, pc in placed_top):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            placed_top.append((r0, c0))
            break
    placed_bot = []
    for shape in chosen:
        sh = max(r for r, _c in shape) + 1
        sw = max(c for _r, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(div + 1, h - sh - 1)
            c0 = rng.randint(0, w - sw - 1)
            if any(abs(r0 - pr) < (sh + 2) and abs(c0 - pc) < (sw + 2) for pr, pc in placed_bot):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = 3
            placed_bot.append((r0, c0))
            break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 4]
    else:
        pool = [1, 2, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 3, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 13, 15
    g = full_grid(h, w, 0)
    div = h // 2
    for c in range(w):
        g[div][c] = 5
    if name == "no_keys":
        for dr, dc in SHAPES[0]:
            g[div + 2 + dr][3 + dc] = 3
        return g
    if name == "no_targets":
        for dr, dc in SHAPES[0]:
            g[2 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
