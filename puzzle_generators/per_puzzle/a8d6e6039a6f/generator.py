"""Generator for arc_puzzle_bank_21_set23_bundle:hard_p07 — sel + transform + frame.

Rule: (0, 0)=sel color, (0, w-1)=transform code, (h-1, 0)=frame color. Find an
object in sel color; transform; center-place into the frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchors (corner cells empty → no sel/code/frame
identifiers); no_sel_motif (anchors set but no body shape in sel
color → nothing to transform); no_frame (anchors + sel object but no
hollow frame → no destination).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a8d6e6039a6f"
VERSION = "1.1.0"
TASK_ID = "a8d6e6039a6f"

SUMMARY = "Corner anchors hold sel/code/frame-color; body has a hollow frame + sel-colored object."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds sel color, (0, w-1) holds transform code (1..6), (h-1, 0) holds frame color",
    "body has 1 hollow rectangular frame in frame-color and 1 small object in sel-color",
    "the object's bbox fits inside the frame's interior",
    "frame and object are isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchors", "no_sel_motif", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "corner_anchors_with_frame",
                          "valid": "corner_anchors_with_frame"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    rng = ctx.draw_rng("layout")

    sel_color, frame_color = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        g[0][0] = sel_color
        g[0][w - 1] = rng.randint(1, 6)
        g[h - 1][0] = frame_color
        fh, fw = rng.choice([(5, 5), (5, 6), (6, 5), (5, 7)])
        placed_f = False
        for _ in range(120):
            r0 = rng.randint(2, h - fh - 1); c0 = rng.randint(2, w - fw - 1)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, frame_color)
            placed_f = True; break
        if not placed_f:
            continue
        cells = [(0, 0)]; seen = {(0, 0)}
        target = rng.randint(2, 4)
        while len(cells) < target:
            r, c = rng.choice(cells)
            dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            nr, nc = r + dr, c + dc
            if (nr, nc) not in seen:
                cells.append((nr, nc)); seen.add((nr, nc))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1
        sw = max(cs) - min(cs) + 1
        placed_o = False
        for _ in range(120):
            r0 = rng.randint(2, h - sh - 2); c0 = rng.randint(2, w - sw - 2)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = sel_color
            placed_o = True; break
        if placed_o:
            return g
    raise ValueError("could not realize set17 p02 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # No corner cells — no sel/code/frame identifiers.
        draw_frame(g, 3, 3, 7, 8, 5)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][11 + dc] = 4
        return g
    if name == "no_sel_motif":
        # Anchors + frame but no body shape in sel color — nothing to transform.
        g[0][0] = 4
        g[0][w - 1] = 2
        g[h - 1][0] = 5
        draw_frame(g, 3, 3, 7, 8, 5)
        return g
    if name == "no_frame":
        # Anchors + sel-color object but no hollow frame — no destination.
        g[0][0] = 4
        g[0][w - 1] = 2
        g[h - 1][0] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 4
        return g
    return g
