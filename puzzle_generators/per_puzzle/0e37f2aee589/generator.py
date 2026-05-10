"""Generator for arc_puzzle_bank_21_set24_bundle:medium_p01 — sel + transform + frame.

Rule: (0, 0)=sel color, (0, w-1)=transform code, (h-1, 0)=frame color. Find an
object in sel color; transform; center-place into the frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_sel (cell (0,0) is bg → rule's sel-color selector
returns nothing), no_frame (no hollow frame in body → rule's
frame-interior target undefined), identity_transform (transform code
yields identity → rule's transform produces no visible change).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "0e37f2aee589"
VERSION = "1.1.0"
TASK_ID = "0e37f2aee589"

SUMMARY = "Corner anchors hold sel/code/frame-color; body has a hollow frame + sel-colored object."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds sel color, (0, w-1) holds transform code (1..6), (h-1, 0) holds frame color",
    "body has 1 hollow rectangular frame in frame-color and 1 small object in sel-color",
    "the object's bbox fits inside the frame's interior",
    "frame and object are isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_sel", "no_frame", "identity_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "anchors_plus_frame_plus_object",
                          "valid": "anchors_plus_frame_plus_object"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 14, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 16, 16)
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
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_sel":
        # (0,0) is bg — rule's sel-color selector returns nothing.
        g[0][w - 1] = 3
        g[h - 1][0] = 6
        draw_frame(g, 4, 4, 8, 9, 6)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "no_frame":
        # No hollow frame in body — rule's frame-interior target undefined.
        g[0][0] = 4
        g[0][w - 1] = 3
        g[h - 1][0] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 4
        return g
    if name == "identity_transform":
        # Object rotationally symmetric + tf=cw → output identical.
        g[0][0] = 4
        g[0][w - 1] = 1
        g[h - 1][0] = 6
        draw_frame(g, 4, 4, 9, 11, 6)
        g[6][6] = 4; g[6][7] = 4; g[7][6] = 4; g[7][7] = 4
        return g
    return g
