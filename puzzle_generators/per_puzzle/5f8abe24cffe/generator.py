"""Generator for arc_additional_puzzles_21_set13_bundle:H86 — A:B::C transform analogy.

Rule: 3 rectangular color-1 frames, sorted by (r1, c1). Inner = crop-to-content
of subgrid inside frame. A→B determines transform code (1..6: identity, cw, 180,
transpose, flip-lr, flip-ud). Apply same transform to C as the output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-1 frames → rule cannot identify
panels); identity_transform (A == B → t = identity, output = C
unchanged); no_C_content (frame C is empty → rule's transform
input is empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5f8abe24cffe"
VERSION = "1.1.0"
TASK_ID = "5f8abe24cffe"

SUMMARY = "3 square color-1 frames; A→B determines transform; output = transform(C-inner)."

INVARIANTS = [
    "background is 0",
    "exactly 3 hollow rectangular color-1 frames, each 5×5",
    "frames are placed in distinct (top-left) positions; sortable by (r1, c1)",
    "frames A and B have inner shapes related by some transform t in {1..6}",
    "frame C has an independent shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "identity_transform", "no_C_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_n":           {"type": "int", "default": "rng 5..6", "valid": "5..7"},
    "transform":         {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_horizontal_frames",
                          "valid": "three_horizontal_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform(cells, t, n):
    if t == 1: return list(cells)
    if t == 2: return [(c, n - 1 - r) for r, c in cells]
    if t == 3: return [(n - 1 - r, n - 1 - c) for r, c in cells]
    if t == 4: return [(c, r) for r, c in cells]
    if t == 5: return [(r, n - 1 - c) for r, c in cells]
    return [(n - 1 - r, c) for r, c in cells]


def _rand_cells(rng, n, k):
    cells = []
    seen = set()
    r0, c0 = rng.randint(0, n - 1), rng.randint(0, n - 1)
    cells.append((r0, c0)); seen.add((r0, c0))
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        fn = ctx.draw_int("frame_n", 5, 5)
    elif difficulty == "hard":
        fn = ctx.draw_int("frame_n", 6, 6)
    else:
        fn = ctx.draw_int("frame_n", 5, 6)
    t = ctx.draw_int("transform", 2, 6)
    rng = ctx.draw_rng("layout")
    inner_n = fn - 2
    h = fn + 2
    w = fn * 3 + 2 * 3

    for outer in range(40):
        g = full_grid(h, w, 0)
        frame_xs = [3, 3 + fn + 3, 3 + 2 * (fn + 3)]
        if frame_xs[-1] + fn - 1 >= w:
            w = frame_xs[-1] + fn + 1
            g = full_grid(h, w, 0)
        anchors = [(1, fx) for fx in frame_xs]
        for ar, ac in anchors:
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)

        ka = rng.randint(3, 5)
        cells_a = _rand_cells(rng, inner_n, ka)
        cells_b = _xform(cells_a, t, inner_n)
        if set(cells_a) == set(cells_b):
            continue

        color_inner = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        color_c = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c != color_inner])
        ar, ac = anchors[0]
        for r, c in cells_a:
            g[ar + 1 + r][ac + 1 + c] = color_inner
        ar, ac = anchors[1]
        for r, c in cells_b:
            g[ar + 1 + r][ac + 1 + c] = color_inner
        ar, ac = anchors[2]
        kc = rng.randint(3, 5)
        cells_c = _rand_cells(rng, inner_n, kc)
        for r, c in cells_c:
            g[ar + 1 + r][ac + 1 + c] = color_c
        return g
    raise ValueError("could not realize 3-frame analogy in 40 attempts")


def _draw_from_degenerate(name, rng):
    fn = 5
    h = fn + 2
    w = fn * 3 + 2 * 3
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No color-1 frames — rule cannot identify panels.
        g[2][3] = 4; g[3][3] = 4; g[3][4] = 4
        g[2][10] = 4; g[3][10] = 4; g[4][10] = 4
        g[2][17] = 5; g[3][17] = 5; g[4][17] = 5
        return g
    if name == "identity_transform":
        # A == B (same shape, no transform) — output = C unchanged.
        for ax_anchor in [(1, 3), (1, 11), (1, 19)]:
            ar, ac = ax_anchor
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)
        # A and B identical
        for r0, c0 in [(0, 0), (1, 0), (1, 1)]:
            g[2 + r0][4 + c0] = 4
            g[2 + r0][12 + c0] = 4
        for r0, c0 in [(0, 0), (0, 1), (1, 0)]:
            g[2 + r0][20 + c0] = 5
        return g
    if name == "no_C_content":
        # Frame C empty — rule's transform input is empty.
        for ax_anchor in [(1, 3), (1, 11), (1, 19)]:
            ar, ac = ax_anchor
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)
        for r0, c0 in [(0, 0), (1, 0), (1, 1)]:
            g[2 + r0][4 + c0] = 4
        for r0, c0 in [(0, 1), (1, 0), (1, 1)]:
            g[2 + r0][12 + c0] = 4
        return g
    return g
