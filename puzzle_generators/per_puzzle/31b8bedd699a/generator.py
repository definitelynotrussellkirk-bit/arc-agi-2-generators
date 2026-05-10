"""Generator for a680ac02.

Rule: extract hollow frames from a mix of solid and hollow rectangles
and arrange them in a row or column.

Combinatorial axes (8): grid_h/w, n_frames, n_solids, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_frames, all_solid, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect, draw_rect_outline

GENERATOR_ID = "31b8bedd699a"
VERSION = "1.1.0"
TASK_ID = "31b8bedd699a"
SUMMARY = "Mix of solid and hollow boxes; rule extracts hollow frames and arranges them."

INVARIANTS = [
    "background is 0",
    "at least two hollow rectangular frames each as a perimeter outline",
    "zero to two solid rectangles which the rule filters out",
    "boxes are non-overlapping with margin of at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "all_solid", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 18..24", "valid": "15..30"},
    "grid_w":         {"type": "int", "default": "rng 18..24", "valid": "15..30"},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "n_solids":       {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, nf_lo, nf_hi = 18, 20, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, nf_lo, nf_hi = 22, 28, 3, 5
    else:
        h_lo, h_hi, nf_lo, nf_hi = 18, 24, 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_frames = ctx.draw_int("n_frames", nf_lo, nf_hi)
    n_solids = ctx.draw_int("n_solids", 0, 2)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    g = full_grid(h, w, 0)
    placed_boxes = []

    def _place(is_frame, attempts=60):
        for _ in range(attempts):
            bh = rng.randint(4, max(4, h // 4))
            bw = rng.randint(4, max(4, w // 4))
            rr = rng.randint(1, h - bh - 1)
            rc = rng.randint(1, w - bw - 1)
            ok = True
            for (or1, oc1, or2, oc2) in placed_boxes:
                if (rr - 1 <= or2 and rr + bh >= or1
                        and rc - 1 <= oc2 and rc + bw >= oc1):
                    ok = False; break
            if not ok:
                continue
            color = rng.choice(palette)
            if is_frame:
                draw_rect_outline(g, rr, rc, bh, bw, color)
            else:
                draw_rect(g, rr, rc, bh, bw, color)
            placed_boxes.append((rr, rc, rr + bh - 1, rc + bw - 1))
            return True
        return False

    n_frames_actually = 0
    for _ in range(n_frames):
        if _place(True):
            n_frames_actually += 1
    for _ in range(n_solids):
        _place(False)
    if n_frames_actually < 2:
        return [[0]]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = list(range(1, 10))
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 18, 18
    g = full_grid(h, w, 0)
    if name == "no_frames":
        draw_rect(g, 2, 2, 5, 5, 2)
        return g
    if name == "all_solid":
        draw_rect(g, 2, 2, 4, 4, 2)
        draw_rect(g, 8, 8, 4, 4, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
