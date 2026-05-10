"""Generator for arc_puzzle_bank_21_set13_bundle:hard_m01 — find dihedral match.

Rule: a target shape in color 2; among other candidate components, find the
one whose cropped grid is dihedrally equivalent to the target. Output that
candidate's grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_target (no color-2 shape → rule's target selector
returns nothing), no_match (target present but no candidate is
dihedrally equivalent → rule's match selector finds nothing), tied_match
(≥2 candidates dihedrally equivalent to target → rule's "the matching
candidate" is ambiguous, tie-break decides).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a079fac95996"
VERSION = "1.1.0"
TASK_ID = "a079fac95996"

SUMMARY = "Color-2 target + 2 other candidate shapes; one is dihedrally equivalent."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 target shape",
    "2 other candidate components in distinct non-{0, 2} colors",
    "exactly one candidate is dihedrally equivalent to the target",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "target_plus_dihedral_candidate",
                          "valid": "target_plus_dihedral_candidate"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 14, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")

    target = rng.choice(_SHAPES)
    rotated = target
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other = rng.choice([s for s in _SHAPES if s != target])
    palette = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], 2)
    shapes = [(target, 2), (rotated, palette[0]), (other, palette[1])]
    rng.shuffle(shapes)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for shape, color in shapes:
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(60):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not place 3 shapes in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_target":
        # No color-2 shape — rule's target selector finds nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[6 + dr][8 + dc] = 6
        return g
    if name == "no_match":
        # Target present but no dihedrally equivalent candidate.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2   # L
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[5 + dr][6 + dc] = 4   # H_LINE_3 — different shape class
        for dr, dc in [(0, 0), (1, 0), (1, 1), (1, 2)]:
            g[7 + dr][2 + dc] = 6
        return g
    if name == "tied_match":
        # Two candidates are dihedrally equivalent — match is ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2   # target L
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][6 + dc] = 4   # rotated L
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[7 + dr][2 + dc] = 6   # another rotated L
        return g
    return g
