"""Generator for puzzle 4cd1b7b2.

Rule: 4×4 Latin square (values 1..4) with some cells erased. 3 passes
of: each 0-cell with exactly 1 candidate (not in row, not in col)
gets filled.

Combinatorial axes (8): n_erased, base_kind, erasure_pattern,
erasure_density, row_perm, col_perm, anchor_corner, asymmetry_force.
Degenerates: full_grid, no_erasure, all_erased.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "135219aecdb4"
VERSION = "1.1.0"
TASK_ID = "135219aecdb4"
SUMMARY = "4x4 Latin square (vals 1..4) with cells erased to 0."

INVARIANTS = [
    "h = w = 4",
    "non-zero cells form valid partial Latin square",
    ">=1 and <=10 cells are 0",
    "puzzle solvable by row/col elimination within 3 passes",
]

ERASURE_PATTERNS = ("scattered", "row_focus", "col_focus", "diagonal",
                    "corners", "centered", "checker")
DEGENERATE_TEXTURES = ("full_grid", "no_erasure", "all_erased")
HELPFUL_TEXTURES = ERASURE_PATTERNS

AXES = {
    "n_erased":          {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "erasure_pattern":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(ERASURE_PATTERNS)},
    "base_kind":         {"type": "int", "default": "rng 0..3",
                          "valid": "0..3"},
    "row_perm":          {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "col_perm":          {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for erasure_pattern",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BASES = [
    [[1, 2, 3, 4], [3, 4, 1, 2], [4, 3, 2, 1], [2, 1, 4, 3]],
    [[1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 1, 2], [4, 3, 2, 1]],
    [[1, 2, 3, 4], [4, 3, 2, 1], [2, 1, 4, 3], [3, 4, 1, 2]],
    [[1, 4, 2, 3], [4, 1, 3, 2], [2, 3, 4, 1], [3, 2, 1, 4]],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 1, 3
    elif difficulty == "hard":
        n_lo, n_hi = 5, 8
    else:
        n_lo, n_hi = 2, 5
    n_erase = int(overrides.get("n_erased",
                                ctx.draw_int("n_erased", n_lo, n_hi)))
    n_erase = max(1, min(10, n_erase))
    base_idx = int(overrides.get("base_kind",
                                 ctx.draw_int("base_kind", 0, 3)))
    base_idx = max(0, min(3, base_idx))
    base = [row[:] for row in _BASES[base_idx]]
    rows = list(range(4))
    cols = list(range(4))
    if bool(overrides.get("row_perm", True)):
        rng.shuffle(rows)
    if bool(overrides.get("col_perm", True)):
        rng.shuffle(cols)
    g = [[base[rows[r]][cols[c]] for c in range(4)] for r in range(4)]
    pattern = (overrides.get("texture") or
               overrides.get("erasure_pattern")
               or ctx.draw_choice("erasure_pattern",
                                  list(ERASURE_PATTERNS)))
    erase_cells = _pick_erase_cells(pattern, n_erase, rng)
    for r, c in erase_cells:
        g[r][c] = 0
    return g


def _pick_erase_cells(pattern, n, rng):
    all_cells = [(r, c) for r in range(4) for c in range(4)]
    if pattern == "scattered":
        rng.shuffle(all_cells)
        return all_cells[:n]
    if pattern == "row_focus":
        r = rng.randint(0, 3)
        cs = list(range(4))
        rng.shuffle(cs)
        return [(r, c) for c in cs[:min(n, 4)]] + \
               rng.sample([(rr, cc) for rr in range(4) for cc in range(4)
                            if rr != r], max(0, n - 4))
    if pattern == "col_focus":
        c = rng.randint(0, 3)
        rs = list(range(4))
        rng.shuffle(rs)
        return [(r, c) for r in rs[:min(n, 4)]] + \
               rng.sample([(rr, cc) for rr in range(4) for cc in range(4)
                            if cc != c], max(0, n - 4))
    if pattern == "diagonal":
        diag = [(i, i) for i in range(4)]
        rng.shuffle(diag)
        rest = [(r, c) for r in range(4) for c in range(4) if r != c]
        rng.shuffle(rest)
        return (diag + rest)[:n]
    if pattern == "corners":
        corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
        rng.shuffle(corners)
        rest = [(r, c) for r in range(4) for c in range(4)
                if (r, c) not in corners]
        rng.shuffle(rest)
        return (corners + rest)[:n]
    if pattern == "centered":
        center = [(1, 1), (1, 2), (2, 1), (2, 2)]
        rng.shuffle(center)
        rest = [(r, c) for r in range(4) for c in range(4)
                if (r, c) not in center]
        rng.shuffle(rest)
        return (center + rest)[:n]
    if pattern == "checker":
        cells = [(r, c) for r in range(4) for c in range(4)
                 if (r + c) % 2 == 0]
        rng.shuffle(cells)
        if len(cells) < n:
            rest = [(r, c) for r in range(4) for c in range(4)
                    if (r + c) % 2 == 1]
            rng.shuffle(rest)
            cells.extend(rest)
        return cells[:n]
    rng.shuffle(all_cells)
    return all_cells[:n]


def _draw_from_degenerate(name, rng):
    base = [row[:] for row in rng.choice(_BASES)]
    if name == "full_grid":
        # No erasure — rule has no work
        return base
    if name == "no_erasure":
        return base
    if name == "all_erased":
        # Too many erased — unsolvable in 3 passes
        return [[0] * 4 for _ in range(4)]
    return base
