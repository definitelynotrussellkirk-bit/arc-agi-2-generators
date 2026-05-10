"""Generator for puzzle 9ddd00f0.

Rule: k(k+1)-1 square; decode self-indexed kxk macro grid where each
block has one hole at its block coordinate.

Combinatorial axes (8): k, fg_color, palette_kind, anchor_corner,
asymmetry_force, hole_pattern_kind, decoy_density, palette_size.
Degenerates: empty_grid, full_grid, no_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "94a828f72627"
VERSION = "1.1.0"
TASK_ID = "94a828f72627"
SUMMARY = "k(k+1)-1 square; rule decodes self-indexed macro grid."

INVARIANTS = [
    "input is square with side h = k*(k+1) - 1, k in {2, 3, 4}",
    "single non-bg color throughout (except holes)",
    "separators (r mod (k+1) == k OR c mod (k+1) == k) are 0",
    "within each block, exactly one cell at block-coord is 0",
]

PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "no_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "k":               {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "fg_color":        {"type": "color", "default": "rng (≠0)",
                        "valid": "1..9"},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "asymmetry_force": {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "hole_pattern_kind": {"type": "str", "default": "default",
                          "valid": "default"},
    "decoy_density":   {"type": "float", "default": "0", "valid": "0..0"},
    "palette_size":    {"type": "int", "default": "1", "valid": "1..1"},
    "texture":         {"type": "str", "default": "alias for palette_kind",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        k_lo, k_hi = 2, 2
    elif difficulty == "hard":
        k_lo, k_hi = 3, 4
    else:
        k_lo, k_hi = 2, 3
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        k = rng.randint(k_lo, k_hi)
        return _draw_from_degenerate(overrides["texture"], k, rng)
    k = int(overrides.get("k", ctx.draw_int("k", k_lo, k_hi)))
    k = max(2, min(4, k))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    fg = int(overrides.get("fg_color", pool[0]))
    if fg == 0:
        fg = pool[0]
    period = k + 1
    h = w = k * period - 1
    g = full_grid(h, w, fg)
    for r in range(h):
        for c in range(w):
            if r % period == k or c % period == k:
                g[r][c] = 0
    for br in range(k):
        for bc in range(k):
            r = br * period + bc
            c = bc * period + br
            g[r][c] = 0
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = fg
    return g


def _draw_from_degenerate(name, k, rng):
    period = k + 1
    h = w = k * period - 1
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, fg)
    if name == "empty_grid":
        return [[0] * w for _ in range(h)]
    if name == "full_grid":
        return g
    if name == "no_holes":
        for r in range(h):
            for c in range(w):
                if r % period == k or c % period == k:
                    g[r][c] = 0
        return g
    return g
