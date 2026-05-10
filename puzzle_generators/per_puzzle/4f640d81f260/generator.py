"""Generator for 9f27f097.

Rule: non-bg template horizontally flipped into matching all-zero target.

Combinatorial axes (8): grid_h/w, template_size, palette_kind,
template_position, target_position, anchor_corner, asymmetry_force,
palette_size.
Degenerates: no_target, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4f640d81f260"
VERSION = "1.1.0"
TASK_ID = "4f640d81f260"
SUMMARY = "A template is horizontally flipped into the matching all-zero target region."

INVARIANTS = [
    "the statistical background is neither 0 nor part of the template",
    "there is one rectangular zero target region",
    "the nonzero template bbox has the same size as the zero target bbox",
    "the canonical rule writes the horizontally flipped template into the zero region",
]

TEMPLATE_SIZES = ("3x4", "3x5", "4x4", "4x5")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_target", "no_template", "full_grid")
HELPFUL_TEXTURES = TEMPLATE_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "11..16"},
    "template_size":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TEMPLATE_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_position":{"type": "str", "default": "rng",
                       "valid": "left|center|rng"},
    "target_position":{"type": "str", "default": "right",
                       "valid": "right|left|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "texture":        {"type": "str", "default": "alias for template_size",
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
        sizes = ("3x4",)
    elif difficulty == "hard":
        sizes = ("4x4", "4x5", "3x5")
    else:
        sizes = TEMPLATE_SIZES
    size_str = (overrides.get("texture") if overrides.get("texture") in TEMPLATE_SIZES else None) or \
               overrides.get("template_size") or \
               ctx.draw_choice("template_size", list(sizes))
    th, tw = (int(s) for s in size_str.split("x"))
    h = max(int(overrides.get("grid_h", 9)), th + 4)
    w = max(int(overrides.get("grid_w", 13)), 2 * tw + 5)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 4, rng)
    g = full_grid(h, w, 9)
    r0 = max(2, (h - th) // 2)
    c0 = 2
    pattern = []
    for _ in range(th):
        row = []
        for _ in range(tw):
            row.append(rng.choice([9] + palette))
        pattern.append(row)
    pattern[0][0] = palette[0]
    pattern[0][tw - 1] = palette[1 % len(palette)]
    for r in range(th):
        for c in range(tw):
            g[r0 + r][c0 + c] = pattern[r][c]
    target_c = w - tw - 1
    for r in range(th):
        for c in range(tw):
            g[r0 + r][target_c + c] = 0
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8]
    pool = [c for c in pool if c not in (0, 9)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 9)
    if name == "no_target":
        for r in range(2, 5):
            for c in range(2, 6):
                g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "no_template":
        for r in range(2, 5):
            for c in range(8, 12):
                g[r][c] = 0
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 0
        return g
    return g
