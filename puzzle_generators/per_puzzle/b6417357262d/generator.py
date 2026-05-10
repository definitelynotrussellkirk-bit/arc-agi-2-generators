"""Generator for 5b:hard_31 — boolean template combine by key.

Rule: a key cell has value 4 (OR), 6 (AND), or 8 (XOR). Two shapes
(color 2 and color 3) get cell-wise combined per key into color 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key (no isolated key cell → rule's op-selector returns
nothing), identical_shapes (cells_a == cells_b → AND==OR==both, XOR
empty; ops collapse), unequal_bboxes (color-2 and color-3 shapes have
different bbox dims → rule's "equal-bbox" precondition fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b6417357262d"
VERSION = "1.1.0"
TASK_ID = "b6417357262d"
SUMMARY = "1 op-key (4/6/8) + 1 color-2 shape + 1 color-3 shape, equal bbox dims."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell with value in {4, 6, 8}",
    "one color-2 shape and one color-3 shape with equal bbox dims",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "identical_shapes", "unequal_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape_h":           {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "shape_w":           {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "key_plus_two_shapes",
                          "valid": "key_plus_two_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
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
        sh = ctx.draw_int("shape_h", 3, 3)
        sw = ctx.draw_int("shape_w", 3, 3)
    elif difficulty == "hard":
        sh = ctx.draw_int("shape_h", 4, 4)
        sw = ctx.draw_int("shape_w", 4, 4)
    else:
        sh = ctx.draw_int("shape_h", 3, 4)
        sw = ctx.draw_int("shape_w", 3, 4)
    rng = ctx.draw_rng("layout")
    h = sh * 2 + 4; w = sw * 2 + 4
    for _ in range(40):
        g = full_grid(h, w, 0)
        op = rng.choice([4, 6, 8])
        for _ in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            bad = False
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                        bad = True; break
                if bad: break
            if bad: continue
            g[r][c] = op; break
        cells_a = {(0, 0)}
        target = rng.randint(max(3, sh * sw // 2), sh * sw)
        attempts = 0
        while len(cells_a) < target and attempts < 100:
            attempts += 1
            r, c = rng.choice(list(cells_a))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < sh and 0 <= nc < sw and (nr, nc) not in cells_a:
                    cells_a.add((nr, nc))
                    if len(cells_a) >= target: break
        cells_b = {(0, 0)}
        target = rng.randint(max(3, sh * sw // 2), sh * sw)
        attempts = 0
        while len(cells_b) < target and attempts < 100:
            attempts += 1
            r, c = rng.choice(list(cells_b))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < sh and 0 <= nc < sw and (nr, nc) not in cells_b:
                    cells_b.add((nr, nc))
                    if len(cells_b) >= target: break
        if cells_a == cells_b: continue
        ar, ac = 1, 1
        br, bc = sh + 3, sw + 3
        if not _free(g, ar, ac, ar + sh - 1, ac + sw - 1) or not _free(g, br, bc, br + sh - 1, bc + sw - 1):
            continue
        for dr, dc in cells_a: g[ar + dr][ac + dc] = 2
        for dr, dc in cells_b: g[br + dr][bc + dc] = 3
        return g
    return g


def _draw_from_degenerate(name, rng):
    sh, sw = 3, 3
    h = sh * 2 + 4
    w = sw * 2 + 4
    g = full_grid(h, w, 0)
    if name == "no_key":
        # No isolated key cell — rule's op-selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]: g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    if name == "identical_shapes":
        # cells_a == cells_b — all ops collapse.
        cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]
        g[8][1] = 4
        for dr, dc in cells: g[1 + dr][1 + dc] = 2
        for dr, dc in cells: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    if name == "unequal_bboxes":
        # A is 3x3, B is 2x2 — equal-bbox precondition fails.
        g[8][1] = 6
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]: g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    return g
