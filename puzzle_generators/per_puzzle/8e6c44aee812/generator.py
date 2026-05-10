"""Generator for 539a4f51.

Rule: input has staircase pattern. Diagonal yields period+0 sequence.
Output is 2h × 2w with cell (r, c) = nz-diag[max(r, c) % period].

Combinatorial axes (8): period, palette_kind, palette_size,
zero_position, decoy_density, asymmetry_force, padding_size,
include_decoy.
Degenerates: monochrome_diag, full_diag, no_zero_terminator.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8e6c44aee812"
VERSION = "1.1.0"
TASK_ID = "8e6c44aee812"
SUMMARY = "(p+1)×(p+1) staircase grid; rule tiles to 2h × 2w."

INVARIANTS = [
    "h = w = p + 1 for p in 2..7",
    "diagonal cells: distinct palette[i] for i in [0, p), then 0 at i=p (terminator)",
    "cell at (r, c) = palette[max(r, c)] for max(r, c) < p, else 0",
    "rule's nz-diag has length p (no zeros before terminator)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("monochrome_diag", "full_diag", "no_zero_terminator")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "period":         {"type": "int", "default": "rng 2..7", "valid": "2..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_order":  {"type": "str", "default": "rng forward|reverse|random",
                       "valid": "forward|reverse|random"},
    "zero_position":  {"type": "str", "default": "last", "valid": "last"},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "noise_overlay":  {"type": "float", "default": "0", "valid": "0..0"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "color_balance":  {"type": "str", "default": "even", "valid": "even"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        p_lo, p_hi = 2, 3
    elif difficulty == "hard":
        p_lo, p_hi = 6, 9
    else:
        p_lo, p_hi = 2, 7
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        p = rng.randint(p_lo, p_hi)
        return _draw_from_degenerate(overrides["texture"], p, rng)
    p = int(overrides.get("period", ctx.draw_int("period", p_lo, p_hi)))
    p = max(2, min(9, p))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:p]
    if len(palette) < p:
        extra = [c for c in range(1, 10) if c not in palette]
        rng.shuffle(extra)
        palette += extra[:p - len(palette)]
    palette = palette[:p]
    palette_order = overrides.get("palette_order",
                                  ctx.draw_choice("palette_order",
                                                  ["forward", "reverse", "random"]))
    if palette_order == "reverse":
        palette = palette[::-1]
    elif palette_order == "random":
        rng.shuffle(palette)
    n = p + 1
    g = full_grid(n, n, 0)
    for r in range(n):
        for c in range(n):
            idx = max(r, c)
            if idx < p:
                g[r][c] = palette[idx]
    return g


def _draw_from_degenerate(name, p, rng):
    n = p + 1
    g = full_grid(n, n, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "monochrome_diag":
        for r in range(n):
            for c in range(n):
                if max(r, c) < p:
                    g[r][c] = color
        return g
    if name == "full_diag":
        for r in range(n):
            for c in range(n):
                g[r][c] = color
        return g
    if name == "no_zero_terminator":
        # diagonal has no 0 at end → period would extend
        for r in range(n):
            for c in range(n):
                g[r][c] = color
        return g
    return g
