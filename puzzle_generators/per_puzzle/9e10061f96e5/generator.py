"""Generator for arc_additional_puzzles_21_set17_bundle:H118 — transform-equivalence matrix.

Rule: 3 panels separated by single full-zero columns. Each panel holds a small
non-zero shape. Output N×N matrix: diagonal=5, off-diagonal=2 if shapes are
dihedrally equivalent (under rotations and reflections), else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_panels (no shapes → matrix is empty); single_panel
(only 1 → matrix is 1x1 with value 5, no off-diag contrast);
all_dihedral_equivalent (all 3 shapes belong to same dihedral class
→ matrix all 5/2, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e10061f96e5"
VERSION = "1.1.0"
TASK_ID = "9e10061f96e5"

SUMMARY = "3 panels split by full-zero columns; output 3×3 dihedral equivalence matrix."

INVARIANTS = [
    "background is 0",
    "exactly 3 panels separated by full-height all-zero columns",
    "each panel contains a non-trivial shape in some non-bg color",
    "panels are NxM (small) with at least one non-zero cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_panels", "single_panel", "all_dihedral_equivalent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_n":           {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_panels_one_dihedral_pair",
                          "valid": "three_panels_one_dihedral_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
]


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("panel_n", 3, 3)
    elif difficulty == "hard":
        n = ctx.draw_int("panel_n", 4, 4)
    else:
        n = ctx.draw_int("panel_n", 3, 4)
    rng = ctx.draw_rng("layout")

    base = rng.choice(_SHAPES)
    rot = base
    for _ in range(rng.randint(1, 3)):
        rot = _rotate_cw(rot)
    other = rng.choice([s for s in _SHAPES if s != base])
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], 3)
    shapes_colors = list(zip([base, rot, other], palette))
    rng.shuffle(shapes_colors)

    panel_widths = []
    panel_heights = []
    panel_grids = []
    for shape, color in shapes_colors:
        sh = max(r for r, _ in shape) + 1
        sw = max(c for _, c in shape) + 1
        gp = [[0] * sw for _ in range(sh)]
        for dr, dc in shape:
            gp[dr][dc] = color
        panel_widths.append(sw)
        panel_heights.append(sh)
        panel_grids.append(gp)
    h = max(panel_heights)
    w = sum(panel_widths) + 2

    g = full_grid(h, w, 0)
    col = 0
    for i, gp in enumerate(panel_grids):
        sw = panel_widths[i]
        sh = panel_heights[i]
        for r in range(sh):
            for c in range(sw):
                g[r][col + c] = gp[r][c]
        col += sw + 1
    return g


def _draw_from_degenerate(name, rng):
    if name == "no_panels":
        return full_grid(4, 10, 0)
    if name == "single_panel":
        g = full_grid(3, 4, 0)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[dr][dc] = 4
        return g
    if name == "all_dihedral_equivalent":
        # Three rotations of the same L-tromino in distinct colors — output all-5/2.
        g = full_grid(3, 8, 0)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[dr][dc] = 4
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[dr][3 + dc] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[dr][6 + dc] = 7
        return g
    return full_grid(3, 8, 0)
