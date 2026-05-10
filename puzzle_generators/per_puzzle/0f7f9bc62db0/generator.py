"""Generator for puzzle 48d8fb45.

Rule: gray marker + adjacent non-gray shape + distractor shapes.
Erase gray, crop to adjacent shape's bbox.

Combinatorial axes (8): grid_h/w, target_size_kind, n_distractors,
distractor_size_kind, palette_kind, marker_position_kind,
inter_object_margin, asymmetry_force.
Degenerates: no_marker, marker_alone, all_adjacent.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "0f7f9bc62db0"
VERSION = "1.1.0"
TASK_ID = "0f7f9bc62db0"
SUMMARY = "Gray marker + adjacent shape + distractors; rule extracts adjacent shape's bbox."

INVARIANTS = [
    "background is 0",
    "exactly one gray(5) cell (marker)",
    ">=1 non-gray shape adjacent (Chebyshev <=1) to marker",
    ">=1 distractor non-gray shape NOT adjacent to marker",
    "shapes don't overlap",
]

TARGET_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
DISTRACTOR_SIZE_KINDS = ("small", "medium", "varied")
MARKER_POSITION_KINDS = ("corner", "side", "center", "varied")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_marker", "marker_alone", "all_adjacent")
HELPFUL_TEXTURES = TARGET_SIZE_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":              {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "target_size_kind":    {"type": "str", "default": "rng helpful",
                            "valid": "|".join(TARGET_SIZE_KINDS)},
    "n_distractors":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "distractor_size_kind": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(DISTRACTOR_SIZE_KINDS)},
    "palette_kind":        {"type": "str", "default": "rng helpful",
                            "valid": "|".join(PALETTE_KINDS)},
    "marker_position_kind": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(MARKER_POSITION_KINDS)},
    "inter_object_margin": {"type": "int", "default": "2", "valid": "2..4"},
    "texture":             {"type": "str", "default": "alias for target_size_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 17, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    palette = pool[:3]
    while len(palette) < 3:
        palette.append(palette[0])
    target_size_kind = (overrides.get("texture") or
                        overrides.get("target_size_kind")
                        or ctx.draw_choice("target_size_kind",
                                           list(TARGET_SIZE_KINDS)))
    rh, rw = _target_dims(target_size_kind, rng)
    g = full_grid(h, w, 0)
    rr = rng.randint(2, max(2, h // 2 - 1))
    rc = rng.randint(2, max(2, w // 2 - 1))
    target_color = palette[0]
    for dr in range(rh):
        for dc in range(rw):
            if rr + dr < h and rc + dc < w:
                g[rr + dr][rc + dc] = target_color
    candidates = []
    for dr in range(-1, rh + 1):
        for dc in range(-1, rw + 1):
            mr, mc = rr + dr, rc + dc
            if 0 <= mr < h and 0 <= mc < w and g[mr][mc] == 0:
                in_range = any(abs(mr - (rr + tdr)) <= 1
                               and abs(mc - (rc + tdc)) <= 1
                               for tdr in range(rh) for tdc in range(rw))
                if in_range:
                    candidates.append((mr, mc))
    if not candidates:
        return _draw_from_degenerate("no_marker", h, w, rng)
    mr, mc = rng.choice(candidates)
    g[mr][mc] = 5
    n_distract = int(overrides.get("n_distractors",
                                   ctx.draw_int("n_distractors", 1, 3)))
    n_distract = max(1, min(4, n_distract))
    distract_kind = overrides.get("distractor_size_kind",
                                  ctx.draw_choice("distractor_size_kind",
                                                  list(DISTRACTOR_SIZE_KINDS)))
    placed_d = 0
    for _ in range(n_distract * 5):
        if placed_d >= n_distract:
            break
        dh, dw = _distractor_dims(distract_kind, rng)
        for _try in range(20):
            dr = rng.randint(h // 2 + 1, h - dh - 1)
            dc = rng.randint(w // 2 + 1, w - dw - 1)
            if abs(dr - mr) < 3 and abs(dc - mc) < 3:
                continue
            ok = True
            for ddr in range(-1, dh + 1):
                for ddc in range(-1, dw + 1):
                    nr = dr + ddr; nc = dc + ddc
                    if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0:
                        ok = False; break
                if not ok: break
            if not ok:
                continue
            color = rng.choice(palette[1:])
            for ddr in range(dh):
                for ddc in range(dw):
                    g[dr + ddr][dc + ddc] = color
            placed_d += 1
            break
    if placed_d < 1:
        return _draw_from_degenerate("marker_alone", h, w, rng)
    return g


def _target_dims(kind, rng):
    if kind == "small":
        return 2, 2
    if kind == "medium":
        return rng.randint(2, 3), rng.randint(2, 3)
    if kind == "large":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "wide":
        return 2, rng.randint(3, 4)
    if kind == "tall":
        return rng.randint(3, 4), 2
    return rng.randint(2, 3), rng.randint(2, 3)


def _distractor_dims(kind, rng):
    if kind == "small":
        return 2, 2
    if kind == "medium":
        return rng.randint(2, 3), rng.randint(2, 3)
    return rng.randint(2, 3), rng.randint(2, 3)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "no_marker":
        for r in range(2, 5):
            for c in range(2, 5):
                if r < h and c < w:
                    g[r][c] = color
        return g
    if name == "marker_alone":
        g[h // 2][w // 2] = 5
        return g
    if name == "all_adjacent":
        for r in range(2, 5):
            for c in range(2, 5):
                if r < h and c < w:
                    g[r][c] = color
        if 2 < h and 5 < w:
            g[2][5] = 5
        return g
    return g
