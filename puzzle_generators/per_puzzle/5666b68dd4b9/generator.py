"""Generator for arc_puzzle_bank_21_set20_bundle:hard_p01 — sel-color + tcode + 8-frame.

Rule: (0, 0) holds the select color and (0, w-1) holds a transform code.
Cells of select color form a sub-shape; transform by code; paste into the
color-8 frame's interior. Other-colored components in the body are
distractors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_sel_color (cell (0,0) is bg → rule's sel-color
selector returns nothing), no_frame (no color-8 frame → rule's
paste-target is undefined), identity_transform (tcode chosen as
identity → rule's transform produces no visible change).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5666b68dd4b9"
VERSION = "1.1.0"
TASK_ID = "5666b68dd4b9"

SUMMARY = "(0,0)=sel-color, (0,w-1)=tcode, body has 8-frame + sel-colored motif + distractors."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds the select color",
    "(0, w-1) holds the transform code (1..6)",
    "body has one hollow color-8 frame and one sel-color motif (and 1-2 distractors)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_sel_color", "no_frame", "identity_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..12", "valid": "9..15"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "n_distract":        {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "sel_tcode_frame_motif_distractors",
                          "valid": "sel_tcode_frame_motif_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n_distract = ctx.draw_int("n_distract", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 14, 14)
        n_distract = ctx.draw_int("n_distract", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
        n_distract = ctx.draw_int("n_distract", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        sel_color = rng.choice([2, 3, 4, 6, 7, 9])
        tcode = rng.randint(1, 6)
        if tcode == sel_color:
            tcode = (tcode % 6) + 1
        g[0][0] = sel_color
        g[0][w - 1] = tcode
        fh, fw = rng.choice([(5, 5), (5, 6), (6, 5), (6, 6)])
        placed_f = False
        for _ in range(120):
            r0 = rng.randint(2, h - fh - 1); c0 = rng.randint(0, w - fw - 1)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 8)
            placed_f = True; break
        if not placed_f:
            continue
        cells = _build_motif(rng, rng.randint(2, 4))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(120):
            r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = sel_color
            placed = True; break
        if not placed:
            continue
        distract_colors = [c for c in [1, 2, 3, 4, 5, 6, 7, 9]
                           if c not in {sel_color, tcode}]
        for _ in range(n_distract):
            color = rng.choice(distract_colors)
            cells = _build_motif(rng, rng.randint(2, 3))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            for _ in range(80):
                r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                break
        return g
    raise ValueError("could not realize set20 p01 layout")


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_sel_color":
        # (0,0) is bg — rule's sel-color selector returns nothing.
        g[0][w - 1] = 2
        draw_frame(g, 3, 3, 7, 7, 8)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][1 + dc] = 4
        return g
    if name == "no_frame":
        # No color-8 frame — paste-target is undefined.
        g[0][0] = 4
        g[0][w - 1] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        return g
    if name == "identity_transform":
        # tcode 1 + sel motif rotationally symmetric → no visible change.
        g[0][0] = 4
        g[0][w - 1] = 1
        draw_frame(g, 3, 3, 7, 7, 8)
        # 2x2 sel motif (rotationally symmetric)
        g[8][1] = 4; g[8][2] = 4; g[9][1] = 4; g[9][2] = 4
        return g
    return g
