"""Generator for v3_rich_schema:medium_05_stamp_exemplar_at_targets — stamp color-3 exemplar at color-1 markers.

Rule: a color-3 exemplar shape (3-5 cells) + 1-3 single-cell color-1 markers.
The exemplar's relative offsets are stamped (in color 3) at each marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_exemplar (no color-3 motif → rule has no template);
no_targets (exemplar present but no target markers → rule has no
destinations); single_cell_exemplar (exemplar is just 1 cell → all
stamps trivial, no shape contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "761a24339019"
VERSION = "1.1.0"
TASK_ID = "761a24339019"

SUMMARY = "1 color-3 exemplar + 1-3 single-cell color-1 markers + 1 nearby color-1 marker (anchor)."

INVARIANTS = [
    "background is 0",
    "exactly one color-3 connected motif (3-5 cells)",
    "1-3 color-1 single-cell markers at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_exemplar", "no_targets", "single_cell_exemplar")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "n_targets":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "exemplar_top_left_targets_bottom",
                          "valid": "exemplar_top_left_targets_bottom"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_targets", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n_targets", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n = ctx.draw_int("n_targets", 1, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, max(0, h // 2 - sh - 1))
            c0 = rng.randint(0, max(0, w // 2 - sw - 1))
            if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = 3
            ar = r0; ac = c0 - 1 if c0 > 0 else c0 + sw
            if 0 <= ar < h and 0 <= ac < w and g[ar][ac] == 0:
                g[ar][ac] = 1
            placed = True; break
        if not placed:
            continue
        ok = True
        for _ in range(n):
            placed_t = False
            for _t in range(80):
                r = rng.randint(h // 2, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if any(g[r + dr][c + dc] != 0 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                       if 0 <= r + dr < h and 0 <= c + dc < w):
                    continue
                g[r][c] = 1
                placed_t = True; break
            if not placed_t:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_exemplar":
        # No color-3 motif — rule has no template.
        g[6][3] = 1; g[7][8] = 1
        return g
    if name == "no_targets":
        # Exemplar but no target markers — rule has no destinations.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 3
        return g
    if name == "single_cell_exemplar":
        # 1-cell exemplar — all stamps are trivial single cells.
        g[2][2] = 3
        g[1][1] = 1
        g[6][3] = 1; g[7][8] = 1
        return g
    return g
