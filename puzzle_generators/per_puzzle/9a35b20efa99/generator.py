"""Generator for arc_puzzle_bank_21_set23_bundle:hard_p06 — anchor + 4 rotations stamped around it.

Rule: a single color-9 anchor cell plus one connected motif in some other
color. Output stamps the motif's 4 rotations into the 4 quadrants around
the anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor (no color-9 cell → rule's anchor selector
returns nothing, no stamping), no_motif (anchor present but no motif →
rule has nothing to rotate-stamp), rot_symmetric_motif (motif is
rotationally symmetric → all 4 rotations identical, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a35b20efa99"
VERSION = "1.1.0"
TASK_ID = "9a35b20efa99"

SUMMARY = "1 color-9 anchor cell + 1 connected motif in a non-{0, 9} color."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 single-cell anchor",
    "exactly one connected motif (3-5 cells) in a non-{0, 9} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_motif", "rot_symmetric_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "anchor_plus_motif_for_4rotations",
                          "valid": "anchor_plus_motif_for_4rotations"},
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


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 14, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(120):
            r0 = rng.randint(0, h // 2 - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = color
            placed = True; break
        if not placed:
            continue
        for _ in range(120):
            r = rng.randint(h // 2, h - 4); c = rng.randint(4, w - 5)
            if g[r][c] != 0: continue
            if any(g[r + dr][c + dc] != 0 for dr in range(-1, 2) for dc in range(-1, 2)
                   if 0 <= r + dr < h and 0 <= c + dc < w):
                continue
            g[r][c] = 9
            return g
    raise ValueError("could not realize set23 hard_p06 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # No color-9 — rule's anchor selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_motif":
        # Anchor present but no motif — rule has nothing to rotate.
        g[6][6] = 9
        return g
    if name == "rot_symmetric_motif":
        # Motif rotationally symmetric (2x2 square) — all 4 rotations
        # identical; no rotational contrast.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 4
        g[6][6] = 9
        return g
    return g
