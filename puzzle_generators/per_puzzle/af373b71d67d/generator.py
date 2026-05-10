"""Generator for v2_meta_puzzles:H6 — rotate motif inside frame.

Rule: a hollow color-7 frame contains a color-3 motif inside; output
rotates the motif 90° relative to its bbox (still inside the frame).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame (no color-7 frame → rule has no container);
no_motif (frame present but no color-3 motif → rule has nothing
to rotate); rot_symmetric_motif (motif invariant under 90° → no
visible effect from the rotation).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "af373b71d67d"
VERSION = "1.1.0"
TASK_ID = "af373b71d67d"

SUMMARY = "Color-3 motif outside grid + 1 hollow color-7 frame elsewhere."

INVARIANTS = [
    "background is 0",
    "exactly one connected color-3 motif (3-5 cells)",
    "exactly one hollow color-7 frame (≥4×4) at a different position",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_motif", "rot_symmetric_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "motif_top_left_frame_bottom_right",
                          "valid": "motif_top_left_frame_bottom_right"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
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


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = _build_motif(rng, rng.randint(3, 4))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, max(0, h // 2 - sh - 1))
            c0 = rng.randint(0, max(0, w // 2 - sw - 1))
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = 3
            placed = True; break
        if not placed:
            continue
        for _ in range(80):
            fh = 4; fw = 4
            r0 = rng.randint(h // 2, h - fh); c0 = rng.randint(w // 2, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 7)
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # No color-7 frame — rule has no container.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 3
        return g
    if name == "no_motif":
        # Frame present but no motif inside — rule has nothing to rotate.
        draw_frame(g, 4, 7, 7, 10, 7)
        return g
    if name == "rot_symmetric_motif":
        # 2x2 solid square is invariant under 90° rotation.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 3
        draw_frame(g, 4, 7, 7, 10, 7)
        return g
    return g
