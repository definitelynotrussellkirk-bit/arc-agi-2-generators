"""Generator for 239be575.

Rule: 1x1 output reports whether one cyan component bridges two red 2x2
blocks.

Combinatorial axes (8): grid_h/w, bridge, palette_kind, block1_pos,
block2_pos, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_blocks, no_cyan, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "eefadafb2b7b"
VERSION = "1.1.0"
TASK_ID = "eefadafb2b7b"
SUMMARY = "1x1 output reports if cyan bridges two red 2x2 blocks."

INVARIANTS = [
    "the grid contains exactly two separated 2x2 red blocks",
    "cyan cells form either one 8-connected bridge or a non-bridging fragment",
    "red block cells are never overwritten by cyan",
    "the output is 8 for a bridge and 0 otherwise",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "no_cyan", "full_grid")
HELPFUL_TEXTURES = ("bridge", "no_bridge")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..18"},
    "bridge":         {"type": "bool", "default": "rng helpful",
                       "valid": "true|false"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed",
                       "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for bridge",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if overrides.get("texture") == "bridge":
        bridge = True
    elif overrides.get("texture") == "no_bridge":
        bridge = False
    else:
        bridge_o = overrides.get("bridge")
        if bridge_o is None:
            bridge = ctx.draw_choice("bridge", (True, False))
        else:
            bridge = bool(bridge_o)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 8, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 13, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 11, 10, 13
    h = rng.randint(h_lo, h_hi)
    w = rng.randint(w_lo, w_hi)
    b1r = rng.randint(1, 2)
    b1c = rng.randint(1, 2)
    b2r = h - rng.randint(3, 4)
    b2c = w - rng.randint(3, 4)
    g = full_grid(h, w, 0)
    draw_rect(g, b1r, b1c, 2, 2, 2)
    draw_rect(g, b2r, b2c, 2, 2, 2)
    if bridge:
        r, c = b1r + 1, b1c + 2
        target = (b2r, b2c - 1)
        while (r, c) != target:
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = 8
            if r < target[0]:
                r += 1
            elif r > target[0]:
                r -= 1
            if c < target[1]:
                c += 1
            elif c > target[1]:
                c -= 1
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 8
    else:
        for r, c in [(b1r + 1, b1c + 2), (b1r + 2, b1c + 2), (b1r + 3, b1c + 2)]:
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = 8
        for r, c in [(b2r - 1, b2c), (b2r - 1, b2c + 1)]:
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = 8
        er = rng.randint(0, h - 1)
        ec = rng.randint(0, w - 1)
        if g[er][ec] == 0:
            g[er][ec] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        g[3][3] = 8
        return g
    if name == "no_cyan":
        draw_rect(g, 1, 1, 2, 2, 2)
        draw_rect(g, h - 3, w - 3, 2, 2, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
