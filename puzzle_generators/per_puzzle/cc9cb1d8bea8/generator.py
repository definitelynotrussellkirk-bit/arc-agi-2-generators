"""Generator for arc_additional_puzzles_21_set12_bundle:H84 — ranked component with composed transforms.

Rule: row 0 cell 0 = k (1-indexed selector by area-desc / color-asc tiebreaker);
row 0 cells (w-2) and (w-1) = transform codes t1 and t2 (1=cw, 2=180, 3=flip-lr,
4=flip-ud). Sort components by (area desc, color asc), pick the k-th, crop, apply
t1 then t2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 components share size → "k-th by area-desc"
falls back to color-asc tiebreaker, no clear cross-candidate contrast),
no_k (cell (0,0) is bg → rule's k-selector returns nothing, no
component chosen), identity_transforms (t1=t2=identity-like, e.g.,
both 4 = flip-ud-then-flip-ud = identity → rule's transform composition
is identity, output equals cropped target).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cc9cb1d8bea8"
VERSION = "1.1.0"
TASK_ID = "cc9cb1d8bea8"

SUMMARY = "Top row anchors: (0,0)=k selector, (0,w-2)=t1, (0,w-1)=t2; body has K-many distinct-area components."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds k in [1..n_components], (0, w-2) and (0, w-1) hold transform codes 1..4",
    "the rest of row 0 is 0",
    "body has 3-4 isolated 4-conn components in distinct colors and distinct sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "no_k", "identity_transforms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "n_components":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "k_t1_t2_plus_components",
                          "valid": "k_t1_t2_plus_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES_BY_SIZE = {
    2: [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    3: [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (0, 1), (1, 0)]],
    4: [[(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)], [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
    7: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]],
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
        n = ctx.draw_int("n_components", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 14, 14)
        n = ctx.draw_int("n_components", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n = ctx.draw_int("n_components", 3, 4)
    rng = ctx.draw_rng("layout")

    sizes = rng.sample([2, 3, 4, 5, 6, 7], n)
    sizes.sort(reverse=True)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n)
    k = rng.randint(1, n)
    t1 = rng.randint(1, 4)
    t2 = rng.randint(1, 4)

    for outer in range(40):
        g = full_grid(h, w, 0)
        g[0][0] = k
        g[0][w - 2] = t1
        g[0][w - 1] = t2
        ok = True
        for sz, color in zip(sizes, colors):
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
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place {0} distinct-area components".format(n))


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two components share the same size — area-desc rank breaks
        # to color-asc tiebreaker; no clear cross-candidate contrast.
        g[0][0] = 1
        g[0][w - 2] = 1
        g[0][w - 1] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 4   # tied size with prev
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
            g[8 + dr][3 + dc] = 6
        return g
    if name == "no_k":
        # (0,0) is bg — rule's k-selector returns nothing.
        g[0][w - 2] = 1
        g[0][w - 1] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 3
        for dr, dc in [(0, 0), (1, 0), (2, 0)]:
            g[5 + dr][5 + dc] = 4
        return g
    if name == "identity_transforms":
        # Both transforms cancel (4=flip-ud applied twice = identity);
        # rule's composed transform is identity.
        g[0][0] = 1
        g[0][w - 2] = 4
        g[0][w - 1] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[7 + dr][5 + dc] = 4
        return g
    return g
