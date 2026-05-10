"""Generator for arc_puzzle_bank_21_set23_bundle:hard_p04 — pair frames to solids by size.

Rule: detect rectangular hollow frames and other (non-frame) components.
Sort both by ascending size; place each solid centered in the paired frame's
interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no frames → rule has no chambers);
no_solids (frames but no solids → nothing to place);
tied_sizes (frames or solids of equal size → sort ambiguous, no
unique pairing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "e2051b3f4045"
VERSION = "1.1.0"
TASK_ID = "e2051b3f4045"

SUMMARY = "2 hollow frames + 2 solid components in distinct sizes."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow rectangular frames in distinct colors with distinct interior sizes",
    "exactly 2 solid (filled) components in distinct colors with distinct sizes",
    "frames and solids are 4-conn isolated",
    "each solid fits inside its paired frame's interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_solids", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "two_frames_two_solids",
                          "valid": "two_frames_two_solids"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..6"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 17)
    rng = ctx.draw_rng("layout")

    frame_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    solid_colors = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in frame_colors], 2)
    frame_dims = rng.sample([(4, 4), (5, 5), (4, 5), (5, 4), (4, 6)], 2)
    solid_dims = rng.sample([(2, 2), (2, 3), (3, 2), (3, 3)], 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for color, (fh, fw) in zip(frame_colors, frame_dims):
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - fh)
                c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1):
                    continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, color)
                placed = True; break
            if not placed:
                ok = False; break
        if not ok:
            continue
        for color, (sh, sw) in zip(solid_colors, solid_dims):
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh)
                c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1):
                    continue
                for r in range(sh):
                    for c in range(sw):
                        g[r0 + r][c0 + c] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_p03 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Solids only — no chambers to place into.
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 3
        for r in range(7, 10):
            for c in range(8, 11):
                g[r][c] = 5
        return g
    if name == "no_solids":
        # Frames only — nothing to place.
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 6, 8, 10, 13, 2)
        return g
    if name == "tied_sizes":
        # Two frames same interior size + two solids same size — pairing ambiguous.
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 1, 9, 4, 12, 2)
        for r in range(7, 9):
            for c in range(2, 4):
                g[r][c] = 3
        for r in range(7, 9):
            for c in range(8, 10):
                g[r][c] = 4
        return g
    return g
