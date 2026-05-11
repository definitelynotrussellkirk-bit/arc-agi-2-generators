# ARC Additional Puzzle Bank — Solver-Style Companion
This is the companion pass after the 21-puzzle bank: the same tasks, but rewritten to feel native to your current solver loop. It emphasizes the `rule!` format, the `grid-from-fn` / `safe-at` idiom where possible, and helper-oriented sketches where the puzzle naturally wants richer object operations.
## How to read this file
- **Direct** means the sketch stays close to the low-level style shown in your solved example: local scans over `grid-from-fn`, `cell-at`, and `safe-at`.
- **Helper-dependent** means the rule is intentionally written against a small object-helper vocabulary analogous to the Python reference bank (`connected-components`, `rect-frames`, `bbox`, `crop-to-bbox`, and related helpers). These are good candidates for DSL/macros or librarian hints.
- Each puzzle includes a one-sentence written solution, a staged solve path, the main helper/primitive needs, a likely failure signature, and a solver-style program sketch.
## Assumed helper vocabulary for the object-heavy sketches
These names are intentionally close to the Python reference utilities from the first bank. They are not claimed to already exist in your runtime.
- `connected-components g color`
- `nonzero-components-anycolor g`
- `largest-component`, `component-size`, `component-bbox`
- `rect-frames g color`, `frame-contains-color?`, `fill-frame-interiors`
- `crop-to-bbox`, `find-singleton`, `cells-of-color`, `translate-cells`, `paint-cells`
- `first-full-row`, `first-full-col`, `draw-horizontal-run`, `draw-bars-with-gaps`

## Summary table
| ID | Difficulty | Style | Core skill | Helper needs |
|---|---|---|---|---|
| E1 | easy | direct | 2x2 diagonal completion | none |
| E2 | easy | direct | diagonal halo | none |
| E3 | easy | direct | one-gap line completion | none |
| E4 | easy | direct | horizontal segment endcaps | none |
| E5 | easy | direct | solid 2x2 block membership | none |
| E6 | easy | direct | fixed translation shadow | none |
| E7 | easy | direct | vertical triplet middle | none |
| M1 | medium | helper-dependent | seeded rectangular frames | rect-frames, frame-contains-color?, fill-frame-interiors |
| M2 | medium | helper-dependent | largest connected component | connected-components, largest-component |
| M3 | medium | helper-dependent | same-color endpoint bridge | find-color-cells, pairwise path fill |
| M4 | medium | helper-dependent | external marker projected into frame | rect-frames, outside-marker->stripe |
| M5 | medium | mostly direct | vertical mirror axis | first-full-col |
| M6 | medium | helper-dependent | L triomino filter | connected-components, bbox |
| M7 | medium | helper-dependent | crop largest nonzero object | nonzero-components-anycolor, bbox, crop-to-bbox |
| H1 | hard | helper-dependent | translate object by anchor vector | find-singleton, connected-components or color cells, paint-cells |
| H2 | hard | helper-dependent | extract template and stamp | rect-frames, extract-pattern, stamp-pattern |
| H3 | hard | mostly direct | choose row/col reflection axis | first-full-row, first-full-col |
| H4 | hard | helper-dependent | component count summary bar | connected-components, find-singleton, draw-run |
| H5 | hard | helper-dependent | rank frames by area | rect-frames, frame-area |
| H6 | hard | helper-dependent | deepest seeded frame only | rect-frames, frame-contains-color?, interior-contains? |
| H7 | hard | helper-dependent | sorted component-size bars | connected-components, sort, find-singleton, draw-run |

## Easy

### E1 — Diagonal Corner Completion
**Style:** direct  
**Written solution:** Look at every 2x2 window. If color 3 occupies one diagonal and the other diagonal is empty, fill the empty diagonal with 7.  
**Primitive/helper profile:** none

**Staged solve path**
- Detect the 2x2 windows that have opposite 3s.
- Mark only the missing diagonal corner cells, not the original 3s.
- Preserve everything else unchanged.

**Likely failure signature**
The common bad patch is to color orthogonal neighbors of 3 rather than the opposite corners of a 2x2 diagonal.

**Solver-style program**

