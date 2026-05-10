"""Generator for arc_puzzle_bank_21_set17_s:S17_H6 — pick color-2 motif by mask.

Rule: among color-2 motifs, select the one whose 3x3 growth overlaps the
color-1 mask most, breaking ties by distance and position. Output the
selected motif's tight crop in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs (no color-2 motifs → rule has no candidates);
no_mask (motifs present but no color-1 mask → selector has no
score signal); mask_overlaps_all (mask cells overlap every motif's
growth equally → tie ambiguous, "exactly one" precondition fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00a3a71adae9"
VERSION = "1.1.0"
TASK_ID = "00a3a71adae9"

SUMMARY = "2-3 color-2 motifs plus a color-1 mask selecting one motif."

INVARIANTS = [
    "background is 0",
    "2-3 separated color-2 motifs",
    "color-1 mask cells overlap only one motif's one-cell square growth",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "no_mask", "mask_overlaps_all")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "n":                 {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "motifs_with_mask_selector",
                          "valid": "motifs_with_mask_selector"},
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


def _grown_square(cells, h, w):
    out = set()
    for r, c in cells:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    out.add((nr, nc))
    return out


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n = ctx.draw_int("n", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(80):
        g = full_grid(h, w, 0)
        sizes = rng.sample([2, 3, 4, 5], n)
        target_idx = rng.randrange(n)
        motifs = []
        ok = True
        for size in sizes:
            cells = _build_motif(rng, size)
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                placed_cells = []
                for r, c in cells:
                    pr, pc = r0 + r - min(rs), c0 + c - min(cs)
                    g[pr][pc] = 2
                    placed_cells.append((pr, pc))
                motifs.append(placed_cells)
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            target = motifs[target_idx]
            target_grown = _grown_square(target, h, w)
            other_grown = set()
            for i, cells in enumerate(motifs):
                if i != target_idx:
                    other_grown.update(_grown_square(cells, h, w))
            target_cells = set(target)
            candidates = sorted(
                p for p in target_grown
                if p not in target_cells and p not in other_grown and g[p[0]][p[1]] == 0
            )
            if len(candidates) < 2:
                continue
            mask_count = rng.randint(2, min(5, len(candidates)))
            for r, c in rng.sample(candidates, mask_count):
                g[r][c] = 1
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # No color-2 motifs — selector has no candidates.
        g[3][5] = 1; g[3][6] = 1
        return g
    if name == "no_mask":
        # Motifs present but no color-1 mask — selector has no signal.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 2
        return g
    if name == "mask_overlaps_all":
        # Mask cells equidistant from every motif — selector tie ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[1 + dr][8 + dc] = 2
        # Mask cells touch both motifs equally — central placement.
        g[4][5] = 1; g[5][5] = 1
        return g
    return g
