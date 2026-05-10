"""Generator for arc_additional_puzzle_bank_volume19:M127 — Move 3-shape via 2→1 marker delta.

Rule: dr/dc = (1-marker - 2-marker). Move largest 3-blob by that delta;
output is empty grid + moved cells in 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: zero_delta (1 and 2 coincide → blob doesn't move; output =
input recolored), missing_marker (only 1 OR only 2 → rule's
delta-from-pair selector finds nothing), blob_at_target (delta lands
moved blob inside its original footprint → overlap collapses output).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8738d400fb96"
VERSION = "1.1.0"
TASK_ID = "8738d400fb96"
SUMMARY = "3-blob + 2-marker near it + 1-marker downstream; output moves blob by 2→1 delta and recolors to 8."

INVARIANTS = [
    "background is 0",
    "exactly one 3-blob, one 2-cell, one 1-cell",
    "moved blob fits within grid",
    "no overlap among 3/2/1 placements",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("zero_delta", "missing_marker", "blob_at_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "blob_size":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "blob_plus_two_markers",
                          "valid": "blob_plus_two_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target_lo, target_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        target_lo, target_hi = 4, 5
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
        target_lo, target_hi = 3, 5
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    blob = [(0, 0)]
    target = rng.randint(target_lo, target_hi)
    while len(blob) < target:
        rb, cb = rng.choice(blob)
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = rb + dr, cb + dc
        if (nr, nc) not in blob:
            blob.append((nr, nc))
    minr = min(r for r, _ in blob); minc = min(c for _, c in blob)
    blob = [(r - minr, c - minc) for r, c in blob]
    bh = max(r for r, _ in blob) + 1; bw = max(c for _, c in blob) + 1
    or1 = rng.randint(1, max(1, h // 3))
    oc1 = rng.randint(1, max(1, w // 3))
    used = set()
    for dr, dc in blob:
        used.add((or1 + dr, oc1 + dc))
        g[or1 + dr][oc1 + dc] = 3
    for _ in range(40):
        mr2 = rng.randint(0, or1 - 1) if or1 > 0 else 0
        mc2 = rng.randint(0, oc1 - 1) if oc1 > 0 else 0
        if (mr2, mc2) in used: continue
        if g[mr2][mc2] != 0: continue
        break
    g[mr2][mc2] = 2
    used.add((mr2, mc2))
    for _ in range(40):
        mr1 = rng.randint(mr2 + 2, h - bh)
        mc1 = rng.randint(mc2 + 2, w - bw)
        if (mr1, mc1) in used: continue
        if g[mr1][mc1] != 0: continue
        delta_r = mr1 - mr2; delta_c = mc1 - mc2
        moved = [(or1 + dr + delta_r, oc1 + dc + delta_c) for dr, dc in blob]
        if any(not (0 <= r < h and 0 <= c < w) for r, c in moved): continue
        g[mr1][mc1] = 1
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "zero_delta":
        # 1 and 2 coincide → delta = (0,0); rule moves blob by zero,
        # output equals input recolored — degenerate identity.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 3
        g[6][6] = 2
        g[6][6] = 1  # overwrites — caller's rule may not be defined here
        return g
    if name == "missing_marker":
        # Only the 1 is present (no 2) → delta is undefined; rule's
        # selector returns no pair, no movement.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 3
        g[6][6] = 1
        return g
    if name == "blob_at_target":
        # Delta lands moved-blob on top of original — output overlap
        # collapses, rule's "move and reveal empty" effect is invisible.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 3
        g[2][2] = 2
        g[3][3] = 1  # delta = (1, 1) lands moved blob within 3-region
        return g
    return g
