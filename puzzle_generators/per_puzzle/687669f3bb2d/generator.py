"""Generator for 3b:hard_16 — scale the unique vertically symmetric component.

Rule: among color-3 components, pick the first whose normalized cells
form a vertically (LR-mirror) symmetric shape. Output is that shape
2x-upscaled, painted color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_vsym (no symmetric component → rule selects nothing),
all_vsym (every component is symmetric → first-match makes selection
order-sensitive), single_component (only one shape → no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "687669f3bb2d"
VERSION = "1.1.0"
TASK_ID = "687669f3bb2d"

SUMMARY = "1 vertically-symmetric color-3 shape + 1-2 asymmetric color-3 shapes."

INVARIANTS = [
    "background is 0",
    "1 color-3 component is vertically (LR) mirror-symmetric",
    "1-2 other color-3 components are NOT vertically symmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_vsym", "all_vsym", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "one_vsym_with_asym_distractors",
                       "valid": "one_vsym_with_asym_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_VSYM = [
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],          # plus
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],   # H
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],          # T
]
_ASYM = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(60):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_asym = 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 15, 18)
        n_asym = 2
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_asym = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    _place_or_raise(g, rng, rng.choice(_VSYM), 3, "v-symmetric")
    if n_asym is None:
        n_asym = rng.randint(1, 2)
    for _ in range(n_asym):
        _place_or_raise(g, rng, rng.choice(_ASYM), 3, "asymmetric")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_vsym":
        # Only asymmetric components — rule's "first vsym" selector
        # finds nothing; output undefined.
        for shape, base in [(_ASYM[0], (1, 1)), (_ASYM[1], (5, 8)), (_ASYM[2], (8, 2))]:
            for dr, dc in shape:
                g[base[0] + dr][base[1] + dc] = 3
        return g
    if name == "all_vsym":
        # Every component is symmetric — rule's "first-match" makes
        # selection depend on scan order, not a property of the input.
        for shape, base in [(_VSYM[0], (1, 1)), (_VSYM[1], (5, 7)), (_VSYM[2], (8, 2))]:
            for dr, dc in shape:
                g[base[0] + dr][base[1] + dc] = 3
        return g
    if name == "single_component":
        # Only one component — selector is trivial; no asymmetric
        # distractors so the rule has no contrast to demonstrate.
        for dr, dc in _VSYM[0]:
            g[2 + dr][5 + dc] = 3
        return g
    return g
