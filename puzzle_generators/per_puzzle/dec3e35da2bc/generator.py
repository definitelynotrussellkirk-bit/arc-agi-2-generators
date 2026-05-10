"""Generator for 20b:m137 — match prototype under rotation and recolor.

Rule: prototype at subgrid (0,0)-(4,4); candidate panels at fixed cols
[6, 12, 18] (also rows 0-4). Target color at (5, 0). Find the panel
whose normalized binary matches the prototype under any rotation;
output is that panel's crop, recolored to target.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: rotation_symmetric_proto (prototype invariant under
rotation → all 3 candidates can match, rule's "find the one" is
ambiguous), all_match (every candidate is a rotation of prototype →
selector finds 3 valid panels), no_match (no candidate matches →
selector finds nothing, output undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dec3e35da2bc"
VERSION = "1.1.0"
TASK_ID = "dec3e35da2bc"

SUMMARY = "5x5 prototype at (0,0) + 3 5x5 candidate panels at cols [6,12,18] + target color at (5,0)."

INVARIANTS = [
    "background is 0",
    "grid is 6 rows tall and 23 cols wide",
    "prototype panel at rows 0..4 cols 0..4 (single color)",
    "3 candidate panels at rows 0..4 cols [6..10, 12..16, 18..22]",
    "exactly one candidate is rotation-equivalent to the prototype",
    "the other candidates are different shapes (not rotation-equivalent)",
    "cell (5,0) is the target color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("rotation_symmetric_proto", "all_match", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "fixed_proto_3candidates",
                       "valid": "fixed_proto_3candidates"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "grid_h":         {"type": "int", "default": "6", "valid": "6..6"},
    "grid_w":         {"type": "int", "default": "23", "valid": "23..23"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
    rng = ctx.draw_rng("layout")
    h = 6; w = 23
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
    ]
    proto_shape = rng.choice(base_shapes)
    rotated = proto_shape
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other_choices = [s for s in base_shapes if s != proto_shape]
    others = rng.sample(other_choices, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)
    proto_color = palette[0]
    cand_colors = palette[1:4]
    target_color = palette[4]
    g = full_grid(h, w, 0)
    for dr, dc in proto_shape:
        g[dr][dc] = proto_color
    panel_starts = [6, 12, 18]
    cand_shapes = [rotated] + others
    rng.shuffle(cand_shapes)
    for c0, color, shape in zip(panel_starts, cand_colors, cand_shapes):
        for dr, dc in shape:
            g[dr][c0 + dc] = color
    g[5][0] = target_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 23
    g = full_grid(h, w, 0)
    panel_starts = [6, 12, 18]
    if name == "rotation_symmetric_proto":
        # Prototype is a single cell — invariant under all rotations.
        # All 3 candidates can match; rule's selector is ambiguous.
        proto = [(0, 0)]
        for dr, dc in proto: g[dr][dc] = 1
        for c0, color in zip(panel_starts, [3, 4, 5]):
            for dr, dc in [(0, 0), (1, 0)]:
                g[dr][c0 + dc] = color
        g[5][0] = 7
        return g
    if name == "all_match":
        # Every candidate is a rotation of the prototype — selector
        # finds 3 matches; rule's "the one" branch ambiguous.
        proto = [(0, 0), (0, 1), (1, 0)]
        for dr, dc in proto: g[dr][dc] = 1
        rotations = [proto, _rotate_cw(proto), _rotate_cw(_rotate_cw(proto))]
        for c0, color, shape in zip(panel_starts, [3, 4, 5], rotations):
            for dr, dc in shape:
                g[dr][c0 + dc] = color
        g[5][0] = 7
        return g
    if name == "no_match":
        # No candidate matches the prototype under any rotation —
        # selector finds nothing; output undefined.
        proto = [(0, 0), (0, 1), (1, 0)]
        for dr, dc in proto: g[dr][dc] = 1
        non_matching = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (1, 1), (2, 2), (3, 3)],
        ]
        for c0, color, shape in zip(panel_starts, [3, 4, 5], non_matching):
            for dr, dc in shape:
                if 0 <= dr < h and 0 <= c0 + dc < w:
                    g[dr][c0 + dc] = color
        g[5][0] = 7
        return g
    return g
