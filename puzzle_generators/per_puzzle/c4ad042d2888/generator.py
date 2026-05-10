"""Generator for arc_puzzle_bank_21_set14_bundle:hard_n07 — frame-area to object-size pairing.

Rule: 2-3 hollow color-8 frames of distinct interior areas, plus 2-3 solid
components in non-8 colors whose sizes equal those frame interior areas.
Output pastes each component into the frame whose area matches.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no 8-frames → no chambers);
no_solids (frames but no solids → nothing to place);
tied_areas (frames or solids with equal sizes → matching ambiguous).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c4ad042d2888"
VERSION = "1.1.0"
TASK_ID = "c4ad042d2888"

SUMMARY = "2-3 color-8 frames + 2-3 solid colored components whose sizes match frame interior areas."

INVARIANTS = [
    "background is 0",
    "2-3 hollow rectangular color-8 frames at distinct positions",
    "2-3 solid components in distinct non-{0, 8} colors",
    "for each component there is a frame whose interior area equals the component size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_solids", "tied_areas")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "n_pairs":           {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":     {"type": "str", "default": "frames_with_size_matched_solids",
                          "valid": "frames_with_size_matched_solids"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2, pad=1):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - pad), min(h, r2 + pad + 1)):
        for c in range(max(0, c1 - pad), min(w, c2 + pad + 1)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")

    interior_options = [(2, 2), (2, 3), (3, 2), (2, 4), (3, 3), (4, 2)]

    for outer in range(40):
        g = full_grid(h, w, 0)
        chosen = []
        for ih, iw in rng.sample(interior_options, n_pairs):
            chosen.append((ih, iw))
        areas = {ih * iw for ih, iw in chosen}
        if len(areas) != n_pairs:
            continue
        ok = True
        for ih, iw in chosen:
            fh, fw = ih + 2, iw + 2
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 8)
                placed = True; break
            if not placed:
                ok = False; break
        if not ok:
            continue
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_pairs)
        for (ih, iw), color in zip(chosen, colors):
            area = ih * iw
            cells = [(0, 0)]; seen = {(0, 0)}
            while len(cells) < area:
                r, c = rng.choice(cells)
                dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                nr, nc = r + dr, c + dc
                if (nr, nc) not in seen:
                    cells.append((nr, nc)); seen.add((nr, nc))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            placed_b = False
            for _ in range(120):
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
                if any(g[r][c] != 0 for r, c in cells_p): continue
                if not all(_free(g, rr, cc, rr, cc, pad=0) for rr, cc in cells_p): continue
                ok2 = True
                for rr, cc in cells_p:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = rr + dr, cc + dc
                            if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in cells_p and g[nr][nc] != 0:
                                ok2 = False; break
                        if not ok2: break
                    if not ok2: break
                if not ok2: continue
                for rr, cc in cells_p:
                    g[rr][cc] = color
                placed_b = True; break
            if not placed_b:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set14 n07 layout")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Solids only — no chambers.
        for r in range(2, 4):
            for c in range(3, 5):
                g[r][c] = 3
        for r in range(7, 9):
            for c in range(8, 11):
                g[r][c] = 5
        return g
    if name == "no_solids":
        # Frames only — nothing to pair.
        draw_frame(g, 1, 1, 4, 4, 8)
        draw_frame(g, 6, 8, 10, 13, 8)
        return g
    if name == "tied_areas":
        # Two frames with equal interior areas → matching ambiguous.
        draw_frame(g, 1, 1, 4, 4, 8)   # 2x2 interior
        draw_frame(g, 1, 9, 4, 12, 8)  # 2x2 interior
        for r in range(7, 9):
            for c in range(2, 4):
                g[r][c] = 3
        for r in range(7, 9):
            for c in range(8, 10):
                g[r][c] = 4
        return g
    return g
