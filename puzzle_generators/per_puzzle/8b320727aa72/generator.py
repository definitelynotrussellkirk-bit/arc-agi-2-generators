"""Generator for puzzle e84fef15.

Rule: 29×29 grid is 5×5 of 5×5 tiles separated by 1-cell gaps. Rule
extracts the consensus 5×5 tile; cells where tiles disagree get 1.

Combinatorial axes (8): n_filled_in_tile, n_disagreements,
disagreement_strength, palette_size, palette_kind, tile_layout,
disagreement_distribution, anchor_position.
Degenerates: empty_tile, full_tile, all_disagree.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b320727aa72"
VERSION = "1.1.0"
TASK_ID = "8b320727aa72"
SUMMARY = "29×29 of 25 5×5 tiles; rule extracts consensus tile, marks disagreements as 1."

INVARIANTS = [
    "grid is exactly 29×29",
    "25 tiles at offsets {0, 6, 12, 18, 24}",
    "the 25 tiles agree on most cells",
    "1-5 cell positions have disagreement (so output has both consensus and 1-marked)",
    "no color 1 in input (rule writes 1 for output disagreement)",
]

TILE_LAYOUTS = ("scattered", "blob", "diagonal", "frame",
                "corners", "checker", "stripes")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_tile", "full_tile", "all_disagree")
HELPFUL_TEXTURES = TILE_LAYOUTS

AXES = {
    "n_filled_in_tile":       {"type": "int", "default": "rng 8..18",
                               "valid": "1..24"},
    "n_disagreements":        {"type": "int", "default": "rng 1..3",
                               "valid": "1..5"},
    "disagreement_strength":  {"type": "int", "default": "rng 1..8",
                               "valid": "1..24"},
    "palette_size":           {"type": "int", "default": "rng 2..5",
                               "valid": "1..7"},
    "palette_kind":           {"type": "str", "default": "rng helpful",
                               "valid": "|".join(PALETTE_KINDS)},
    "tile_layout":            {"type": "str", "default": "rng helpful",
                               "valid": "|".join(TILE_LAYOUTS)},
    "disagreement_distribution": {"type": "str",
                                  "default": "rng spread|center|edge",
                                  "valid": "spread|center|edge"},
    "anchor_position":        {"type": "bool", "default": "false",
                               "valid": "true|false"},
    "texture":                {"type": "str", "default": "alias for tile_layout",
                               "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        nf_lo, nf_hi, nd_lo, nd_hi = 4, 10, 1, 1
    elif difficulty == "hard":
        nf_lo, nf_hi, nd_lo, nd_hi = 14, 22, 3, 5
    else:
        nf_lo, nf_hi, nd_lo, nd_hi = 8, 18, 1, 3
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n_filled = int(overrides.get("n_filled_in_tile",
                                 ctx.draw_int("n_filled_in_tile",
                                              nf_lo, nf_hi)))
    n_filled = max(1, min(24, n_filled))
    n_dis = int(overrides.get("n_disagreements",
                              ctx.draw_int("n_disagreements", nd_lo, nd_hi)))
    n_dis = max(1, min(25 - n_filled, n_dis))
    dis_strength = int(overrides.get("disagreement_strength",
                                     ctx.draw_int("disagreement_strength",
                                                  1, 8)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [5, 7, 8]
    elif palette_kind == "small":
        pool = [3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = pool[:max(1, n_palette)]
    layout = (overrides.get("texture") or overrides.get("tile_layout")
              or ctx.draw_choice("tile_layout", list(TILE_LAYOUTS)))
    dis_dist = overrides.get("disagreement_distribution",
                             ctx.draw_choice("disagreement_distribution",
                                             ["spread", "center", "edge"]))
    tile = [[0] * 5 for _ in range(5)]
    positions = _layout_positions(layout, rng)
    for i, (r, c) in enumerate(positions[:n_filled]):
        tile[r][c] = rng.choice(palette)
    if bool(overrides.get("anchor_position", False)):
        tile[0][0] = palette[0]
    available = [(r, c) for r in range(5) for c in range(5)
                 if tile[r][c] == 0]
    if dis_dist == "center":
        available.sort(key=lambda rc: abs(rc[0] - 2) + abs(rc[1] - 2))
    elif dis_dist == "edge":
        available.sort(key=lambda rc: -max(rc[0], 4 - rc[0],
                                           rc[1], 4 - rc[1]))
    else:
        rng.shuffle(available)
    dis_positions = available[:min(n_dis, len(available))]
    tile_offsets = [0, 6, 12, 18, 24]
    g = full_grid(29, 29, 0)
    for tr_o in tile_offsets:
        for tc_o in tile_offsets:
            for r in range(5):
                for c in range(5):
                    g[tr_o + r][tc_o + c] = tile[r][c]
    for r, c in dis_positions:
        tile_indices = rng.sample(range(25),
                                  min(dis_strength, 25))
        for ti in tile_indices:
            tr, tc = divmod(ti, 5)
            g[tile_offsets[tr] + r][tile_offsets[tc] + c] = rng.choice(palette)
    return g


def _layout_positions(layout, rng):
    positions = [(r, c) for r in range(5) for c in range(5)]
    if layout == "blob":
        cr, cc = rng.randint(0, 4), rng.randint(0, 4)
        positions.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return positions
    if layout == "diagonal":
        diag = [(k, k) for k in range(5)]
        rest = [c for c in positions if c not in diag]
        rng.shuffle(rest)
        return diag + rest
    if layout == "frame":
        border = [(r, c) for (r, c) in positions
                  if r in (0, 4) or c in (0, 4)]
        interior = [(r, c) for (r, c) in positions if (r, c) not in border]
        rng.shuffle(border); rng.shuffle(interior)
        return border + interior
    if layout == "corners":
        corners = [(0, 0), (0, 4), (4, 0), (4, 4)]
        rest = [c for c in positions if c not in corners]
        rng.shuffle(rest)
        return corners + rest
    if layout == "checker":
        even = [(r, c) for (r, c) in positions if (r + c) % 2 == 0]
        odd = [(r, c) for (r, c) in positions if (r + c) % 2 != 0]
        rng.shuffle(even); rng.shuffle(odd)
        return even + odd
    if layout == "stripes":
        even = [(r, c) for (r, c) in positions if r % 2 == 0]
        odd = [(r, c) for (r, c) in positions if r % 2 != 0]
        rng.shuffle(even); rng.shuffle(odd)
        return even + odd
    rng.shuffle(positions)
    return positions


def _draw_from_degenerate(name, rng):
    tile_offsets = [0, 6, 12, 18, 24]
    g = full_grid(29, 29, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_tile":
        g[0][0] = color
        return g
    if name == "full_tile":
        for tr_o in tile_offsets:
            for tc_o in tile_offsets:
                for r in range(5):
                    for c in range(5):
                        g[tr_o + r][tc_o + c] = color
        return g
    if name == "all_disagree":
        for tr_o in tile_offsets:
            for tc_o in tile_offsets:
                for r in range(5):
                    for c in range(5):
                        g[tr_o + r][tc_o + c] = rng.choice(
                            [2, 3, 4, 5, 6, 7, 8, 9])
        return g
    return g
