"""Generator for 3b4c2228.

Rule: count solid 2×2 sub-blocks of color 3 (overlapping). Output is
3×3 with cells (r,r) for r<count set to 1, else 0.

Combinatorial axes (8): grid_h/w, n_three_blocks, n_decoy_blocks,
decoy_palette_size, position_bias, block_clustering, decoration_density,
asymmetry_force.
Degenerates: zero_three_blocks, all_three_blocks, single_decoy.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "36a24fb20512"
VERSION = "1.1.0"
TASK_ID = "36a24fb20512"
SUMMARY = "1-3 solid 2×2 3-rectangles + decoration of other colors."

INVARIANTS = [
    "count of solid 2×2 3-blocks ∈ 0..3 (rule's diag has 3 cells)",
    ">=1 solid block of OTHER color (so input isn't trivially empty)",
    "blocks separated by >2 cells (so they're distinct components)",
]

DEGENERATE_TEXTURES = ("zero_three_blocks", "all_three_blocks", "single_decoy")
HELPFUL_TEXTURES = ("balanced", "many_decoys", "edge_clustered", "spread")

AXES = {
    "grid_h":             {"type": "int", "default": "rng 6..10", "valid": "5..12"},
    "grid_w":             {"type": "int", "default": "rng 6..10", "valid": "5..12"},
    "n_three_blocks":     {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "n_decoy_blocks":     {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "decoy_palette_size": {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "block_separation":   {"type": "int", "default": "3", "valid": "2..4"},
    "decoration_density": {"type": "float", "default": "0",
                           "valid": "0..0.05"},
    "texture":            {"type": "str", "default": "rng helpful",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n3_lo, n3_hi = 5, 7, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, n3_lo, n3_hi = 9, 12, 2, 3
    else:
        h_lo, h_hi, n3_lo, n3_hi = 6, 10, 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    if texture == "many_decoys":
        n_3, n_decoy = 1, 4
    elif texture == "edge_clustered":
        n_3, n_decoy = 2, 2
    elif texture == "spread":
        n_3, n_decoy = 2, 1
    else:
        n_3 = int(overrides.get("n_three_blocks",
                                ctx.draw_int("n_three_blocks", n3_lo, n3_hi)))
        n_decoy = int(overrides.get("n_decoy_blocks",
                                    ctx.draw_int("n_decoy_blocks", 1, 3)))
    n_3 = max(0, min(3, n_3))
    n_decoy = max(1, min(5, n_decoy))
    n_decoy_palette = int(overrides.get("decoy_palette_size",
                                        ctx.draw_int("decoy_palette_size", 2, 4)))
    sep = int(overrides.get("block_separation", 3))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(40):
        if len(placed) >= n_3:
            break
        r, c = _pick_pos(bias, h, w, rng)
        if all(abs(r - pr) >= sep or abs(c - pc) >= sep for pr, pc in placed):
            draw_rect(g, r, c, 2, 2, 3)
            placed.append((r, c))
    decoy_pool = [c for c in range(1, 10) if c != 3]
    rng.shuffle(decoy_pool)
    decoy_palette = decoy_pool[:max(1, n_decoy_palette)]
    decoy_placed = []
    for _ in range(40):
        if len(decoy_placed) >= n_decoy:
            break
        color = rng.choice(decoy_palette)
        r, c = _pick_pos(bias, h, w, rng)
        ok = True
        for dr in range(2):
            for dc in range(2):
                if g[r + dr][c + dc] != 0:
                    ok = False
        if ok:
            draw_rect(g, r, c, 2, 2, color)
            decoy_placed.append((r, c))
    return g


def _pick_pos(bias, h, w, rng):
    if bias == "center":
        cr, cc = h // 2 - 1, w // 2 - 1
        return (max(0, cr + rng.randint(-1, 1)),
                max(0, cc + rng.randint(-1, 1)))
    if bias == "edge":
        edges = [(0, rng.randint(0, w - 2)),
                 (h - 2, rng.randint(0, w - 2)),
                 (rng.randint(0, h - 2), 0),
                 (rng.randint(0, h - 2), w - 2)]
        return rng.choice(edges)
    return (rng.randint(0, h - 2), rng.randint(0, w - 2))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    decoy_pool = [c for c in range(1, 10) if c != 3]
    rng.shuffle(decoy_pool)
    if name == "zero_three_blocks":
        draw_rect(g, 1, 1, 2, 2, decoy_pool[0])
        draw_rect(g, 1, w - 3, 2, 2, decoy_pool[1])
        return g
    if name == "all_three_blocks":
        positions = [(0, 0), (0, 4), (4, 0)]
        for r, c in positions:
            if r + 2 <= h and c + 2 <= w:
                draw_rect(g, r, c, 2, 2, 3)
        return g
    if name == "single_decoy":
        draw_rect(g, h // 2 - 1, w // 2 - 1, 2, 2, decoy_pool[0])
        return g
    return g
