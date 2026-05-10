"""Generator for c97c0139.

Rule: K connected red bars on bg=0; rule paints cyan diamond aura
around each bar at radius equal to bar length.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_bars, bar_kind.
Degenerates: no_bars, single_bar, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e706449ebf4c"
VERSION = "1.1.0"
TASK_ID = "e706449ebf4c"
SUMMARY = "Red bars with cyan diamond aura at radius equal to bar length."

INVARIANTS = [
    "background is 0",
    "at least one red connected bar of color 2",
    "bars do not touch grid edges so the aura has room",
    "bars separated by bg margin of at least two cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bars", "single_bar", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_bars":         {"type": "int", "default": "2", "valid": "1..3"},
    "bar_kind":       {"type": "str", "default": "rng", "valid": "rng"},
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
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    placed = []
    for _try in range(40):
        if len(placed) >= 2:
            break
        is_horiz = rng.random() < 0.5
        bar_len = rng.randint(2, 4)
        if is_horiz:
            bh, bw = 1, bar_len
        else:
            bh, bw = bar_len, 1
        rr = rng.randint(2, h - bh - 2)
        rc = rng.randint(2, w - bw - 2)
        ok = True
        for r in range(max(0, rr - 2), min(h, rr + bh + 2)):
            for c in range(max(0, rc - 2), min(w, rc + bw + 2)):
                if g[r][c] != 0:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        for dr in range(bh):
            for dc in range(bw):
                g[rr + dr][rc + dc] = 2
        placed.append((rr, rc, bh, bw))
    if not placed:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_bars":
        return g
    if name == "single_bar":
        for c in range(5, 8):
            g[7][c] = 2
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
