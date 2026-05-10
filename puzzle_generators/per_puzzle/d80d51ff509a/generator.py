"""Generator for arc_puzzle_bank_21_set13_bundle:hard_m07 — ranked-component transform.

Rule: (0, 0) holds rank-key (1-indexed by size asc); (0, w-1) holds tf-key
(4=identity, 5=rotate-cw, 6=flip-lr, else=rotate-180). Sort body components by
size asc; pick the rank-key-th; apply the transform to its crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 components share size → "rank-key-th by
size asc" is ambiguous, tie-break decides), no_rank (cell (0,0) is bg →
rule's rank selector returns nothing), identity_transform (tf-key = 4 →
rule's transform is identity, output equals cropped target).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d80d51ff509a"
VERSION = "1.1.0"
TASK_ID = "d80d51ff509a"

SUMMARY = "(0,0)=rank-key, (0,w-1)=tf-key (4..7), body has N distinct-size components."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds rank-key (1..N)",
    "(0, w-1) holds tf-key in {4, 5, 6, 7}",
    "body has N=3 components in distinct sizes (so ranking is unambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "no_rank", "identity_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "rank_tf_plus_components",
                          "valid": "rank_tf_plus_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES_BY_SIZE = {
    2: [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    3: [[(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 0)]],
    4: [[(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)], [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 14, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    n = 3
    sizes = rng.sample([2, 3, 4, 5, 6], n)
    rank_key = rng.randint(1, n)
    tf_key = rng.randint(4, 7)
    used = {rank_key, tf_key}
    body_colors = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in used], n)

    for outer in range(40):
        g = full_grid(h, w, 0)
        g[0][0] = rank_key
        g[0][w - 1] = tf_key
        ok = True
        for sz, color in zip(sizes, body_colors):
            shape = rng.choice(_SHAPES_BY_SIZE[sz])
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(80):
                r0 = rng.randint(1, h - sh)
                c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_m07 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        g[0][0] = 2
        g[0][w - 1] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 8
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
            g[7 + dr][3 + dc] = 9
        return g
    if name == "no_rank":
        g[0][w - 1] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 7
        for dr, dc in [(0, 0), (1, 0), (2, 0)]:
            g[5 + dr][5 + dc] = 8
        return g
    if name == "identity_transform":
        g[0][0] = 1
        g[0][w - 1] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 7
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][6 + dc] = 8
        return g
    return g
