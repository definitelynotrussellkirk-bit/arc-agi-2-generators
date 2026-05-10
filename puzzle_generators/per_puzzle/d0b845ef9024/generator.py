"""Generator for ARC task 42a50994.

Rule: erase isolated same-color pixels (cells with no 8-connected
neighbor of the same color).

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * fg_color               — the single fg color (canonical: one fg color)
  * cluster_count          — number of connected clusters to plant
  * cluster_kind           — shape of clusters: rect/L/blob/cross/line
  * cluster_size_dist      — small / medium / large / mixed
  * isolated_count         — number of isolated cells to plant (the
                             cells the rule will erase)
  * isolated_layout        — random / corners / row / column / scattered
  * caller-opt-in degenerates: only_clusters (no isolates → rule no-op),
                               only_isolates (rule erases everything),
                               all_isolated (uniformly sparse)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d0b845ef9024"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "d0b845ef9024"
SUMMARY = "Fg clusters + isolated pixels; the rule erases cells without an 8-neighbor."

INVARIANTS = [
    "background is zero",
    "foreground includes ≥1 connected cluster (cells survive the rule)",
    "foreground includes ≥1 isolated same-color pixel (cells the rule erases)",
]

CLUSTER_KINDS = ("rect", "L_shape", "blob", "cross", "line_h", "line_v")
SIZE_DISTRIBUTIONS = ("small", "medium", "large", "mixed")
ISOLATED_LAYOUTS = ("random", "corners", "row", "column", "scattered")
DEGENERATE_TEXTURES = ("only_clusters", "only_isolates", "all_isolated")
HELPFUL_TEXTURES = CLUSTER_KINDS

AXES = {
    "grid_h":            {"type": "int",   "default": "rng 8..16", "valid": "3..22"},
    "grid_w":            {"type": "int",   "default": "rng 8..16", "valid": "3..22"},
    "fg_color":          {"type": "color", "default": "rng",       "valid": "1..9"},
    "cluster_count":     {"type": "int",   "default": "rng 2..4",  "valid": "1..6"},
    "cluster_kind":      {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(CLUSTER_KINDS)},
    "cluster_size_dist": {"type": "str",   "default": "rng small|medium|large|mixed",
                          "valid": "|".join(SIZE_DISTRIBUTIONS)},
    "isolated_count":    {"type": "int",   "default": "rng 2..6",  "valid": "1..12"},
    "isolated_layout":   {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(ISOLATED_LAYOUTS)},
    "texture":           {"type": "str",   "default": "alias for cluster_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi, i_lo, i_hi = 8, 11, 1, 2, 2, 4
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi, i_lo, i_hi = 14, 16, 3, 4, 5, 8
    else:
        h_lo, h_hi, c_lo, c_hi, i_lo, i_hi = 8, 16, 2, 4, 2, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, ctx, rng)

    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    n_clusters = int(overrides.get("cluster_count",
                                   ctx.draw_int("cluster_count", c_lo, c_hi)))
    kind = (overrides.get("texture")
            or overrides.get("cluster_kind")
            or ctx.draw_choice("cluster_kind", list(CLUSTER_KINDS)))
    size_dist = overrides.get(
        "cluster_size_dist",
        ctx.draw_choice("cluster_size_dist", list(SIZE_DISTRIBUTIONS)))
    n_isolated = int(overrides.get("isolated_count",
                                   ctx.draw_int("isolated_count", i_lo, i_hi)))
    iso_layout = overrides.get(
        "isolated_layout",
        ctx.draw_choice("isolated_layout", list(ISOLATED_LAYOUTS)))

    g = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()

    placed_clusters = 0
    for _ in range(n_clusters):
        for _try in range(20):
            sh, sw = _cluster_dims(size_dist, h, w, rng)
            rr = rng.randint(0, max(0, h - sh))
            rc = rng.randint(0, max(0, w - sw))
            cells = _cluster_cells(kind, sh, sw)
            actual = [(rr + dr, rc + dc) for dr, dc in cells]
            # Need 1-cell buffer so isolated cells don't touch clusters.
            buffer = set()
            for r, c in actual:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        buffer.add((r + dr, c + dc))
            if any(p in occupied for p in buffer):
                continue
            for r, c in actual:
                if 0 <= r < h and 0 <= c < w:
                    g[r][c] = fg
                    occupied.add((r, c))
            placed_clusters += 1
            break

    if placed_clusters == 0:
        # Fallback: place a tiny cluster.
        g[1][1] = fg; g[1][2] = fg; g[2][1] = fg
        for r, c in [(1, 1), (1, 2), (2, 1)]:
            occupied.add((r, c))

    placed_isolated = 0
    iso_candidates = _isolated_candidates(iso_layout, h, w, rng)
    for r, c in iso_candidates:
        if placed_isolated >= n_isolated:
            break
        if (r, c) in occupied:
            continue
        # Check 8-neighborhood is clear.
        if any((r + dr, c + dc) in occupied
               for dr in (-1, 0, 1) for dc in (-1, 0, 1)
               if not (dr == 0 and dc == 0)):
            continue
        g[r][c] = fg
        occupied.add((r, c))
        placed_isolated += 1
    return g


def _cluster_dims(size_dist, h, w, rng):
    if size_dist == "small":
        return rng.randint(2, 3), rng.randint(2, 3)
    if size_dist == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if size_dist == "large":
        return rng.randint(4, max(4, h // 3)), rng.randint(4, max(4, w // 3))
    return rng.randint(2, max(3, h // 4)), rng.randint(2, max(3, w // 4))


def _cluster_cells(kind, sh, sw):
    if kind == "rect":
        return [(dr, dc) for dr in range(sh) for dc in range(sw)]
    if kind == "L_shape":
        out = [(dr, 0) for dr in range(sh)]
        out += [(sh - 1, dc) for dc in range(1, sw)]
        return out
    if kind == "blob":
        out = [(0, 0), (0, 1), (1, 0), (1, 1)]
        if sh > 2: out.append((2, 0))
        if sw > 2: out.append((0, 2))
        return out
    if kind == "cross":
        mr, mc = sh // 2, sw // 2
        out = [(mr, dc) for dc in range(sw)]
        out += [(dr, mc) for dr in range(sh) if dr != mr]
        return list(set(out))
    if kind == "line_h":
        return [(0, dc) for dc in range(sw)]
    if kind == "line_v":
        return [(dr, 0) for dr in range(sh)]
    return [(dr, dc) for dr in range(sh) for dc in range(sw)]


def _isolated_candidates(layout, h, w, rng):
    if layout == "corners":
        return [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    if layout == "row":
        r = rng.randint(0, h - 1)
        return [(r, c) for c in range(w)]
    if layout == "column":
        c = rng.randint(0, w - 1)
        return [(r, c) for r in range(h)]
    if layout == "scattered":
        cells = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(cells)
        return cells
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, ctx, rng):
    """Edge-case where the isolation-detection signal is hidden.

    only_clusters  — every fg cell is inside a cluster; no isolates,
                     so the rule has no work (output == input).
    only_isolates  — every fg cell is isolated; the rule erases all fg.
    all_isolated   — uniformly sparse with no clusters; same as
                     only_isolates but explicitly random scatter.
    """
    fg = ctx.draw_color("fg_color", exclude={0})
    g = full_grid(h, w, 0)
    if name == "only_clusters":
        rh, rw = max(2, h // 4), max(2, w // 4)
        rr = rng.randint(0, h - rh); rc = rng.randint(0, w - rw)
        for r in range(rr, rr + rh):
            for c in range(rc, rc + rw):
                g[r][c] = fg
        return g
    if name == "only_isolates":
        positions = [(r, c) for r in range(0, h, 3) for c in range(0, w, 3)]
        rng.shuffle(positions)
        for (r, c) in positions[:6]:
            g[r][c] = fg
        return g
    if name == "all_isolated":
        for r in range(0, h, 2):
            for c in range(0, w, 2):
                if rng.random() < 0.4:
                    g[r][c] = fg
        return g
    return g