```scheme
(define rule-e1
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (letrec ((hole?
                   (lambda (r c)
                     (or
                       ;; current cell is NW hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g r (+ c 1) 0) 3)
                            (= (safe-at g (+ r 1) c 0) 3)
                            (= (safe-at g (+ r 1) (+ c 1) 0) 0))
                       ;; current cell is NE hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g r (- c 1) 0) 3)
                            (= (safe-at g (+ r 1) c 0) 3)
                            (= (safe-at g (+ r 1) (- c 1) 0) 0))
                       ;; current cell is SW hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g (- r 1) c 0) 3)
                            (= (safe-at g r (+ c 1) 0) 3)
                            (= (safe-at g (- r 1) (+ c 1) 0) 0))
                       ;; current cell is SE hole
                       (and (= (safe-at g r c 0) 0)
                            (= (safe-at g (- r 1) c 0) 3)
                            (= (safe-at g r (- c 1) 0) 3)
                            (= (safe-at g (- r 1) (- c 1) 0) 0))))))
          (grid-from-fn h w
            (lambda (r c)
              (let ((v (cell-at g r c)))
                (if (and (= v 0) (hole? r c)) 7 v)))))))))
```

### E2 — Diagonal Halo
**Style:** direct  
**Written solution:** Each 3 paints its four diagonal neighbors with 7, clipped to the grid. The original 3s stay in place.  
**Primitive/helper profile:** none

**Staged solve path**
- Detect the source cells of color 3.
- For black cells only, check the four diagonal directions for a 3.
- Write 7 only on those diagonal neighbors.

**Likely failure signature**
A wrong rule usually paints orthogonal neighbors too, producing plus-sign halos instead of diagonals.

**Solver-style program**

```scheme
(define rule-e2
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or (= (safe-at g (- r 1) (- c 1) 0) 3)
                           (= (safe-at g (- r 1) (+ c 1) 0) 3)
                           (= (safe-at g (+ r 1) (- c 1) 0) 3)
                           (= (safe-at g (+ r 1) (+ c 1) 0) 3)))
                  7
                  v))))))))
```

### E3 — One-Gap Completion
**Style:** direct  
**Written solution:** Fill a black cell with 4 when it lies exactly between two 4s in a straight line, horizontally or vertically.  
**Primitive/helper profile:** none

**Staged solve path**
- Focus only on black cells.
- Test the left-right pattern and the up-down pattern independently.
- Promote the cell to 4 if either test succeeds.

**Likely failure signature**
Over-coverage usually comes from extending whole lines instead of filling only the single interior gap.

**Solver-style program**

```scheme
(define rule-e3
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or (and (= (safe-at g r (- c 1) 0) 4)
                                (= (safe-at g r (+ c 1) 0) 4))
                           (and (= (safe-at g (- r 1) c 0) 4)
                                (= (safe-at g (+ r 1) c 0) 4))))
                  4
                  v))))))))
```

### E4 — Bar Caps
**Style:** direct  
**Written solution:** For every horizontal run of at least two 6s, cap each open end with an 8 if that end cell is black.  
**Primitive/helper profile:** none

**Staged solve path**
- Detect black cells adjacent to a run of 6s.
- Require at least two 6s on one side so the run length is at least 2.
- Keep the write local: only the endcaps become 8.

**Likely failure signature**
A frequent miss is to extend the bar itself or to cap single isolated 6s; the length>=2 test matters.

**Solver-style program**

```scheme
(define rule-e4
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (or
                         ;; left endcap of a run to the right
                         (and (not (= (safe-at g r (- c 1) 0) 6))
                              (= (safe-at g r (+ c 1) 0) 6)
                              (= (safe-at g r (+ c 2) 0) 6))
                         ;; right endcap of a run to the left
                         (and (not (= (safe-at g r (+ c 1) 0) 6))
                              (= (safe-at g r (- c 1) 0) 6)
                              (= (safe-at g r (- c 2) 0) 6))))
                  8
                  v))))))))
```

### E5 — Solid Square Recolor
**Style:** direct  
**Written solution:** Recolor any 5 that belongs to a solid 2x2 block of 5s. Only those cells change, and they become 1.  
**Primitive/helper profile:** none

