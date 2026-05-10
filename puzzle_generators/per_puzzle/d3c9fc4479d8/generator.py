"""Generator for arc_puzzle_bank_21_set10_e:medium_j14 — Pairwise color-mapping in row 0.

Rule: scan row 0 left-to-right; consecutive non-zero pairs (c, c+1) form
mapping (a→b). Drop row 0; for body cells, replace v with mapping[v] if
present, else v.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, no_body_blobs, source_not_in_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d3c9fc4479d8"
VERSION = "1.1.0"
TASK_ID = "d3c9fc4479d8"
SUMMARY = "Row 0 has 1-2 color-mapping pairs (a, b consecutive); body has blobs of source colors; output remaps."

INVARIANTS = [
    "row 0 has 2-4 non-zero cells in adjacent pairs",
    "each pair (a, b) maps source color a → target color b",
    "body has at least one blob of each source color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_body_blobs", "source_not_in_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "= 2*n_pairs", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "row0_pairs_blobs_below",
                       "valid": "row0_pairs_blobs_below"},
    "n_distinct_colors": {"type": "int", "default": "= 2*n_pairs", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n_pairs = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        n_pairs = ctx.draw_int("n_pairs", 1, 2)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(1, 10)); rng.shuffle(palette)
    sources = palette[:n_pairs]
    targets = palette[n_pairs:n_pairs + n_pairs]
    pos = 0
    pair_positions = []
    for s, t in zip(sources, targets):
        if pos + 1 >= w: break
        g[0][pos] = s
        g[0][pos + 1] = t
        pair_positions.append((pos, pos + 1))
        pos += 3
    used = set()
    for s in sources:
        for _ in range(20):
            blob = grow_blob(rng, h - 1, w, used, rng.randint(1, 2))
            if blob is None: continue
            shifted = {(r + 1, c) for r, c in blob}
            used |= shifted
            for r, c in shifted: g[r][c] = s
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Body blobs but row 0 is empty — rule's mapping table is empty,
        # output equals input.
        for r, c in [(2, 2), (2, 3)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7)]: g[r][c] = 6
        return g
    if name == "no_body_blobs":
        # Row-0 mapping pairs but no body blobs — rule has no source
        # cells to remap.
        g[0][0] = 4; g[0][1] = 7
        return g
    if name == "source_not_in_body":
        # Row-0 pair maps a→b but body uses a different color, not a
        # — rule's mapping never fires; output equals input.
        g[0][0] = 4; g[0][1] = 7
        for r, c in [(2, 2), (2, 3)]: g[r][c] = 6
        return g
    return g
