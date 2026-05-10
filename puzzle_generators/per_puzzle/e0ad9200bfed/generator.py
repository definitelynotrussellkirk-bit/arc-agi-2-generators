"""Generator for 4b:hard_23 — make transform strip from template and keys.

Rule: template = color-1 multi-cell shape. keys = scattered cells
with values in {2,3,4,5}, sorted by column. For each key, transform
template by the key's value (2=identity, 3=CW, 4=180, 5=flip-lr),
recolor to key's color. Output is hpack-top of these strips.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-1 shape → rule has no source);
no_keys (template present but no {2,3,4,5} keys → rule's strip
list is empty); rot_symmetric_template (template invariant under
all 4 rotations + flips → all key transforms produce identical
strips, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0ad9200bfed"
VERSION = "1.1.0"
TASK_ID = "e0ad9200bfed"

SUMMARY = "1 color-1 template + 2-4 scattered key cells in {2, 3, 4, 5}."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 multi-cell template",
    "2-4 isolated single-cell keys with values in {2, 3, 4, 5}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_keys", "rot_symmetric_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "template_plus_scattered_keys",
                          "valid": "template_plus_scattered_keys"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    placed = False
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = 1
        placed = True; break
    if not placed:
        raise ValueError("could not place template")
    n_keys = rng.randint(2, 4)
    placed_keys = 0
    attempts = 0
    while placed_keys < n_keys and attempts < 80:
        attempts += 1
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0 or _too_close(g, r, c): continue
        g[r][c] = rng.choice([2, 3, 4, 5])
        placed_keys += 1
    if placed_keys < n_keys:
        raise ValueError(f"could only place {placed_keys}/{n_keys} keys")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-1 template — rule has no source to transform.
        g[3][3] = 2; g[5][7] = 3; g[7][11] = 4
        return g
    if name == "no_keys":
        # Template present but no {2,3,4,5} keys — strip list is empty.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        return g
    if name == "rot_symmetric_template":
        # 2x2 solid square is invariant under rotations + flips.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 1
        g[5][7] = 2; g[7][9] = 3; g[9][11] = 4; g[6][12] = 5
        return g
    return g
