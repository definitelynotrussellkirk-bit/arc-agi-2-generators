"""Generator for puzzle 9edfc990.

Rule: 0-components touching a 1-cell get filled with 1; isolated 0
components stay 0.

Combinatorial axes (8): grid_h/w, n_holes, hole_size_kind,
hole_position_kind, palette_kind, n_isolated_holes, anchor_corner,
asymmetry_force.
Degenerates: no_holes, all_holes, single_hole.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be05cee2806f"
VERSION = "1.1.0"
TASK_ID = "be05cee2806f"
SUMMARY = "Blue walls + 0-holes; rule absorbs holes touching walls into 1."

INVARIANTS = [
    "non-bg color is exclusively blue(1)",
    ">=2 distinct 0-cell components",
    ">=1 0-component touches a 1-cell",
    "1-walls form the dominant pattern (carve holes from all-1)",
]

HOLE_SIZE_KINDS = ("small", "medium", "large", "varied")
POSITION_BIAS = ("center", "spread", "edge", "corners")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "single_hole")
HELPFUL_TEXTURES = HOLE_SIZE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":            {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_holes":           {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "hole_size_kind":    {"type": "str", "default": "rng helpful",
                          "valid": "|".join(HOLE_SIZE_KINDS)},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "n_isolated_holes":  {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for hole_size_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 15, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_holes = int(overrides.get("n_holes",
                                ctx.draw_int("n_holes", 2, 4)))
    n_holes = max(1, min(6, n_holes))
    size_kind = (overrides.get("texture") or
                 overrides.get("hole_size_kind")
                 or ctx.draw_choice("hole_size_kind",
                                    list(HOLE_SIZE_KINDS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         list(POSITION_BIAS)))
    g = full_grid(h, w, 1)
    placed = []
    for _ in range(n_holes * 5):
        if len(placed) >= n_holes:
            break
        hh, hw = _hole_dims(size_kind, rng)
        for _try in range(20):
            r0, c0 = _pick_pos(bias, h, w, hh, hw, rng)
            if r0 < 1 or c0 < 1 or r0 + hh > h - 1 or c0 + hw > w - 1:
                continue
            if any(abs(r0 - pr) <= max(hh, prh) + 1 and
                   abs(c0 - pc) <= max(hw, pcw) + 1
                   for pr, pc, prh, pcw in placed):
                continue
            for r in range(r0, r0 + hh):
                for c in range(c0, c0 + hw):
                    g[r][c] = 0
            placed.append((r0, c0, hh, hw))
            break
    if not placed:
        # Force one hole
        if h >= 4 and w >= 4:
            for r in range(2, 4):
                for c in range(2, 4):
                    g[r][c] = 0
    return g


def _hole_dims(kind, rng):
    if kind == "small":
        return 2, 2
    if kind == "medium":
        return rng.randint(2, 3), rng.randint(2, 3)
    if kind == "large":
        return rng.randint(3, 4), rng.randint(3, 4)
    return rng.randint(2, 4), rng.randint(2, 4)


def _pick_pos(bias, h, w, hh, hw, rng):
    if bias == "center":
        return max(1, (h - hh) // 2), max(1, (w - hw) // 2)
    if bias == "edge":
        choices = [(1, 1), (1, w - hw - 1), (h - hh - 1, 1),
                   (h - hh - 1, w - hw - 1)]
        return rng.choice(choices)
    if bias == "corners":
        return rng.choice([(1, 1), (1, w - hw - 1),
                           (h - hh - 1, 1),
                           (h - hh - 1, w - hw - 1)])
    return rng.randint(1, h - hh - 1), rng.randint(1, w - hw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 1)
    if name == "no_holes":
        return g
    if name == "all_holes":
        return [[0] * w for _ in range(h)]
    if name == "single_hole":
        if h >= 4 and w >= 4:
            for r in range(2, 4):
                for c in range(2, 4):
                    g[r][c] = 0
        return g
    return g