**Staged solve path**
- Treat each 5 as a candidate member of a 2x2 solid block.
- Check the four possible 2x2 placements around that cell.
- Recolor the cell to 1 if any placement is fully 5.

**Likely failure signature**
The typical false negative is checking only one anchor orientation, which misses cells in the same square seen from another corner.

**Solver-style program**

```scheme
(define rule-e5
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 5)
                       (or
                         ;; current is NW corner
                         (and (= (safe-at g (+ r 1) c 0) 5)
                              (= (safe-at g r (+ c 1) 0) 5)
                              (= (safe-at g (+ r 1) (+ c 1) 0) 5))
                         ;; current is NE corner
                         (and (= (safe-at g (+ r 1) c 0) 5)
                              (= (safe-at g r (- c 1) 0) 5)
                              (= (safe-at g (+ r 1) (- c 1) 0) 5))
                         ;; current is SW corner
                         (and (= (safe-at g (- r 1) c 0) 5)
                              (= (safe-at g r (+ c 1) 0) 5)
                              (= (safe-at g (- r 1) (+ c 1) 0) 5))
                         ;; current is SE corner
                         (and (= (safe-at g (- r 1) c 0) 5)
                              (= (safe-at g r (- c 1) 0) 5)
                              (= (safe-at g (- r 1) (- c 1) 0) 5))))
                  1
                  v))))))))
```

### E6 — Down-Right Shadow
**Style:** direct  
**Written solution:** Each 2 casts a one-cell shadow down-right. The new shadow cells are 5, and the original 2s remain.  
**Primitive/helper profile:** none

**Staged solve path**
- Keep all original cells by default.
- For a black cell, ask only whether its up-left neighbor is a 2.
- If yes, write 5 there.

**Likely failure signature**
Off-by-one errors show up as a full diagonal shift in the mask, especially when the shadow is written down-left or up-right instead.

**Solver-style program**

```scheme
(define rule-e6
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 0)
                       (= (safe-at g (- r 1) (- c 1) 0) 2))
                  5
                  v))))))))
```

### E7 — Vertical Middle Highlight
**Style:** direct  
**Written solution:** Whenever three 4s form a vertical triplet, recolor the middle cell to 9 and keep the other two unchanged.  
**Primitive/helper profile:** none

**Staged solve path**
- Scan only cells that are already 4.
- Check whether the cell has a 4 directly above and below.
- Recolor only the middle cell.

**Likely failure signature**
A common overreach is recoloring the whole triplet instead of just the center.

**Solver-style program**

```scheme
(define rule-e7
  (rule!
    (lambda (g)
      (let ((h (rows g)) (w (cols g)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (and (= v 4)
                       (= (safe-at g (- r 1) c 0) 4)
                       (= (safe-at g (+ r 1) c 0) 4))
                  9
                  v))))))))
```

## Medium

### M1 — Seeded Frame Fill
**Style:** helper-dependent  
**Written solution:** Find hollow rectangular 1-frames. If a frame's interior contains a 2, fill that whole interior with 4.  
**Primitive/helper profile:** rect-frames, frame-contains-color?, fill-frame-interiors

**Staged solve path**
- Detect rectangular 1-frames first; do not reason about seeds before the frame geometry is fixed.
- Classify each frame by whether its interior contains at least one 2.
- Fill only the qualifying interiors.

**Likely failure signature**
If the model paints the frame border itself or fills every frame regardless of seed, the object/frame split is off.

**Solver-style program**

```scheme
(define rule-m1
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 1))
             (seeded (filter (lambda (fr) (frame-contains-color? g fr 2))
                             frames)))
        (fill-frame-interiors g seeded 4)))))
```

### M2 — Largest 3-Component
**Style:** helper-dependent  
**Written solution:** Split the 3s into connected components, choose the largest one, and recolor only that component to 8.  
**Primitive/helper profile:** connected-components, largest-component, paint-component

**Staged solve path**
- Build the connected components of color 3.
- Compare their sizes globally.
- Paint only the largest component.

**Likely failure signature**
The usual wrong family is recoloring all 3s or the first component encountered instead of the largest one.

**Solver-style program**

