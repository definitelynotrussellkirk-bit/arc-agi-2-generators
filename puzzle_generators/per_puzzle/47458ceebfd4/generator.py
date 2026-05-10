"""Generator for arc_additional_puzzles_21_set10_bundle:H67 — frame-local 2×2 tiling.

Rule: each rectangular color-8 border (frame) reads a 2×2 sample at
rows [r1-2, r1-1] cols [c1, c1+1] (relative to its top-left corner)
and tiles that sample periodically across its interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "47458ceebfd4"
VERSION = "1.1.0"
TASK_ID = "47458ceebfd4"

SUMMARY = "1-2 hollow 8-frames; each frame's interior is tiled from a 2×2 sample two rows above its top-left."

INVARIANTS = [
    "background is 0",
    "1 or 2 disjoint color-8 rectangular borders (4-conn), interior cells all 0",
    "each frame top-row r1 >= 2 (sample rows fit) and left-col c1 has c1+1 <= w-1",
    "the 2×2 sample area at rows [r1-2, r1-1], cols [c1, c1+1] has 1-4 non-zero non-{0,8} cells",
    "frame border + sample area do not collide with other frames or other samples",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w": {"type": "int", "default": "rng 12..15", "valid": "11..18"},
    "n_frames": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
}


def _free_box(g, r1, c1, r2, c2):
    """All cells in [r1, r2] x [c1, c2] are zero."""
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if r < 0 or r >= len(g) or c < 0 or c >= len(g[0]):
                return False
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 11, 13)
    w = ctx.draw_int("grid_w", 12, 15)
    n_frames = ctx.draw_int("n_frames", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(60):
        g = full_grid(h, w, 0)
        placed = 0
        ok = True
        for fi in range(n_frames):
            placed_this = False
            for _ in range(80):
                fh = rng.randint(4, 6)
                fw = rng.randint(4, 6)
                r1 = rng.randint(2, h - fh)
                c1 = rng.randint(0, w - fw)
                # require a 1-cell buffer around the frame so adjacent frames don't merge
                # frame footprint includes sample area at rows r1-2..r1-1, cols c1..c1+1
                # frame border at rows r1..r1+fh-1, cols c1..c1+fw-1
                if not _free_box(g, r1 - 2, c1, r1 - 1, c1 + 1):
                    continue
                if not _free_box(g, r1 - 1, c1 - 1, r1 + fh, c1 + fw):
                    continue
                if not _free_box(g, r1, c1, r1 + fh - 1, c1 + fw - 1):
                    continue
                # draw frame border
                draw_frame(g, r1, c1, r1 + fh - 1, c1 + fw - 1, 8)
                # paint 2×2 sample at (r1-2..r1-1, c1..c1+1) with 2-4 non-zero cells
                colors = rng.sample([1, 2, 3, 4, 6, 7, 9], 2)
                n_paint = rng.randint(2, 4)
                slots = [(r1 - 2, c1), (r1 - 2, c1 + 1), (r1 - 1, c1), (r1 - 1, c1 + 1)]
                rng.shuffle(slots)
                for i in range(n_paint):
                    pr, pc = slots[i]
                    g[pr][pc] = colors[i % 2]
                placed += 1
                placed_this = True
                break
            if not placed_this:
                ok = False
                break
        if ok and placed == n_frames:
            return g
    raise ValueError("could not place {0} frames in 60 attempts".format(n_frames))
