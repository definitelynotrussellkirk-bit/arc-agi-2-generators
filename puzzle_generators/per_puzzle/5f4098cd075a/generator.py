"""Generator for arc_puzzle_bank_eleventh21:H74 — keyed library + target frames.

Rule: top region has 3-4 keyed source prototypes separated by 9-cols. Below
a 9-divider row, body has 2-3 empty hollow frames in distinct colors.
Output: stamps the source prototype matching each frame's color into the frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library (top region empty → rule has no prototypes);
no_frames (library but no body frames → no destinations);
frame_color_no_proto (frame color not in library → rule's lookup
returns nothing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5f4098cd075a"
VERSION = "1.1.0"
TASK_ID = "5f4098cd075a"

SUMMARY = "Top library + 9-divider + body with empty frames in matching colors."

INVARIANTS = [
    "background is 0",
    "rows 0-3 hold 3-4 prototype panels separated by full color-9 columns",
    "row 4 is full color-9 divider",
    "rows 5+ have 1-2 empty hollow frames in colors from the library",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_frames", "frame_color_no_proto")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_w":           {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "n_panels":          {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "body_h":            {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "library_with_target_frames",
                          "valid": "library_with_target_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        pw = ctx.draw_int("panel_w", 3, 3)
        n = ctx.draw_int("n_panels", 3, 3)
        body_h = ctx.draw_int("body_h", 7, 8)
    elif difficulty == "hard":
        pw = ctx.draw_int("panel_w", 4, 4)
        n = ctx.draw_int("n_panels", 4, 4)
        body_h = ctx.draw_int("body_h", 8, 9)
    else:
        pw = ctx.draw_int("panel_w", 3, 4)
        n = ctx.draw_int("n_panels", 3, 4)
        body_h = ctx.draw_int("body_h", 7, 9)
    rng = ctx.draw_rng("layout")

    h = 4 + 1 + body_h
    w = pw * n + (n - 1)
    g = full_grid(h, w, 0)
    for k in range(1, n):
        c = pw * k + (k - 1)
        for r in range(4):
            g[r][c] = 9
    for c in range(w):
        g[4][c] = 9
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n)
    used_colors = []
    for k in range(n):
        c0 = k * (pw + 1)
        cells = _build_motif(rng, rng.randint(2, 3))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        if sh > 4 or sw > pw: continue
        ofr = rng.randint(0, 4 - sh)
        ofc = rng.randint(0, pw - sw)
        for r, c in cells:
            g[ofr + r - min(rs)][c0 + ofc + c - min(cs)] = colors[k]
        used_colors.append(colors[k])
    if not used_colors:
        raise ValueError("no prototypes")
    n_frames = rng.randint(1, 2)
    for _ in range(n_frames):
        for _t in range(60):
            fr = rng.randint(5, h - 4)
            fc = rng.randint(0, w - 4)
            if not _free(g, fr, fc, fr + 3, fc + 3): continue
            color = rng.choice(used_colors)
            for c in range(fc, fc + 4):
                g[fr][c] = color
                g[fr + 3][c] = color
            for r in range(fr, fr + 4):
                g[r][fc] = color
                g[r][fc + 3] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    pw, n, body_h = 3, 3, 7
    h = 4 + 1 + body_h
    w = pw * n + (n - 1)
    g = full_grid(h, w, 0)
    if name == "no_library":
        for c in range(w):
            g[4][c] = 9
        # frames in body
        for c in range(2, 6): g[6][c] = 4; g[9][c] = 4
        for r in range(6, 10): g[r][2] = 4; g[r][5] = 4
        return g
    if name == "no_frames":
        for k in range(1, n):
            c = pw * k + (k - 1)
            for r in range(4):
                g[r][c] = 9
        for c in range(w):
            g[4][c] = 9
        # library prototypes only
        g[1][1] = 4; g[1][5] = 5; g[1][9] = 6
        return g
    if name == "frame_color_no_proto":
        for k in range(1, n):
            c = pw * k + (k - 1)
            for r in range(4):
                g[r][c] = 9
        for c in range(w):
            g[4][c] = 9
        g[1][1] = 4; g[1][5] = 5; g[1][9] = 6
        # frame in color 7 (not in library)
        for c in range(2, 6): g[6][c] = 7; g[9][c] = 7
        for r in range(6, 10): g[r][2] = 7; g[r][5] = 7
        return g
    return g