```scheme
(define rule-m2
  (rule!
    (lambda (g)
      (let* ((comps (connected-components g 3))
             (best (largest-component comps)))
        (paint-component g best 8)))))
```

### M3 — Straight Bridge
**Style:** helper-dependent  
**Written solution:** For any color that appears exactly twice, if its two cells lie on one row or one column with only black cells between them, fill the straight path with that color.  
**Primitive/helper profile:** positions-by-color, aligned-pair?, clear-corridor?, paint-bridge

**Staged solve path**
- Group nonzero cells by color.
- Keep only colors that occur exactly twice.
- If the pair is aligned and the corridor is black, fill the corridor.

**Likely failure signature**
Bad rules often bridge diagonally or bridge colors that appear more than twice.

**Solver-style program**

```scheme
(define rule-m3
  (rule!
    (lambda (g)
      (let* ((pairs (colors-with-exactly-two-cells g))
             (usable (filter (lambda (entry)
                               (let ((cells (cdr entry)))
                                 (and (aligned-pair? cells)
                                      (clear-corridor? g cells))))
                             pairs)))
        (paint-bridges g usable)))))
```

### M4 — Frame Stripe from External Marker
**Style:** helper-dependent  
**Written solution:** A 7 marker just outside a 5-frame projects a stripe through that frame's interior: vertical if the marker is above/below, horizontal if it is left/right.  
**Primitive/helper profile:** rect-frames, frame-outside-markers, stripe-from-marker, paint-cells

**Staged solve path**
- Detect the 5-frame and only then search one cell outside each side for a 7.
- Convert the marker position into an interior row or column index.
- Paint the projected stripe with 3.

**Likely failure signature**
If the painted stripe lands on the border instead of the interior, the projection step is off by one.

**Solver-style program**

```scheme
(define rule-m4
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 5))
             (stripes (flatten
                        (map (lambda (fr)
                               (markers->interior-stripes g fr 7))
                             frames))))
        (paint-cells g stripes 3)))))
```

### M5 — Vertical Mirror Divider
**Style:** mostly direct  
**Written solution:** A full vertical column of 9 is the mirror axis. Reflect every nonzero, non-9 cell on the left onto the right side.  
**Primitive/helper profile:** first-full-col

**Staged solve path**
- Find the unique full 9 column.
- For each empty target cell, look at its reflected source cell on the left.
- Copy the source color if it is nonzero and not 9.

**Likely failure signature**
False positives on the left side mean the rule is mirroring both directions instead of using the left as source and right as target.

**Solver-style program**

```scheme
(define rule-m5
  (rule!
    (lambda (g)
      (let* ((h (rows g))
             (w (cols g))
             (axis (first-full-col g 9)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (not (= v 0))
                  v
                  (let ((src-c (- (* 2 axis) c))
                        (src (safe-at g r (- (* 2 axis) c) 0)))
                    (if (and (< c w)
                             (>= c 0)
                             (not (= src 0))
                             (not (= src 9)))
                        src
                        0))))))))))
```

### M6 — L-Triomino Filter
**Style:** helper-dependent  
**Written solution:** Among the connected components of color 6 that have exactly three cells, recolor only the L-shaped ones to 1. Straight triominoes stay 6.  
**Primitive/helper profile:** connected-components, component-bbox, bbox-height, bbox-width, paint-component

**Staged solve path**
- Find the connected 6-components and keep only size-3 components.
- Use the bounding box: 2x2 means L-shaped; 1x3 or 3x1 means straight.
- Paint only the qualifying components.

**Likely failure signature**
If straight triominoes also change, the shape test is too weak; the 2x2 bounding-box check is the clean discriminator.

**Solver-style program**

```scheme
(define rule-m6
  (rule!
    (lambda (g)
      (let* ((comps (connected-components g 6))
             (ells  (filter (lambda (comp)
                              (and (= (component-size comp) 3)
                                   (let* ((bb (component-bbox comp))
                                          (bh (bbox-height bb))
                                          (bw (bbox-width bb)))
                                     (and (= bh 2) (= bw 2)))))
                            comps)))
        (paint-components g ells 1)))))
```

