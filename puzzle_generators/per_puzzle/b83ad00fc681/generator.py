"""Generator for arc_puzzle_bank_eleventh21:H72 — keyed prototype dictionary stamping.

Rule: top region (rows 0-3) has 3-4 color-keyed prototype panels separated
by full color-9 columns. A horizontal color-9 divider row at row 4. Body has
single-cell markers in matching colors. Output stamps prototypes at markers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dict (top dict region empty → rule has no
prototypes); no_markers (dict present but body has no markers →
rule has no destinations); marker_color_no_proto (a marker uses a
color not in the dict → rule's lookup returns nothing for that
slot).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b83ad00fc681"
VERSION = "1.1.0"
TASK_ID = "b83ad00fc681"

SUMMARY = "Top dict (rows 0-3) with 3-4 keyed prototypes + 9-divider row + body with markers."

INVARIANTS = [
    "background is 0",
    "rows 0-3 hold 3-4 prototype panels separated by full color-9 columns",
    "row 4 is a full color-9 horizontal divider",
    "rows 5+ have 1-3 single-cell markers in colors used by prototypes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dict", "no_markers", "marker_color_no_proto")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_w":           {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "n_panels":          {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "body_h":            {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "top_dict_with_body_markers",
                          "valid": "top_dict_with_body_markers"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        pw = ctx.draw_int("panel_w", 3, 3)
        n = ctx.draw_int("n_panels", 3, 3)
        body_h = ctx.draw_int("body_h", 5, 6)
    elif difficulty == "hard":
        pw = ctx.draw_int("panel_w", 4, 4)
        n = ctx.draw_int("n_panels", 4, 4)
        body_h = ctx.draw_int("body_h", 6, 7)
    else:
        pw = ctx.draw_int("panel_w", 3, 4)
        n = ctx.draw_int("n_panels", 3, 4)
        body_h = ctx.draw_int("body_h", 5, 7)
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
    proto_pos = []
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
        proto_pos.append(colors[k])
    if not proto_pos:
        raise ValueError("no prototypes placed")
    n_markers = rng.randint(1, 3)
    for _ in range(n_markers):
        for _t in range(40):
            r = rng.randint(5, h - 1)
            c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(proto_pos)
                break
    return g


def _draw_from_degenerate(name, rng):
    pw, n, body_h = 3, 3, 5
    h = 4 + 1 + body_h
    w = pw * n + (n - 1)
    g = full_grid(h, w, 0)
    if name == "no_dict":
        # Top dict region empty — rule has no prototypes.
        for c in range(w):
            g[4][c] = 9
        g[6][2] = 4; g[7][6] = 5
        return g
    if name == "no_markers":
        # Dict present but body has no markers.
        for k in range(1, n):
            c = pw * k + (k - 1)
            for r in range(4):
                g[r][c] = 9
        for c in range(w):
            g[4][c] = 9
        g[1][1] = 4; g[1][5] = 5; g[1][9] = 6
        return g
    if name == "marker_color_no_proto":
        # Markers reference colors not in dict.
        for k in range(1, n):
            c = pw * k + (k - 1)
            for r in range(4):
                g[r][c] = 9
        for c in range(w):
            g[4][c] = 9
        g[1][1] = 4; g[1][5] = 5; g[1][9] = 6
        # Markers in colors 7, 8 (not in dict {4,5,6})
        g[6][2] = 7; g[8][8] = 8
        return g
    return g
