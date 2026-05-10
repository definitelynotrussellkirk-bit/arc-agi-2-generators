# Generator authoring patterns

Working playbook for writing per-puzzle generators. Each pattern
captures: when to use it, what the input has to satisfy, common
failure modes that show up at smoke time, and a starter skeleton.

This is **not** a taxonomy for cataloguing every generator that has
ever shipped. It's a practical reference for the next medium/hard
generator. Add a pattern when you've used it 3+ times in real
generators; remove a pattern that hasn't been useful in 6+ months.

The seven patterns below cover the recurring shapes in the
~200 medium/hard generators that have already landed. The remaining
medium/hard backlog clusters into resistant families documented at
the bottom: graph-algorithmic, dihedral-matching, and
object-classification.

---

## 1. Frame fill

**When to use:** rule iterates rectangle frames (full-perimeter
non-bg objects) and fills their interior under some condition. The
trigger is usually a marker color present in the interior or in a
specific cell.

**Input invariants:**
- Background is 0.
- 1-2 frames in the chosen wall color. Each frame is exactly the
  bbox perimeter (not a solid rect).
- Each frame's interior holds the trigger that the rule looks for —
  often a single marker cell of a specific color.
- Frames don't touch each other (≥1 bg gap between bboxes).

**Smoke pitfalls:**
- Frame perimeter has a gap → object detection sees the frame as a
  blob, not a rect-border. Always paint via `draw_frame`.
- Interior color collides with the frame color — make `random_palette`
  exclude the frame color.
- Identity output: rule fires but the interior was already filled.

**Starter skeleton:**

```python
from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 9, 12)
    w = ctx.draw_int("grid_w", 12, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    needed = 2
    placed = []
    for _ in range(80):
        if len(placed) >= needed: break
        rh = rng.randint(4, 5); rw = rng.randint(4, 5)
        r1 = rng.randint(0, h - rh); c1 = rng.randint(0, w - rw)
        r2, c2 = r1 + rh - 1, c1 + rw - 1
        bb_pad = (r1 - 1, c1 - 1, r2 + 1, c2 + 1)
        if any(bbox_overlaps(bb_pad, (p[0]-1, p[1]-1, p[2]+1, p[3]+1)) for p in placed):
            continue
        placed.append((r1, c1, r2, c2))
    if len(placed) < needed:
        # Round-7 audit policy: invariant failures raise instead of
        # silently returning a partial grid that violates the
        # generator's own INVARIANTS list. The runner records this as
        # `generate.generator_raised`, which is easier to diagnose
        # than a structurally-valid-but-semantically-weak input.
        raise ValueError(f"could only place {len(placed)}/{needed} frames")
    for r1, c1, r2, c2 in placed:
        draw_frame(g, r1, c1, r2, c2, FRAME_COLOR)
        marker = rng.choice(list(random_palette(rng, 4, exclude={FRAME_COLOR})))
        sr = rng.randint(r1 + 1, r2 - 1)
        sc = rng.randint(c1 + 1, c2 - 1)
        g[sr][sc] = marker
    return g
```

**Examples in the corpus:** `set16:M108`, `set17:M115`, `set13:M85`,
`set12:M82`, `set6:M40`, `set7:M44`, `set10_s:S10_M2`,
`v3:medium_03`, `nineteenth21:M125`, `nineteenth21:M128`.

---

## 2. Sort + pack

**When to use:** rule extracts every connected non-bg object,
sorts by some property (size, height, hole count), and pastes the
crops side-by-side or stacked.

**Input invariants:**
- 2-3 connected non-bg objects in distinct colors.
- The sort key is **distinct** for every object so the order is
  unambiguous (size, height, area, hole count).
- Objects don't touch each other.

**Smoke pitfalls:**
- Sort tie → the rule's deterministic tiebreaker (top-row, left-col,
  color) decides, but your invariant doc should still say sizes are
  distinct so future readers don't mis-debug the generator.
- Output bigger than max grid dim — choose distinct sizes from a
  short menu.

**Examples:** `set12:M83` (hole count), `set14:M95`, `set16:M107`
(size DESC), `set11:k10`, `set7:M47` (solid rects only),
`set4:M23` (size ASC).

---

## 3. Marker-pair connect