### M7 — Crop the Largest Object
**Style:** helper-dependent  
**Written solution:** Treat each connected nonzero object as one object even if it has multiple colors. Output only the bounding box of the largest such object.  
**Primitive/helper profile:** nonzero-components-anycolor, largest-component, component-bbox, crop-to-bbox

**Staged solve path**
- Build connected components over nonzero cells without splitting by color.
- Select the largest one by cell count.
- Crop the grid to that component's bounding box.

**Likely failure signature**
The wrong family often splits a multicolor object into separate monochrome pieces and crops the wrong one.

**Solver-style program**

```scheme
(define rule-m7
  (rule!
    (lambda (g)
      (let* ((objs (nonzero-components-anycolor g))
             (best (largest-component objs))
             (bb   (component-bbox best)))
        (crop-to-bbox g bb)))))
```

## Hard

### H1 — Translate by Anchor Vector
**Style:** helper-dependent  
**Written solution:** Compute the vector from the single 1 marker to the single 2 marker. Copy the 3-object by that same vector and recolor the translated copy to 8.  
**Primitive/helper profile:** find-singleton, cells-of-color, translate-cells, paint-cells

**Staged solve path**
- Find the singleton 1 and singleton 2 first; do not move anything until the vector is known.
- Collect the cells of the 3-object.
- Translate that object by the anchor vector and paint the translated copy as 8.

**Likely failure signature**
A very common miss is translating from the 2 back to the 1, which flips the output to the wrong side.

**Solver-style program**

```scheme
(define rule-h1
  (rule!
    (lambda (g)
      (let* ((p1  (find-singleton g 1))
             (p2  (find-singleton g 2))
             (obj (cells-of-color g 3))
             (dr  (- (car p2) (car p1)))
             (dc  (- (cdr p2) (cdr p1)))
             (dst (translate-cells obj dr dc)))
        (paint-cells g dst 8)))))
```

### H2 — Prototype Stamp from Framed Template
**Style:** helper-dependent  
**Written solution:** Extract the interior 4-pattern from the 1-frame, then stamp that pattern at every 7 seed, recolored to 8.  
**Primitive/helper profile:** rect-frames, frame-interior-bitmap, has-color?, seeds-of-color, stamp-pattern

**Staged solve path**
- Detect the 1-frame that actually contains 4s.
- Read its interior as a binary template: 4 means on, everything else means off.
- For each 7 seed, stamp the template with color 8 using the seed as the template origin.

**Likely failure signature**
If the stamped copy is shifted or transposed, the template origin convention is inconsistent between extraction and stamping.

**Solver-style program**

```scheme
(define rule-h2
  (rule!
    (lambda (g)
      (let* ((frames   (rect-frames g 1))
             (source   (first (filter (lambda (fr) (frame-contains-color? g fr 4))
                                      frames)))
             (pattern  (frame-interior-bitmap g source 4))
             (seeds    (cells-of-color g 7)))
        (stamp-patterns g pattern seeds 8)))))
```

### H3 — Axis-Chooser Reflection
**Style:** mostly direct  
**Written solution:** A complete row or column of 9 is the reflection axis. Reflect all nonzero, non-9 cells across that axis using the same colors.  
**Primitive/helper profile:** first-full-row, first-full-col

**Staged solve path**
- Determine whether the full 9 guide is a row or a column.
- For each empty target cell, compute its reflected source cell across that axis.
- Copy the reflected source value if it is nonzero and not 9.

**Likely failure signature**
If the rule only works for vertical axes or only for horizontal axes, the axis-choice branch is missing.

**Solver-style program**

```scheme
(define rule-h3
  (rule!
    (lambda (g)
      (let* ((h (rows g))
             (w (cols g))
             (axis-r (first-full-row g 9))
             (axis-c (first-full-col g 9)))
        (grid-from-fn h w
          (lambda (r c)
            (let ((v (cell-at g r c)))
              (if (not (= v 0))
                  v
                  (cond
                    ((not (false? axis-r))
                     (let ((src (safe-at g (- (* 2 axis-r) r) c 0)))
                       (if (and (not (= src 0)) (not (= src 9))) src 0)))
                    ((not (false? axis-c))
                     (let ((src (safe-at g r (- (* 2 axis-c) c) 0)))
                       (if (and (not (= src 0)) (not (= src 9))) src 0)))
                    (else 0))))))))))
```

