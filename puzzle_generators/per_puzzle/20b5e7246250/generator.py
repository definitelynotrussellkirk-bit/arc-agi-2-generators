"""Generator for arc_puzzle_bank_21_set18_bundle:hard_p01 — frame + key-above + source motif.

Rule: 2 hollow rectangular color-5 frames. Above each frame's top row, a
single-cell marker (in some color) is the 'key'. Elsewhere, a multi-cell
motif in that key color is the source. Output stamps each source into the
matching frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-5 frames → rule has no destinations);
no_keys (frames but no key markers above → rule has no source-color
hint); key_no_motif (key color present above frame but no
matching-color motif elsewhere → rule has nothing to stamp).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "20b5e7246250"
VERSION = "1.1.0"
TASK_ID = "20b5e7246250"

SUMMARY = "2 color-5 frames + key markers above each + matching source motifs."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow color-5 frames at distinct positions",
    "each frame has a single-cell color marker above its top row (the 'key')",
    "for each unique key color, there is a multi-cell motif of that color elsewhere",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_keys", "key_no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":     {"type": "str", "default": "frames_keys_motifs",
                          "valid": "frames_keys_motifs"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 17)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        keys = rng.sample([2, 3, 4, 6, 7, 8, 9], 2)
        frame_specs = []
        ok = True
        for i in range(2):
            fh, fw = rng.choice([(6, 6), (6, 7), (7, 6), (5, 7), (7, 5)])
            placed = False
            for _ in range(120):
                r0 = rng.randint(2, h - fh - 1); c0 = rng.randint(1, w - fw - 1)
                if not _free(g, r0 - 1, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 5)
                frame_specs.append((r0, c0, fh, fw))
                key_col = rng.randint(c0 + 1, c0 + fw - 2)
                g[r0 - 1][key_col] = keys[i]
                placed = True; break
            if not placed:
                ok = False; break
        if not ok:
            continue
        ok2 = True
        for key_color in keys:
            cells = _build_motif(rng, rng.randint(2, 4))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = key_color
                placed = True; break
            if not placed:
                ok2 = False; break
        if ok2:
            return g
    raise ValueError("could not realize set18 p01 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No color-5 frames — rule has no destinations.
        g[2][3] = 4; g[2][9] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[7 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][9 + dc] = 6
        return g
    if name == "no_keys":
        # Frames but no key markers above.
        draw_frame(g, 3, 1, 8, 6, 5)
        draw_frame(g, 3, 9, 8, 14, 5)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[10 + dr][2 + dc] = 4
        return g
    if name == "key_no_motif":
        # Frames + keys but no matching motif colors.
        draw_frame(g, 3, 1, 8, 6, 5)
        draw_frame(g, 3, 9, 8, 14, 5)
        g[2][3] = 4; g[2][11] = 6
        # Motif color 7 doesn't match either key.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[10 + dr][6 + dc] = 7
        return g
    return g
