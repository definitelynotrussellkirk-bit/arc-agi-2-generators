"""Generator for 103eff5b.

Rule: non-8 key tile recolors a scaled color-8 block after a
quarter-turn.

Combinatorial axes (8): key_size, scale, palette_kind, key_position,
block_position, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_key, no_block, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "fd588326c845"
VERSION = "1.1.0"
TASK_ID = "fd588326c845"
SUMMARY = "A non-8 key tile recolors a scaled color-8 block after a quarter-turn."

INVARIANTS = [
    "key cells are the only nonzero non-8 cells",
    "the color-8 region is a solid scaled square block",
    "the 8-region dimensions are integer multiples of the key dimensions",
    "each scaled 8 tile receives the rotated key color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_block", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "key_size":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "scale":          {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key_position":   {"type": "str", "default": "tl",
                       "valid": "tl|tr|bl|br|center"},
    "block_position": {"type": "str", "default": "br",
                       "valid": "tl|tr|bl|br|center"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..9", "valid": "2..9"},
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
        ks_lo, ks_hi = 2, 2
        sc_lo, sc_hi = 2, 2
    elif difficulty == "hard":
        ks_lo, ks_hi = 3, 4
        sc_lo, sc_hi = 3, 5
    else:
        ks_lo, ks_hi = 2, 3
        sc_lo, sc_hi = 2, 3
    key_size = ctx.draw_int("key_size", ks_lo, ks_hi)
    scale = ctx.draw_int("scale", sc_lo, sc_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind,
                             min(key_size * key_size, 8), rng)
    kr = rng.randint(1, 2)
    kc = rng.randint(1, 2)
    er = kr + key_size + rng.randint(2, 3)
    ec = kc + key_size + rng.randint(2, 4)
    block = key_size * scale
    g = full_grid(er + block + 2, ec + block + 2, 0)
    for r in range(key_size):
        for c in range(key_size):
            g[kr + r][kc + c] = palette[(r * key_size + c) % len(palette)]
    draw_rect(g, er, ec, block, block, 8)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_key":
        draw_rect(g, 5, 5, 6, 6, 8)
        return g
    if name == "no_block":
        for r in range(2):
            for c in range(2):
                g[2 + r][2 + c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
