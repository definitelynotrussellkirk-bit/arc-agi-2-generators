"""Generator for arc_additional_puzzles_21_set20_bundle:H134 — commanded pivot rotations.

Rule: pivots are color-8 cells; the cell immediately to the left of each pivot
holds a command (1, 2, or 3 quarter-turns CW). Each non-{0, 8, 1, 2, 3}
component is matched to the nearest pivot (Manhattan), then rotated CW by
the pivot's command. Output preserves pivots and the rotated components.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivots (no color-8 → rule's pivot selector returns
nothing), no_command (pivot present but cell to its left is bg → rule's
command code is undefined), no_components (pivots present but no
non-pivot components → rule has nothing to rotate).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "256f70c87bba"
VERSION = "1.1.0"
TASK_ID = "256f70c87bba"

SUMMARY = "1-2 color-8 pivots with command (1, 2, or 3) to their left; nearby components rotated."

INVARIANTS = [
    "background is 0",
    "1 or 2 color-8 pivots; each has a command cell (1, 2, or 3) immediately to its left",
    "1 or 2 small connected components in colors {4, 5, 6, 7, 9} placed near (Manhattan) their pivot",
    "rotated components must stay in-bounds (so we keep components close to pivots)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivots", "no_command", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_pivots":          {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "pivots_with_commands_plus_components",
                          "valid": "pivots_with_commands_plus_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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


def _rotate_cells_cw(cells, pivot, turns):
    pr, pc = pivot
    out = []
    for r, c in cells:
        cur_r, cur_c = r, c
        for _ in range(turns % 4):
            dr = cur_r - pr
            dc = cur_c - pc
            cur_r = pr + dc
            cur_c = pc - dr
        out.append((cur_r, cur_c))
    return out


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_pivots = ctx.draw_int("n_pivots", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_pivots = ctx.draw_int("n_pivots", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_pivots = ctx.draw_int("n_pivots", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        pivots = []
        ok = True
        for pi in range(n_pivots):
            placed = False
            for _ in range(80):
                pr = rng.randint(2, h - 3)
                pc = rng.randint(3, w - 3)
                if g[pr][pc] != 0 or g[pr][pc - 1] != 0:
                    continue
                if any(abs(pr - r) + abs(pc - c) < 5 for r, c, _ in pivots):
                    continue
                cmd = rng.randint(1, 3)
                g[pr][pc] = 8
                g[pr][pc - 1] = cmd
                pivots.append((pr, pc, cmd))
                placed = True
                break
            if not placed:
                ok = False
                break
        if not ok:
            continue

        comp_colors = rng.sample([4, 5, 6, 7, 9], n_pivots)
        for (pr, pc, cmd), color in zip(pivots, comp_colors):
            placed_c = False
            for _ in range(120):
                motif = [(0, 0)]
                seen = {(0, 0)}
                target = rng.randint(2, 3)
                while len(motif) < target:
                    r, c = rng.choice(motif)
                    dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in seen:
                        motif.append((nr, nc))
                        seen.add((nr, nc))
                offset_r = rng.randint(-2, 2)
                offset_c = rng.randint(-3, 3)
                if offset_r == 0 and offset_c == 0:
                    continue
                placed_cells = [(pr + offset_r + dr, pc + offset_c + dc) for dr, dc in motif]
                if any(not (0 <= r < h and 0 <= c < w) for r, c in placed_cells):
                    continue
                rs = [r for r, _ in placed_cells]
                cs = [c for _, c in placed_cells]
                r1, c1 = min(rs), min(cs)
                r2, c2 = max(rs), max(cs)
                if not _free(g, r1, c1, r2, c2):
                    continue
                rotated = _rotate_cells_cw(placed_cells, (pr, pc), cmd)
                if any(not (0 <= r < h and 0 <= c < w) for r, c in rotated):
                    continue
                if any((r, c) in [(pp[0], pp[1]) for pp in pivots] for r, c in rotated):
                    continue
                for r, c in placed_cells:
                    g[r][c] = color
                placed_c = True
                break
            if not placed_c:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place pivots+components in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_pivots":
        # No color-8 — rule's pivot selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        return g
    if name == "no_command":
        # Pivot present but cell to its left is bg — command undefined.
        g[5][6] = 8
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        return g
    if name == "no_components":
        # Pivots present but no non-pivot components — rule has nothing
        # to rotate.
        g[5][2] = 2; g[5][3] = 8
        return g
    return g
