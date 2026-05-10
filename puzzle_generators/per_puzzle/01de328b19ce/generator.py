"""Generator for arc_puzzle_bank_21_set20_bundle:hard_p07 — rotate-and-stamp by anchor.

Rule: a color-6 base shape; single-cell anchors in colors {1, 2, 3, 4} encode
rotation. For each anchor, rotate base by its anchor color, stamp it centered
at the anchor's position.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_base (no color-6 shape → rule's base-shape selector
returns nothing; nothing to stamp), no_anchors (base present but no
{1,2,3,4} anchors → rule has no stamp positions; output equals input),
rot_symmetric_base (base is rotationally symmetric → all 4 rotations
produce identical stamps; rotation key has no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01de328b19ce"
VERSION = "1.1.0"
TASK_ID = "01de328b19ce"

SUMMARY = "1 color-6 base shape + 2-3 single-cell anchors in colors {1, 2, 3, 4}."

INVARIANTS = [
    "background is 0",
    "exactly one color-6 base component (3-5 cells)",
    "2-3 single-cell anchors in distinct colors from {1, 2, 3, 4}",
    "base is isolated from anchors and anchors from each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_base", "no_anchors", "rot_symmetric_base")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_anchors":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "base_plus_rotation_anchors",
                          "valid": "base_plus_rotation_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_anchors = ctx.draw_int("n_anchors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_anchors = ctx.draw_int("n_anchors", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_anchors = ctx.draw_int("n_anchors", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = [(0, 0)]; seen = {(0, 0)}
        target = rng.randint(3, 5)
        while len(cells) < target:
            r, c = rng.choice(cells)
            dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            nr, nc = r + dr, c + dc
            if (nr, nc) not in seen:
                cells.append((nr, nc)); seen.add((nr, nc))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1
        sw = max(cs) - min(cs) + 1
        placed_b = False
        for _ in range(80):
            r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = 6
            placed_b = True
            break
        if not placed_b:
            continue
        anchor_colors = rng.sample([1, 2, 3, 4], n_anchors)
        placed = []
        ok = True
        for color in anchor_colors:
            placed_a = False
            for _ in range(120):
                r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
                if g[r][c] != 0: continue
                if any(abs(r - pr) + abs(c - pc) < 4 for pr, pc in placed): continue
                g[r][c] = color
                placed.append((r, c))
                placed_a = True; break
            if not placed_a:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_p04 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_base":
        # No color-6 shape — rule's base-shape selector finds nothing.
        g[3][3] = 1
        g[6][8] = 2
        return g
    if name == "no_anchors":
        # Base present but no anchors — rule has no stamp positions.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 6
        return g
    if name == "rot_symmetric_base":
        # Base is rotationally symmetric (2x2) — all rotations produce
        # identical stamps; rotation key has no visible contrast.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 6
        g[6][3] = 1
        g[7][9] = 2
        return g
    return g
