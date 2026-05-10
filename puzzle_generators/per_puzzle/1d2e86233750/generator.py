"""Generator for arc_additional_puzzles_21_set12_bundle:H79 — infer A→B, apply to C.

Rule: 3 rectangular color-9 frames hold inner patterns A, B, C (sorted left-to-right
by left column). Find transform t ∈ {1=cw, 2=180, 3=flip-lr, 4=flip-ud} such that
t(A) == B, then apply t to C as output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-9 frames → rule's panel selector
fails), identity_transform (A == B → t is identity, output = C),
no_C_content (panel C is empty → rule's t(C) is empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1d2e86233750"
VERSION = "1.1.0"
TASK_ID = "1d2e86233750"

SUMMARY = "3 rectangular 9-frames; inner of B = transform(A); output = transform(C)."

INVARIANTS = [
    "background is 0",
    "exactly 3 rectangular color-9 hollow frames; sortable left-to-right by left column",
    "all frames have a square N×N inner region (N in 3..4) so all 4 transforms apply",
    "A and B inners are related by some transform t ∈ {1, 2, 3, 4}",
    "C inner contains a non-trivial shape independent of A/B",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "identity_transform", "no_C_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "inner_n":           {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "three_9_frames",
                          "valid": "three_9_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform(cells, t, n):
    if t == 1: return [(c, n - 1 - r) for r, c in cells]
    if t == 2: return [(n - 1 - r, n - 1 - c) for r, c in cells]
    if t == 3: return [(r, n - 1 - c) for r, c in cells]
    return [(n - 1 - r, c) for r, c in cells]


def _rand_cells(rng, n, k):
    cells = []
    seen = set()
    r0 = rng.randint(0, n - 1); c0 = rng.randint(0, n - 1)
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
        n = ctx.draw_int("inner_n", 3, 3)
    elif difficulty == "hard":
        n = ctx.draw_int("inner_n", 4, 4)
    else:
        n = ctx.draw_int("inner_n", 3, 4)
    rng = ctx.draw_rng("layout")
    frame_size = n + 2
    h = frame_size + 2
    w = 1 + 3 * frame_size + 2 * 1 + 1
    t = rng.randint(1, 4)
    color_a = rng.choice([2, 3, 4, 6, 7, 8])
    color_c = rng.choice([c for c in [2, 3, 4, 6, 7, 8] if c != color_a])

    for outer in range(40):
        g = full_grid(h, w, 0)
        anchors = []
        for i in range(3):
            r1 = 1
            c1 = 1 + i * (frame_size + 1)
            r2 = r1 + frame_size - 1
            c2 = c1 + frame_size - 1
            draw_frame(g, r1, c1, r2, c2, 9)
            anchors.append((r1, c1))

        ka = rng.randint(3, 5)
        cells_a = _rand_cells(rng, n, ka)
        cells_b = _xform(cells_a, t, n)
        if set(cells_a) == set(cells_b):
            continue
        ar, ac = anchors[0]
        for r, c in cells_a:
            g[ar + 1 + r][ac + 1 + c] = color_a
        ar, ac = anchors[1]
        for r, c in cells_b:
            g[ar + 1 + r][ac + 1 + c] = color_a
        kc = rng.randint(3, 5)
        cells_c = _rand_cells(rng, n, kc)
        ar, ac = anchors[2]
        for r, c in cells_c:
            g[ar + 1 + r][ac + 1 + c] = color_c
        return g
    raise ValueError("could not realize 3-frame layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    n = 3
    frame_size = n + 2
    h = frame_size + 2
    w = 1 + 3 * frame_size + 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No color-9 frames — rule's panel selector fails.
        g[2][2] = 4; g[3][3] = 4
        g[2][8] = 4; g[3][9] = 4
        g[2][14] = 6; g[3][15] = 6
        return g
    if name == "identity_transform":
        # A == B → t is identity, output = C.
        for i in range(3):
            r1 = 1
            c1 = 1 + i * (frame_size + 1)
            draw_frame(g, r1, c1, r1 + frame_size - 1, c1 + frame_size - 1, 9)
        # A and B identical: same cells in panel 0 and 1
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[2 + r][2 + c] = 4
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[2 + r][2 + (frame_size + 1) + c] = 4
        for r, c in [(0, 1), (1, 0), (2, 2)]:
            g[2 + r][2 + 2 * (frame_size + 1) + c] = 6
        return g
    if name == "no_C_content":
        # Panel C is empty — rule's t(C) is empty.
        for i in range(3):
            r1 = 1
            c1 = 1 + i * (frame_size + 1)
            draw_frame(g, r1, c1, r1 + frame_size - 1, c1 + frame_size - 1, 9)
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[2 + r][2 + c] = 4
        # B = cw(A): (0,0)→(0,2), (1,0)→(0,1), (1,1)→(1,1)
        for r, c in [(0, 2), (0, 1), (1, 1)]:
            g[2 + r][2 + (frame_size + 1) + c] = 4
        # C empty
        return g
    return g
