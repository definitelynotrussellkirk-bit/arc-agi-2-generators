"""Generator for arc_puzzle_bank_21_set16_bundle:medium_p03 — crop cells of corner-marker color.

Rule: 4 corner cells share a 'marker' color. All other cells of that marker
color (excluding corners) are cropped out as the output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_marker (corners don't all share one color → rule's
marker selector is undefined), no_body_cells (no marker-color cells in
body → rule's crop produces empty output), corners_disagree (corners
hold different colors → rule has no single "the marker" to use).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d94e8b169413"
VERSION = "1.1.0"
TASK_ID = "d94e8b169413"

SUMMARY = "4 corner cells in marker color + 1-3 marker-color cells elsewhere + 1-2 distractor motifs."

INVARIANTS = [
    "background is 0",
    "4 corner cells share a single marker color (non-zero)",
    "1-3 marker-color cells in the body (non-corner positions)",
    "1-2 distractor motifs in distinct non-marker colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_marker", "no_body_cells", "corners_disagree")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "corners_marker_plus_body",
                          "valid": "corners_marker_plus_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        marker = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        g[0][0] = marker
        g[0][w - 1] = marker
        g[h - 1][0] = marker
        g[h - 1][w - 1] = marker
        n_marker = rng.randint(2, 4)
        for _ in range(n_marker):
            for _t in range(60):
                r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
                if g[r][c] != 0: continue
                g[r][c] = marker
                break
        n_distract = rng.randint(1, 2)
        d_colors = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != marker]
        for _ in range(n_distract):
            color = rng.choice(d_colors)
            cells = _build_motif(rng, rng.randint(2, 3))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            for _ in range(60):
                r0 = rng.randint(1, h - sh - 1); c0 = rng.randint(1, w - sw - 1)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                break
        return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_corner_marker":
        # No corners are marked — rule's marker selector finds nothing.
        g[3][3] = 4; g[3][4] = 4
        g[5][6] = 6; g[6][6] = 6
        return g
    if name == "no_body_cells":
        # 4 corners marked but no marker-color cells in body — rule's
        # crop produces empty output.
        g[0][0] = 4; g[0][w - 1] = 4
        g[h - 1][0] = 4; g[h - 1][w - 1] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 6
        return g
    if name == "corners_disagree":
        # Corners hold different colors — rule has no single "the
        # marker" to use.
        g[0][0] = 2; g[0][w - 1] = 4
        g[h - 1][0] = 6; g[h - 1][w - 1] = 8
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 3
        return g
    return g
