"""Generator for arc_puzzle_bank_21_set15_bundle:hard_o06 — 2 objects + transform key + boolean op key.

Rule: row 0 holds a transform key in {1, 2, 3} and a boolean-op key in
{4, 5, 6}. Body has 2 colored motifs (sorted left-to-right). The first is
transformed by tkey; then the two are combined per okey, output painted in okey.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys (row 0 empty → rule has no transform/op);
no_motifs (keys present but no body motifs → boolean op has no
operands); identical_motifs (both motifs identical after first's
transform → AND/OR collapse to A, XOR/diff is empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e7a6ba0bb90"
VERSION = "1.1.0"
TASK_ID = "1e7a6ba0bb90"

SUMMARY = "Row 0 has a tkey (1/2/3) + okey (4/5/6); body has 2 motifs in distinct non-{0,1..6} colors."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly one cell in {1, 2, 3} (tkey) and one cell in {4, 5, 6} (okey) at distinct columns",
    "body (rows ≥ 2) has 2 connected motifs in distinct non-{0, 1..6} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "no_motifs", "identical_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "row0_keys_plus_two_motifs",
                          "valid": "row0_keys_plus_two_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        tkey = rng.choice([1, 2, 3])
        okey = rng.choice([4, 5, 6])
        c_t = rng.randint(0, w - 1); c_o = rng.randint(0, w - 1)
        if c_t == c_o:
            c_o = (c_o + 1) % w
        g[0][c_t] = tkey
        g[0][c_o] = okey
        ca, cb = rng.sample([7, 8, 9], 2)
        ok = True
        for color in (ca, cb):
            cells = _build_motif(rng, rng.randint(3, 5))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs)] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set15 o06 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_keys":
        # Row 0 empty — rule has no transform/op.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 7
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][8 + dc] = 8
        return g
    if name == "no_motifs":
        # Keys present but no body motifs.
        g[0][2] = 1; g[0][8] = 4
        return g
    if name == "identical_motifs":
        # Both motifs identical → AND/OR == A, XOR empty.
        g[0][2] = 1; g[0][8] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][8 + dc] = 8
        return g
    return g
