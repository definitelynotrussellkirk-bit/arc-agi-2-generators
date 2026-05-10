"""Generator for arc_puzzle_bank_21_set16_bundle:hard_p04 — guide-shape selects stamp.

Rule: a color-2 guide shape; color-9 anchors; non-{2, 9} candidate shapes.
Find the candidate whose shape matches a dihedral variant of the guide;
stamp that candidate's crop at every anchor (using the candidate's color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide (no color-2 shape → rule has no template);
no_match (guide + candidates but none matches → selector returns
nothing); no_anchors (guide + match but no color-9 anchors → no
stamp destinations).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e4c956a370d4"
VERSION = "1.1.0"
TASK_ID = "e4c956a370d4"

SUMMARY = "Color-2 guide + color-9 anchor cells + 2 non-{2,9} candidates; one matches guide."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 guide shape (3-5 cells)",
    "1-2 color-9 anchor cells",
    "exactly 2 non-{2, 9} candidate components in distinct colors",
    "exactly one candidate is dihedrally-equivalent to the guide",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_match", "no_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "guide_anchors_two_candidates",
                          "valid": "guide_anchors_two_candidates"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")

    guide = rng.choice(_SHAPES)
    rotated = guide
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other = rng.choice([s for s in _SHAPES if s != guide])
    cand_colors = rng.sample([1, 3, 4, 5, 6, 7, 8], 2)
    n_anchors = rng.randint(1, 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        sh = max(r for r, _ in guide) + 1
        sw = max(c for _, c in guide) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for dr, dc in guide:
                g[r0 + dr][c0 + dc] = 2
            placed = True; break
        if not placed: continue
        for shape, color in zip([rotated, other], cand_colors):
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed_a = False
            for _ in range(80):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed_a = True; break
            if not placed_a:
                ok = False; break
        if not ok:
            continue
        for _ in range(n_anchors):
            for _t in range(80):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if r + 3 >= h or c + 3 >= w: continue
                g[r][c] = 9
                break
        return g
    raise ValueError("could not realize hard_p04 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # No color-2 guide — rule has no template.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][8 + dc] = 5
        g[6][3] = 9
        return g
    if name == "no_match":
        # Guide is L-tromino, candidates are 2x2 squares (different class).
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][8 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][8 + dc] = 5
        g[6][3] = 9
        return g
    if name == "no_anchors":
        # Guide + matching candidate but no color-9 anchors.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[2 + dr][8 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][8 + dc] = 5
        return g
    return g
