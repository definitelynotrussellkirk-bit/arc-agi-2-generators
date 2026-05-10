"""Generator for arc_puzzle_bank_eighth_21_bundle:hard_51_dual_template_rotation_mosaic.

Rule: 2 small template motifs in distinct colors at top, plus a 2x4 index grid
mid-bottom with values 1-8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: single_template (only 1 template → second slot of rule
has no source); no_index (no 2x4 index grid → rule's mosaic
generator finds no codes); identical_templates (two templates have
identical shape & color → second is indistinguishable from first).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "02280b74c8ab"
VERSION = "1.1.0"
TASK_ID = "02280b74c8ab"

SUMMARY = "2 small template motifs at top + small 2x4 index grid mid-bottom."

INVARIANTS = [
    "background is 0",
    "exactly 2 small motifs in distinct non-zero colors at top region",
    "a 2x4 index grid in mid-region with values 1-8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_template", "no_index", "identical_templates")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 13..16", "valid": "10..20"},
    "grid_w":            {"type": "int", "default": "rng 15..18", "valid": "12..22"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "two_templates_plus_index",
                          "valid": "two_templates_plus_index"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 15, 18)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        used = []
        placed = 0
        for _ in range(20):
            if placed >= 2: break
            color_choices = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in used]
            if not color_choices: break
            color = rng.choice(color_choices)
            cells = _build_motif(rng, rng.randint(3, 4))
            rs = [r for r, _ in cells]; cs_ = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs_) - min(cs_) + 1
            for _ in range(40):
                r0 = rng.randint(1, 4)
                c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                for r, c in cells:
                    g[r0 + r - min(rs)][c0 + c - min(cs_)] = color
                used.append(color)
                placed += 1
                break
        if placed < 2:
            continue
        idx_r = rng.randint(h // 2 - 1, h // 2 + 1)
        idx_c = rng.randint(2, w - 6)
        if idx_r + 2 > h or idx_c + 4 > w: continue
        if not _free(g, idx_r, idx_c, idx_r + 1, idx_c + 3): continue
        for r in range(2):
            for c in range(4):
                g[idx_r + r][idx_c + c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    if name == "single_template":
        # Only one template at top — rule's "second template" slot empty.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][3 + dc] = 4
        for r in range(2):
            for c in range(4):
                g[7 + r][5 + c] = 1 + ((r * 4 + c) % 8)
        return g
    if name == "no_index":
        # Two templates but no 2x4 index grid — rule has no codes.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][9 + dc] = 5
        return g
    if name == "identical_templates":
        # Two templates with same shape & color — second is indistinguishable.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][9 + dc] = 4
        for r in range(2):
            for c in range(4):
                g[7 + r][5 + c] = 1 + ((r * 4 + c) % 8)
        return g
    return g
