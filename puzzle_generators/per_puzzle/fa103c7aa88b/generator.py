"""Generator for arc_puzzle_bank_21_set13_bundle:hard_m05 — set-op of two largest shapes by key.

Rule: cell (0, 0) is the key (1=union, 2=intersection, else=symmetric difference).
Two largest non-key components are aligned to a common origin; the output is
their set-operation cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_op_key (cell (0,0) is bg → rule's op selector returns
nothing), single_component (only one non-key motif → rule's "two
largest" has no second operand), tied_sizes (≥2 components share max
size → "two largest" tie-break decides which pair to use).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fa103c7aa88b"
VERSION = "1.1.0"
TASK_ID = "fa103c7aa88b"

SUMMARY = "Cell (0,0) holds key (1/2/3); 2 large shapes elsewhere; output is set-op of their cells."

INVARIANTS = [
    "background is 0",
    "cell (0, 0) holds the key (1, 2, or 3)",
    "exactly 2 connected components elsewhere, each strictly larger than the key cell",
    "components are isolated from each other and from (0, 0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_op_key", "single_component", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "key_plus_two_largest",
                          "valid": "key_plus_two_largest"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
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


def _build_motif(rng, k, color):
    cells = [(0, 0)]
    seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sr0, sc0 = -min(rs), -min(cs)
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    grid = [[0] * sw for _ in range(sh)]
    for r, c in cells:
        grid[sr0 + r][sc0 + c] = color
    return grid


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        key = rng.choice([1, 2, 3])
        g[0][0] = key
        ok = True
        comp_colors = rng.sample([c for c in [4, 5, 6, 7, 8, 9] if c != key], 2)
        for color in comp_colors:
            k = rng.randint(3, 5)
            motif = _build_motif(rng, k, color)
            sh, sw = len(motif), len(motif[0])
            placed = False
            for _ in range(120):
                r0 = rng.randint(1, h - sh); c0 = rng.randint(1, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1):
                    continue
                for r in range(sh):
                    for c in range(sw):
                        if motif[r][c] != 0:
                            g[r0 + r][c0 + c] = motif[r][c]
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_m05 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_op_key":
        # (0,0) is bg — rule's op selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 6
        return g
    if name == "single_component":
        # Only one non-key component — "two largest" has no second
        # operand.
        g[0][0] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][3 + dc] = 4
        return g
    if name == "tied_sizes":
        # Two components share max size — "two largest" tie-break
        # decides which pair.
        g[0][0] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 6   # tied with prev
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[7 + dr][2 + dc] = 7   # tied
        return g
    return g