### H4 — Component Count Bar
**Style:** helper-dependent  
**Written solution:** Count the connected components of color 6. Starting immediately to the right of the single 2 marker, draw that many 3s as one horizontal bar.  
**Primitive/helper profile:** connected-components, find-singleton, draw-horizontal-run

**Staged solve path**
- Count the 6-components before drawing anything.
- Locate the single 2 marker.
- Draw a horizontal run of 3s whose length equals the component count.

**Likely failure signature**
If the bar length equals the number of 6 cells rather than components, the model is counting mass instead of objects.

**Solver-style program**

```scheme
(define rule-h4
  (rule!
    (lambda (g)
      (let* ((n  (length (connected-components g 6)))
             (p2 (find-singleton g 2)))
        (draw-horizontal-run g (car p2) (+ (cdr p2) 1) n 3)))))
```

### H5 — Smallest and Largest Frame Fill
**Style:** helper-dependent  
**Written solution:** Among the rectangular 4-frames, fill the smallest interior with 2 and the largest interior with 8. Middle-sized frames stay unchanged.  
**Primitive/helper profile:** rect-frames, frame-interior-area, smallest-by, largest-by, fill-frame-interior

**Staged solve path**
- Detect all hollow rectangular 4-frames.
- Rank them by interior area, not border length.
- Fill the smallest and largest interiors differently.

**Likely failure signature**
A common bug is to rank by overall bounding-box area including the border, which changes nothing here but breaks generalization later.

**Solver-style program**

```scheme
(define rule-h5
  (rule!
    (lambda (g)
      (let* ((frames (rect-frames g 4))
             (small  (smallest-frame-by-interior-area frames))
             (large  (largest-frame-by-interior-area frames)))
        (fill-frame-interiors
          (fill-frame-interiors g (list small) 2)
          (list large)
          8)))))
```

### H6 — Deepest Seeded Frame
**Style:** helper-dependent  
**Written solution:** Fill a seeded 1-frame only if it is the deepest seeded frame in its nesting chain. An outer seeded frame stays unchanged when it contains a smaller seeded frame that is also seeded.  
**Primitive/helper profile:** rect-frames, frame-contains-color?, interior-contains?, fill-frame-interiors

**Staged solve path**
- Find all 1-frames and then mark which ones are seeded by a 2 in the interior.
- Compare seeded frames by containment.
- Fill only those seeded frames that contain no smaller seeded frame inside them.

**Likely failure signature**
If both outer and inner seeded frames fill, the containment filter is missing.

**Solver-style program**

```scheme
(define rule-h6
  (rule!
    (lambda (g)
      (let* ((frames  (rect-frames g 1))
             (seeded  (filter (lambda (fr) (frame-contains-color? g fr 2)) frames))
             (deepest (filter (lambda (fr)
                                (not (ormap (lambda (other)
                                              (and (not (equal? fr other))
                                                   (interior-contains? fr other)))
                                            seeded)))
                              seeded)))
        (fill-frame-interiors g deepest 3)))))
```

### H7 — Sorted Component-Size Bars
**Style:** helper-dependent  
**Written solution:** Measure the size of every connected 6-component, sort the sizes from largest to smallest, and draw one bar of 3s per size starting to the right of the 2 marker, with one black cell between bars.  
**Primitive/helper profile:** connected-components, component-size, sort-desc, find-singleton, draw-bars-with-gaps

**Staged solve path**
- Extract the 6-components and measure their sizes.
- Sort the sizes descending.
- Render one bar per size from the 2 marker with single-cell gaps between bars.

**Likely failure signature**
If the bars appear in scan order rather than size order, the counting step is right but the ranking step is missing.

**Solver-style program**

```scheme
(define rule-h7
  (rule!
    (lambda (g)
      (let* ((sizes (sort-desc (map component-size (connected-components g 6))))
             (p2    (find-singleton g 2)))
        (draw-bars-with-gaps g (car p2) (+ (cdr p2) 1) sizes 3)))))
```
