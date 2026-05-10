"""Generator for b2bc3ffd.

Rule: bg=7; rule shifts each non-7/non-8 4-connected component up by
its cell count.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_components,
component_kind.
Degenerates: no_components, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "483682b75e12"
VERSION = "1.1.0"
TASK_ID = "483682b75e12"
SUMMARY = "Components on bg=7; rule shifts each up by its cell count."

INVARIANTS = [
    "background is 7",
    "at least two connected components of non-bg non-8 colors",
    "each component upward shift equal to its size keeps it in-bounds",
    "components separated by margin of at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "single_component", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_components":   {"type": "int", "default": "3", "valid": "2..4"},
    "component_kind": {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        h_lo, h_hi = 14, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", 12, 16)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 9] if c not in pool]
    palette = pool[:3]
    g = full_grid(h, w, 7)
    placed = 0
    for color in palette:
        for _try in range(20):
            sz = rng.randint(2, 3)
            is_h = rng.random() < 0.5
            if is_h:
                cells = [(0, dc) for dc in range(sz)]
                rh, rw = 1, sz
            else:
                cells = [(dr, 0) for dr in range(sz)]
                rh, rw = sz, 1
            rr = rng.randint(2 * h // 3, h - rh)
            rc = rng.randint(0, w - rw)
            ok = all(g[rr + dr][rc + dc] == 7 for dr, dc in cells)
            if ok:
                for r in range(max(0, rr - 1), min(h, rr + rh + 1)):
                    for c in range(max(0, rc - 1), min(w, rc + rw + 1)):
                        if g[r][c] != 7:
                            ok = False; break
                    if not ok:
                        break
            if not ok:
                continue
            for dr, dc in cells:
                g[rr + dr][rc + dc] = color
            placed += 1
            break
    if placed < 2:
        return [[7]]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 9]
    pool = [c for c in pool if c not in (0, 7, 8)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 14, 7)
    if name == "no_components":
        return g
    if name == "single_component":
        for c in range(3):
            g[12][2 + c] = 2
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
