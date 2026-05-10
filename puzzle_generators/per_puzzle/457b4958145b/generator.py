"""Generator for arc_puzzle_bank_21_set18_bundle:hard_p03 — angular-order pack around hub.

Rule: a color-9 hub cell. Other components are ordered by their angle from
the hub (top, right, bottom, left, then by angular position) and packed
horizontally as crops.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_hub (no color-9 → rule's reference point missing);
no_components (hub but no components → rule has nothing to order);
single_component (only 1 → angular ordering is trivial, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "457b4958145b"
VERSION = "1.1.0"
TASK_ID = "457b4958145b"

SUMMARY = "1 color-9 hub + 3-4 components scattered around it in distinct colors."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 hub cell near grid center",
    "3-4 isolated components in distinct non-{0, 9} colors at different angular positions around the hub",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_hub", "no_components", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "n_components":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "hub_with_angular_components",
                          "valid": "hub_with_angular_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..6"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n = ctx.draw_int("n_components", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        n = ctx.draw_int("n_components", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n = ctx.draw_int("n_components", 3, 4)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n)

    for outer in range(40):
        g = full_grid(h, w, 0)
        hub_r = rng.randint(h // 2 - 1, h // 2 + 1)
        hub_c = rng.randint(w // 2 - 1, w // 2 + 1)
        g[hub_r][hub_c] = 9
        ok = True
        for color in palette:
            shape = rng.choice([
                [(0, 0), (0, 1)],
                [(0, 0), (1, 0)],
                [(0, 0), (0, 1), (1, 0)],
                [(0, 0)],
            ])
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                if abs(r0 - hub_r) + abs(c0 - hub_c) < 3: continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set18 p03 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_hub":
        # No color-9 hub — rule's reference point missing.
        g[2][3] = 4; g[2][10] = 5
        g[8][3] = 6; g[8][10] = 7
        return g
    if name == "no_components":
        # Hub but no components.
        g[5][7] = 9
        return g
    if name == "single_component":
        # Only 1 component — angular ordering trivial.
        g[5][7] = 9
        g[2][3] = 4
        return g
    return g
