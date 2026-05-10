"""Generator for 6c434453.

Rule: where 3x3 has 8 ones around 0 center, set corners to 0, plus to 2.

Combinatorial axes (8): grid_h/w, n_rings, n_distractors, position_bias,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: solid_block, no_rings, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1279f507a3eb"
VERSION = "1.1.0"
TASK_ID = "1279f507a3eb"
SUMMARY = "1-2 3x3 hollow-ring patterns of 1s plus distractor cells."

INVARIANTS = [
    "1-2 3x3 hollow rings of 1s",
    "rings well-separated (>=4 cells apart)",
    "scattered 1-cells elsewhere as distractors (don't form rings)",
]

POSITION_BIASES = ("scattered", "centered", "corners", "spread")
DEGENERATE_TEXTURES = ("solid_block", "no_rings", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "n_rings":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_distractors":  {"type": "int", "default": "rng 2..4", "valid": "0..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 6, 8
        nr_lo, nr_hi = 1, 1
        nd_lo, nd_hi = 0, 2
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
        nr_lo, nr_hi = 2, 3
        nd_lo, nd_hi = 3, 6
    else:
        h_lo, h_hi = 8, 12
        nr_lo, nr_hi = 1, 2
        nd_lo, nd_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_rings = int(overrides.get("n_rings",
                                ctx.draw_int("n_rings", nr_lo, nr_hi)))
    n_rings = max(1, min(3, n_rings))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed = []
    for _ in range(n_rings * 30):
        if len(placed) >= n_rings:
            break
        if bias == "centered":
            r0 = max(1, h // 2 - 1)
            c0 = max(1, w // 2 - 1)
        elif bias == "corners":
            r0 = rng.choice([1, h - 4])
            c0 = rng.choice([1, w - 4])
        elif bias == "spread":
            r0 = rng.randint(1, max(1, h - 4))
            c0 = rng.randint(1, max(1, w - 4))
        else:
            r0 = rng.randint(1, max(1, h - 4))
            c0 = rng.randint(1, max(1, w - 4))
        if any(abs(r0 - pr) < 5 and abs(c0 - pc) < 5 for pr, pc in placed):
            continue
        for dr in range(3):
            for dc in range(3):
                if dr == 1 and dc == 1:
                    continue
                g[r0 + dr][c0 + dc] = 1
        placed.append((r0, c0))
    nd = int(overrides.get("n_distractors",
                           ctx.draw_int("n_distractors", nd_lo, nd_hi)))
    nd = max(0, min(8, nd))
    for _ in range(nd):
        for _ in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0 and all(abs(r - pr) > 4 or abs(c - pc) > 4
                                     for pr, pc in placed):
                g[r][c] = 1
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "solid_block":
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = 1
        return g
    if name == "no_rings":
        for _ in range(6):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
