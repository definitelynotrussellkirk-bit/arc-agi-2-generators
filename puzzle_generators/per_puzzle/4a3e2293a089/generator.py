"""Generator for arc_puzzle_bank_21_set18_bundle:hard_p06 — dihedral match by guide color 1.

Rule: a color-1 guide motif. Among other components, find one whose dihedral
variant matches the guide's shape; output the matching component's bbox crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide (no color-1 motif → rule's guide selector finds
nothing), no_match (guide present but no candidate is dihedrally
equivalent → rule's match selector finds nothing), tied_match (≥2
candidates dihedrally equivalent → "the match" is ambiguous).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a3e2293a089"
VERSION = "1.1.0"
TASK_ID = "4a3e2293a089"

SUMMARY = "Color-1 guide + 2-3 candidates in distinct non-{0, 1} colors (one matches guide under dihedral)."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 guide motif (3-5 cells, connected)",
    "2-3 candidate motifs in distinct non-{0, 1} colors at separate positions",
    "at least one candidate has the same shape as the guide (modulo rotation/flip)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "n_others":          {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "guide_plus_candidates",
                          "valid": "guide_plus_candidates"},
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


def _normalize(cells):
    cs = list(cells)
    rmin = min(r for r, _ in cs); cmin = min(c for _, c in cs)
    return sorted((r - rmin, c - cmin) for r, c in cs)


def _rot(cells):
    return [(c, -r) for r, c in cells]


def _flip(cells):
    return [(r, -c) for r, c in cells]


def _variants(cells):
    out = set()
    cur = list(cells)
    for _ in range(4):
        out.add(tuple(_normalize(cur))); cur = _rot(cur)
    cur = _flip(cells)
    for _ in range(4):
        out.add(tuple(_normalize(cur))); cur = _rot(cur)
    return [list(v) for v in out]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
        n_others = ctx.draw_int("n_others", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 14, 14)
        n_others = ctx.draw_int("n_others", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
        n_others = ctx.draw_int("n_others", 2, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        guide = _normalize(_build_motif(rng, rng.randint(3, 5)))
        gh = max(r for r, _ in guide) + 1; gw = max(c for _, c in guide) + 1
        placed = False
        for _ in range(80):
            r0 = rng.randint(0, h - gh); c0 = rng.randint(0, w - gw)
            if not _free(g, r0, c0, r0 + gh - 1, c0 + gw - 1): continue
            for r, c in guide:
                g[r0 + r][c0 + c] = 1
            placed = True; break
        if not placed:
            continue
        match_v = rng.choice(_variants(guide))
        mh = max(r for r, _ in match_v) + 1; mw = max(c for _, c in match_v) + 1
        match_color = rng.choice([2, 3, 4, 5, 6, 7])
        placed_m = False
        for _ in range(80):
            r0 = rng.randint(0, h - mh); c0 = rng.randint(0, w - mw)
            if not _free(g, r0, c0, r0 + mh - 1, c0 + mw - 1): continue
            for r, c in match_v:
                g[r0 + r][c0 + c] = match_color
            placed_m = True; break
        if not placed_m:
            continue
        used = {match_color}
        for _ in range(n_others - 1):
            for _t in range(40):
                ocells = _normalize(_build_motif(rng, rng.randint(2, 4)))
                if tuple(ocells) in {tuple(v) for v in _variants(guide)}: continue
                oh = max(r for r, _ in ocells) + 1; ow = max(c for _, c in ocells) + 1
                color = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8] if c not in used])
                for _t2 in range(40):
                    r0 = rng.randint(0, h - oh); c0 = rng.randint(0, w - ow)
                    if not _free(g, r0, c0, r0 + oh - 1, c0 + ow - 1): continue
                    for r, c in ocells:
                        g[r0 + r][c0 + c] = color
                    used.add(color)
                    break
                break
        return g
    raise ValueError("could not realize set18 p06 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # No color-1 guide — rule's guide selector finds nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][7 + dc] = 6
        return g
    if name == "no_match":
        # Guide present but no dihedrally equivalent candidate.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[5 + dr][7 + dc] = 4   # H-line, not L
        return g
    if name == "tied_match":
        # Two candidates dihedrally equivalent — match ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[5 + dr][6 + dc] = 4   # rotated L
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[6 + dr][2 + dc] = 6   # another rotated L
        return g
    return g
