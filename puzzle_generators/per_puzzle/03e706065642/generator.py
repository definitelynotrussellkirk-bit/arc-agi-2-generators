"""Generator for arc_additional_puzzles_21_set13_bundle:H89 — symmetry-class equality matrix.

Rule: 3 color-1 hollow rectangular frames each contain a motif. Classify each
binary-cropped motif by symmetry (0=none, 1=lr only, 2=ud only, 3=both).
Output 3×3 matrix: 2 where two motifs share class, 0 otherwise.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-1 frames → rule cannot identify
panels); empty_motifs (frames present but interiors empty → all
classes default to 3 (both), output all-2); all_same_class (every
motif belongs to same class → output all-2, no off-diagonal contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "03e706065642"
VERSION = "1.1.0"
TASK_ID = "03e706065642"

SUMMARY = "3 horizontal color-1 frames; each contains a motif with a known symmetry class."

INVARIANTS = [
    "background is 0",
    "exactly 3 hollow color-1 rectangular 6×6 frames in a horizontal row",
    "each frame interior holds a motif drawn from one of 4 symmetry classes",
    "at least 2 motifs share a class (so output has off-diagonal 2s) and at least one differs (so 0s)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "empty_motifs", "all_same_class")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_n":           {"type": "int", "default": "rng 6..7", "valid": "5..8"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "three_horizontal_frames",
                          "valid": "three_horizontal_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_MOTIFS = {
    0: [
        [(0, 0), (0, 1), (1, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    1: [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
    ],
    2: [
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    ],
    3: [
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
        [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)],
    ],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        fn = ctx.draw_int("frame_n", 6, 6)
    elif difficulty == "hard":
        fn = ctx.draw_int("frame_n", 7, 7)
    else:
        fn = ctx.draw_int("frame_n", 6, 7)
    rng = ctx.draw_rng("layout")
    inner = fn - 2
    h = fn + 2
    gap = 2
    w = fn * 3 + gap * 2 + 2

    for outer in range(40):
        g = full_grid(h, w, 0)
        anchors = []
        for i in range(3):
            ar = 1
            ac = 1 + i * (fn + gap)
            anchors.append((ar, ac))
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)

        repeated_class = rng.choice([0, 1, 2, 3])
        other_class = rng.choice([c for c in [0, 1, 2, 3] if c != repeated_class])
        layout = [repeated_class, repeated_class, other_class]
        rng.shuffle(layout)
        classes = layout

        ok = True
        color_inner = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        for (ar, ac), cls in zip(anchors, classes):
            motif = rng.choice(_MOTIFS[cls])
            mh = max(r for r, _ in motif) + 1
            mw = max(c for _, c in motif) + 1
            if mh > inner or mw > inner:
                ok = False
                break
            dr = (inner - mh) // 2
            dc = (inner - mw) // 2
            for r, c in motif:
                g[ar + 1 + dr + r][ac + 1 + dc + c] = color_inner
        if ok:
            return g
    raise ValueError("could not realize 3-symmetry-class layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    fn = 6
    h = fn + 2
    gap = 2
    w = fn * 3 + gap * 2 + 2
    g = full_grid(h, w, 0)
    anchors = [(1, 1 + i * (fn + gap)) for i in range(3)]
    if name == "no_frames":
        # No color-1 frames — rule cannot identify panels.
        for ar, ac in anchors:
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
                g[ar + 2 + dr][ac + 2 + dc] = 4
        return g
    if name == "empty_motifs":
        # Frames present but interiors empty.
        for ar, ac in anchors:
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)
        return g
    if name == "all_same_class":
        # Every motif is class 3 (bisymmetric plus) — output all-2 off-diag.
        for ar, ac in anchors:
            draw_frame(g, ar, ac, ar + fn - 1, ac + fn - 1, 1)
            for dr, dc in _MOTIFS[3][0]:
                g[ar + 2 + dr][ac + 2 + dc] = 4
        return g
    return g