**When to use:** rule finds same-color marker pairs in shared
row/col and fills the segment between (sometimes a rect outline if
they're diagonally placed).

**Input invariants:**
- 1-3 distinct non-bg colors, each with **exactly 2** markers.
- Each pair shares a row or column with ≥1 0-cell strictly between.
- Pairs use distinct rows and distinct cols (segments don't cross).
- (For "rect outline" variant: at least one pair is on different
  row AND different col.)

**Smoke pitfalls:**
- 3 same-color cells accidentally generated → the rule's "exactly 2"
  filter skips that color, so the pair never fires and output equals
  input.
- Markers in the same row at adjacent cols (no gap) → no fill, may
  fail `output_equals_input`.

**Examples:** `additional_bank:M5`, `set11:M71`, `set6:M42`,
`v1:M3`, `v3:medium_01`, `v2:M2` (line + rect-outline variant).

---

## 4. Stamp at every anchor

**When to use:** rule finds a small template (defined by an
anchor cell or by a connected non-bg blob), then stamps a copy of
that template at each of N anchor cells.

**Input invariants:**
- Template at one well-defined location (top-left, or anchored by a
  specific marker color like 8 or 9).
- 1-3 anchor cells elsewhere with **room** to land the template
  in-bounds.
- Anchors don't touch the template region.

**Smoke pitfalls:**
- Anchor too close to a grid edge → template stamps off-grid.
  Reserve a `template_h`/`template_w` margin when picking anchors.
- Anchor in a column that lands the template on top of another
  marker → rules typically tolerate this but the puzzle becomes
  ambiguous.

**Examples:** `set12:M82`, `set17:M118`, `set18:M120`
(rotated stamp), `eighteenth21:M124`, `nineteenth21:M130`.

---

## 5. Largest / smallest pick + crop

**When to use:** rule selects one specific object (largest, smallest,
most-holes, marker-color match) and outputs its bbox crop.

**Input invariants:**
- 2-3 connected objects, the chosen-by-property one is unambiguously
  best.
- For "marker-color match": cell (0,0) holds the target marker; the
  matching object has size ≥3 (single cells are usually filtered
  out).

**Smoke pitfalls:**
- All objects same size → tiebreaker decides, output may not match
  what your invariant doc says.
- Marker color collides with another object color → the rule's
  filter merges them.

**Examples:** `set16:M110` (most holes), `set17:M117`
(cmd-driven), `v0_original:medium_01` (largest), `v1:M5`
(erase largest), `set14_bundle:medium_n01`, `eighteenth21:M120`,
`eighteenth_21_bundle:medium_120`,
`nineteenth_21_bundle:medium_127`.

---

## 6. Recolor by property

**When to use:** rule recolors each connected object based on
something computable: cell count, line-vs-blob, hole count, dihedral
class, position rank.

**Input invariants:**
- N objects with **distinct** values of the property the rule
  consults (distinct sizes; or one line + one blob; etc.).
- Each in a distinct color so the rule's per-color path is clean.

**Smoke pitfalls:**
- Two objects share the property value → recolor map is ambiguous;
  output may be deterministic but not what invariant text claims.
- "Line" detection is bbox-based (h=1 or w=1) — make sure your line
  shapes are 1×N or N×1, not L-shapes.

**Examples:** `v0_original:medium_05` (size 1/2/3 → 3/2/1),
`v1:M1` (lines → 8), `v1:M6` (size rank → 1/2/3),
`eighteenth21:M123` (size legend), `set16:M111` (dihedral matrix).

---

## 7. Cmd-driven transform

**When to use:** rule reads a single command cell (often (0,0))
that selects which transform to apply (rotate, flip, transpose).
Output is the transformed crop of the rest of the grid or a chosen
object.

**Input invariants:**
- (0,0) holds a value in a known set (often {1, 2, 3, 4} or
  {2, 3, 4, 5, 6}).
- The rest of the grid satisfies whatever pattern the transform
  applies to (typically a single motif or N objects with distinct
  selector keys).

**Smoke pitfalls:**
- Transform leaves output identical to input → reject as
  `validate.output_equals_input`. Usually fixed by picking a cmd
  that actually changes the motif.
- Cmd cell collides with motif color — exclude cmd values from the
  motif palette.

**Examples:** `set12:M84` (4-corner cmd 2×2), `set18:M124`
(rotation), `set12_bundle:medium_l14` (per-marker cmd),
`set17:M117` (cmd at (0,0) picks object), `set16:M106`
(A:B::C:? transform analogy).

---

## Resistant clusters in the remaining hard backlog

Patterns that are *hard to generate for*, not because the input is
complex, but because the rule is algorithmically novel.

### Graph-algorithmic (~30% of remaining hards)

`arc_puzzle_bank_21_set12_s:S12_M*`, `set13_s:S13_M*`, ... All use
the same scaffold: build object adjacency graph → BFS/cluster →
extract by some graph property (degree, path, cluster ID).

**Why hard to generate:** input has to satisfy joint constraints —
"objects A and B must be adjacent, B and C must NOT be." Without
auto-mining the rule's adjacency conditions, designing inputs is
algorithmic work.

**Tactic:** skip these until a constraint-mining tool exists. A few
can be done by hand if the graph is small (≤4 objects), but the
ROI is poor.

### Dihedral matching (~25% of remaining hards)

`arc_puzzle_bank_*_21_bundle:medium_m0X`, `medium_n0X`. Rule
involves D₄ matching (rotations + reflections) of object shapes.

**Why hard to generate:** the rule classifies objects by their
dihedral equivalence class. To produce a deterministic puzzle, the
generator has to ensure objects are *unambiguously* in distinct
classes — and the 3-cell shapes most generators reach for first all
collapse to a single L-tromino class.

**Tactic:** use shapes with strictly different cell counts (3-cell
vs 4-cell vs 5-cell) so the classes are trivially distinct. Avoid
N-cell shapes that have D₄ symmetries (squares, rings) unless that's
deliberate.

### Object classification (~20% of remaining hards)

`arc_puzzle_bank_NTH21:M*` "keep all objects that satisfy P, erase
the rest" rules. Predicates seen so far: solid-rect, line-shaped,
symmetric, has-holes, on-border, single-color.

**Why hard to generate:** unlike "sort + pack", these rules don't
preserve all objects, so a smoke pitfall is that the output equals
input (no objects matched the predicate). The generator has to
ensure ≥1 object passes and ≥1 fails.

**Tactic:** explicitly include both a passing example (the right
shape) and a failing example (something obviously different), in
distinct colors.

### Individual one-offs (~25% of remaining hards)

These don't cluster. Each gets its own analysis. The
`scripts/sample_generator.py --show-rule` flag is the right
starting point — read the rule body next to the I/O examples.

---

## When NONE of these patterns fit

If the rule doesn't match any pattern above, that's data: either
the rule is genuinely novel, or there's a new pattern emerging.
Before writing the generator, write a one-line description of what
the rule does in plain English. If you can't, the generator will be
hard to design no matter what you do.
