"""Generator for v2_meta_puzzles:H3 — connect 2 motif pairs by line.

Rule: 2 color-3 motifs and 2 color-4 motifs at varied positions; output
draws connecting lines between same-color pairs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, single_endpoint, mismatched_pair_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2a08118e8823"
VERSION = "1.1.0"
TASK_ID = "2a08118e8823"

SUMMARY = "2 color-3 motifs + 2 color-4 motifs at distinct positions."

INVARIANTS = [
    "background is 0",
    "exactly 2 color-3 motifs and 2 color-4 motifs at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "single_endpoint", "mismatched_pair_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_motif_pairs",
                       "valid": "two_motif_pairs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for color in (3, 4):
            for _ in range(2):
                cells = _build_motif(rng, rng.randint(2, 3))
                rs = [r for r, _ in cells]; cs = [c for _, c in cells]
                sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
                placed = False
                for _ in range(120):
                    r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                    if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                    for r, c in cells:
                        g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                    placed = True; break
                if not placed:
                    ok = False; break
            if not ok: break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # Empty grid — rule has no pairs to connect.
        return g
    if name == "single_endpoint":
        # Each color appears once — rule's "connect pair"
        # precondition fails; lines undefined.
        g[2][2] = 3; g[5][7] = 4
        return g
    if name == "mismatched_pair_counts":
        # 1 color-3 motif and 3 color-4 motifs — rule's "exactly 2
        # of each color" filter rejects; rule's connect branch can't
        # decide which color-4 pair to use.
        g[2][2] = 3
        g[5][5] = 4; g[7][9] = 4; g[2][10] = 4
        return g
    return g
