"""Generator for arc_puzzle_bank_21_set15_bundle:hard_o01 — sel+key+frame.

Rule: (0, 0) holds a transform key (1..6). Row 0 also has a 'selector' color
elsewhere. A color-8 hollow frame. Several components in selector-color (and
distractor colors); the largest selector-color component is transformed by
key and pasted into the frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_key (cell (0,0) is bg → rule has no transform);
no_frame (key + selector but no 8-frame → rule has no destination);
no_sel_motif (key + selector marker but no body shape in selector
color → rule has nothing to transform).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "0ffe583089f7"
VERSION = "1.1.0"
TASK_ID = "0ffe583089f7"

SUMMARY = "(0,0)=key, row 0 has selector color, body has 8-frame + selector-color motifs."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds a transform key (1..6)",
    "row 0 has at least one cell of the selector color (not at (0,0))",
    "exactly one hollow color-8 frame in the body",
    "1-2 motifs in the selector color (and 0-1 distractor motifs)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_frame", "no_sel_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..16", "valid": "12..18"},
    "n_sel":             {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_distract":        {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "key_at_origin_with_frame_and_motifs",
                          "valid": "key_at_origin_with_frame_and_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
        n_sel = ctx.draw_int("n_sel", 1, 1)
        n_distract = ctx.draw_int("n_distract", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
        n_sel = ctx.draw_int("n_sel", 2, 2)
        n_distract = ctx.draw_int("n_distract", 1, 1)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
        n_sel = ctx.draw_int("n_sel", 1, 2)
        n_distract = ctx.draw_int("n_distract", 0, 1)
    rng = ctx.draw_rng("layout")

    sel_color = rng.choice([1, 2, 3, 4, 6, 7, 9])
    key_color = rng.randint(1, 6)
    if key_color == sel_color:
        key_color = (key_color % 6) + 1

    for outer in range(40):
        g = full_grid(h, w, 0)
        g[0][0] = key_color
        sel_col = rng.randint(2, w - 1)
        g[0][sel_col] = sel_color
        fh, fw = rng.choice([(5, 6), (5, 7), (6, 6), (6, 7)])
        placed_f = False
        for _ in range(120):
            r0 = rng.randint(2, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 8)
            placed_f = True; break
        if not placed_f:
            continue
        ok = True
        for i in range(n_sel):
            cells = _build_motif(rng, rng.randint(3 if i == 0 else 2, 5 if i == 0 else 3))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed_b = False
            for _ in range(120):
                r0 = rng.randint(2, h - sh - 1); c0 = rng.randint(1, w - sw - 1)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = sel_color
                placed_b = True; break
            if not placed_b:
                ok = False; break
        if not ok:
            continue
        for _ in range(n_distract):
            distract_color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 9]
                                         if c not in {sel_color, key_color}])
            cells = _build_motif(rng, rng.randint(2, 3))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            for _ in range(80):
                r0 = rng.randint(2, h - sh - 1); c0 = rng.randint(1, w - sw - 1)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = distract_color
                break
        return g
    raise ValueError("could not realize set15 o01 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_key":
        # No key at (0, 0) — rule has no transform.
        g[0][5] = 4
        draw_frame(g, 3, 1, 7, 6, 8)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][9 + dc] = 4
        return g
    if name == "no_frame":
        # Key + selector but no 8-frame.
        g[0][0] = 2; g[0][5] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][9 + dc] = 4
        return g
    if name == "no_sel_motif":
        # Key + selector marker but no body shape in selector color.
        g[0][0] = 2; g[0][5] = 4
        draw_frame(g, 3, 1, 7, 6, 8)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][9 + dc] = 6
        return g
    return g
