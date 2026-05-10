"""Generator for arc_puzzle_bank_eighth_21_bundle:hard_56_frame_transform_gallery.

Rule: 4 hollow 5x6 color-8 frames arranged in a 2x2 grid; each contains a
small motif inside in some non-{0,8} color. Output transforms motifs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_motifs (no interior motifs → rule's per-panel
transform has nothing to operate on, output frames-only), all_same_motif
(all 4 panels share a motif → no per-panel contrast in transform),
single_cell_motifs (each motif is one cell → rotations/flips collapse,
rule's transform is invisible).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "efb13f46eb7a"
VERSION = "1.1.0"
TASK_ID = "efb13f46eb7a"

SUMMARY = "4 hollow 5x6 8-frames in 2x2 layout; each with small interior motif."

INVARIANTS = [
    "background is 0",
    "exactly 4 hollow 5x6 color-8 frames in a 2x2 layout",
    "each frame has 1 small interior motif in some non-{0,8} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_motifs", "all_same_motif", "single_cell_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..14", "valid": "13..16"},
    "grid_w":         {"type": "int", "default": "rng 14..14", "valid": "13..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "four_frames_2x2",
                       "valid": "four_frames_2x2"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def _draw_frame(g, r0, c0, fh, fw):
    for c in range(c0, c0 + fw):
        g[r0][c] = 8
        g[r0 + fh - 1][c] = 8
    for r in range(r0, r0 + fh):
        g[r][c0] = 8
        g[r][c0 + fw - 1] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    h = ctx.draw_int("grid_h", 14, 14)
    w = ctx.draw_int("grid_w", 14, 14)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    fh, fw = 5, 6
    positions = [(1, 1), (1, 8), (8, 1), (8, 8)]
    for r0, c0 in positions:
        _draw_frame(g, r0, c0, fh, fw)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        cells = _build_motif(rng, rng.randint(2, 4))
        rs = [r for r, _ in cells]; cs_ = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs_) - min(cs_) + 1
        for _ in range(40):
            ir = rng.randint(r0 + 1, r0 + fh - sh - 1)
            ic = rng.randint(c0 + 1, c0 + fw - sw - 1)
            ok = True
            for r, c in cells:
                if g[ir + r - min(rs)][ic + c - min(cs_)] != 0:
                    ok = False; break
            if ok:
                for r, c in cells:
                    g[ir + r - min(rs)][ic + c - min(cs_)] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    fh, fw = 5, 6
    positions = [(1, 1), (1, 8), (8, 1), (8, 8)]
    for r0, c0 in positions:
        _draw_frame(g, r0, c0, fh, fw)
    if name == "empty_motifs":
        # No interior motifs — rule's per-panel transform has
        # nothing to operate on; output is frames-only.
        return g
    if name == "all_same_motif":
        # All 4 panels share an identical motif → no per-panel
        # contrast in the transform output.
        for r0, c0 in positions:
            for dr, dc in [(1, 1), (1, 2), (2, 2)]:
                g[r0 + dr][c0 + dc] = 3
        return g
    if name == "single_cell_motifs":
        # Each motif is one cell — rotations/flips collapse;
        # rule's transform is invisible.
        for (r0, c0), color in zip(positions, [1, 2, 4, 6]):
            g[r0 + 2][c0 + 2] = color
        return g
    return g
