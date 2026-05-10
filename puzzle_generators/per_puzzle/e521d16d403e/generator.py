"""Generator for 72ca375d.

Rule: extracts the largest LR-symmetric object cropped to its bbox.

Combinatorial axes (8): grid_h/w, palette_kind, n_asym, position_bias,
sym_h, sym_w, anchor_corner, palette_size.
Degenerates: all_asym, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e521d16d403e"
VERSION = "1.1.0"
TASK_ID = "e521d16d403e"
SUMMARY = "Several objects; rule extracts the largest LR-symmetric one cropped to its bbox."

INVARIANTS = [
    "background is 0",
    "exactly one LR-symmetric object, strictly larger than any other LR-symmetric object",
    "other objects are LR-asymmetric or strictly smaller",
    "objects separated by bg margin >= 1",
]

POSITION_BIASES = ("scattered", "spread", "centered", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("all_asym", "no_objects", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES


def _can_place(g, sh, sw, rr, rc, halo=1):
    h, w = len(g), len(g[0])
    for r in range(max(0, rr - halo), min(h, rr + sh + halo)):
        for c in range(max(0, rc - halo), min(w, rc + sw + halo)):
            if g[r][c] != 0:
                return False
    return True


def _make_sym_block(rng, color, sh=None, sw=None):
    if sh is None:
        sh = rng.randint(3, 4)
    if sw is None:
        sw = rng.choice([3, 5])
    block = [[0] * sw for _ in range(sh)]
    half = sw // 2
    for r in range(sh):
        for c in range(half + 1):
            v = color if rng.random() < 0.7 else 0
            block[r][c] = v
            block[r][sw - 1 - c] = v
    for r in range(sh):
        block[r][half] = color
    return block


def _make_asym_block(rng, color):
    sh = rng.randint(2, 3)
    sw = rng.randint(2, 3)
    block = [[color if rng.random() < 0.7 else 0 for _ in range(sw)] for _ in range(sh)]
    block[0][0] = color
    block[0][sw - 1] = 0 if sw > 1 else color
    for r in range(sh):
        block[r][0] = color
    return block


def _paint(g, block, rr, rc):
    for dr, row in enumerate(block):
        for dc, v in enumerate(row):
            if v != 0:
                g[rr + dr][rc + dc] = v


AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_asym":         {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "sym_h":          {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "sym_w":          {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=3, exclude={0})
    g = full_grid(h, w, 0)
    sh = int(overrides.get("sym_h", rng.randint(3, 4)))
    sw_raw = overrides.get("sym_w")
    sw = int(sw_raw) if sw_raw is not None else rng.choice([3, 5])
    sym = _make_sym_block(rng, palette[0], sh=sh, sw=sw)
    sh, sw = len(sym), len(sym[0])
    rr = rng.randint(1, h - sh - 1)
    rc = rng.randint(1, w - sw - 1)
    _paint(g, sym, rr, rc)
    sym_size = sum(1 for row in sym for v in row if v != 0)
    n_asym = int(overrides.get("n_asym", 2))
    placed = 0
    for _ in range(40):
        if placed >= n_asym:
            break
        ablock = _make_asym_block(rng, rng.choice(palette[1:]))
        ah, aw = len(ablock), len(ablock[0])
        a_size = sum(1 for row in ablock for v in row if v != 0)
        if a_size >= sym_size:
            continue
        rr2 = rng.randint(0, h - ah)
        rc2 = rng.randint(0, w - aw)
        if not _can_place(g, ah, aw, rr2, rc2):
            continue
        _paint(g, ablock, rr2, rc2)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "all_asym":
        ablock = _make_asym_block(rng, 2)
        _paint(g, ablock, 3, 3)
        ablock2 = _make_asym_block(rng, 3)
        _paint(g, ablock2, 8, 8)
        return g
    if name == "no_objects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
