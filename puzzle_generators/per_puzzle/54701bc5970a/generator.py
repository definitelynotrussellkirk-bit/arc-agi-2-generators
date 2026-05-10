"""Generator for 18b:m123 — select reflection match and recolor.

Rule: a color-1 prototype shape; among color-2 shapes, find one whose
normalized binary equals the prototype under any of {identity, flip-lr,
flip-ud, rotate-180}. Recolor that shape to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype (no color-1 shape → rule's prototype
selector returns nothing), no_match (prototype present but no
reflection-equivalent color-2 shape → rule's match selector finds
nothing), tied_match (≥2 color-2 shapes are reflection-equivalent →
"the match" is ambiguous, tie-break decides).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "54701bc5970a"
VERSION = "1.1.0"
TASK_ID = "54701bc5970a"
SUMMARY = "1 color-1 prototype + 2-3 color-2 shapes; one matches prototype under reflection."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 prototype shape",
    "2-3 color-2 shapes; exactly one matches prototype under {id, flip-lr, flip-ud, rotate-180}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "prototype_plus_candidates",
                          "valid": "prototype_plus_candidates"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def _flip_lr(shape):
    cs = [c for _, c in shape]
    w = max(cs) + 1
    return sorted([(r, w - 1 - c) for r, c in shape])


def _flip_ud(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(h - 1 - r, c) for r, c in shape])


def _rotate_180(shape):
    return _flip_lr(_flip_ud(shape))


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 0)],
    ]
    proto = rng.choice(base_shapes)
    transformed = rng.choice([proto, _flip_lr(proto), _flip_ud(proto), _rotate_180(proto)])
    other = rng.choice([s for s in base_shapes if s != proto])
    _place(g, rng, proto, 1)
    _place(g, rng, transformed, 2)
    _place(g, rng, other, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_prototype":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][6 + dc] = 2
        return g
    if name == "no_match":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[5 + dr][6 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1), (1, 2)]:
            g[7 + dr][2 + dc] = 2
        return g
    if name == "tied_match":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][6 + dc] = 2
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[6 + dr][2 + dc] = 2
        return g
    return g
