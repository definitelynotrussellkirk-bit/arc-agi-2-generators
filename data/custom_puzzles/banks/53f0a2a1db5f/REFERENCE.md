# ARC-style Puzzle Bank — 21 more puzzles (set 15)

This fifteenth bank leans into **local frames** instead of global coordinates. Many ARC tasks become easier once an object is no longer treated as “cells somewhere on the board” but as a **portable stencil of relative offsets**. That perspective lets you copy shapes to new anchors, compare objects without caring where they sit, mirror or rotate a template before stamping it, and even build symbolic outputs such as indicator rows and congruence matrices.

The core primitive introduced here is:

```text
relative_offsets(cells, anchor='top_left')
  Return the occupied offsets of a component relative to a chosen anchor or corner. This makes translation-invariant shape comparison, anchor-relative copy, local stencil transfer, and transform-coded stamping explicit.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set15_reference.py`.

## Index

### Easy

- **S15_E1** — Copy the Template to the Single Marker

- **S15_E2** — Stamp the Template at All Seeds

- **S15_E3** — Horizontally Mirror the Template at the Marker

- **S15_E4** — Crop the Candidate Congruent to the Source

- **S15_E5** — Use the Source as a Mask on the Target Rectangle

- **S15_E6** — Copy by Preserving Offsets from the Source Anchor

- **S15_E7** — Indicator Row of Congruent Candidates


### Medium

- **S15_M1** — Transfer the Whole Multicolor Pattern to the Marker

- **S15_M2** — Stamp the Template in Each Marker's Color

- **S15_M3** — Rotate the Template 90 Degrees at the Marker

- **S15_M4** — Transform-Coded Stamps

- **S15_M5** — Stamp the XOR of Two Templates

- **S15_M6** — Crop the Majority Shape

- **S15_M7** — Indicator Row of Source-or-Mirror Matches


### Hard

- **S15_H1** — Learn that the Marker Means the Bottom-Right Corner

- **S15_H2** — Anchor-Frame Transform Copy

- **S15_H3** — Pairwise Congruence Matrix

- **S15_H4** — Multicolor Transform-Coded Stamps

- **S15_H5** — Header Chooses the Set Operation

- **S15_H6** — Priority Stamps with Walls

- **S15_H7** — Crop the Odd Shape under Rotation or Reflection



# Easy

## S15_E1 — Copy the Template to the Single Marker
**Skills:** translation invariance, single-anchor stamping, normalization by top-left

**Primitive note:** This is the most direct use of relative_offsets: normalize the source object to its top-left and replay those offsets at the marker.

**Scaffold:**

- Find the unique template object.

- Measure every occupied cell relative to the template's top-left corner.

- Recreate those same offsets at the single marker cell.

**Train 1 input**

```text
000000000000
020000000000
020000000000
022000000000
000000010000
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
000000000000
000000000000
000000080000
000000080000
000000088000
000000000000
```
**Train 2 input**

```text
000000000000
010000000000
000000000000
000000002000
000000022200
000000000000
000000000000
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
008000000000
088800000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000000010000
0000000000000
0000000000000
0022000000000
0002200000000
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000088000
0000000008800
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** Take the source object's occupied cells and convert them into offsets from the source object's top-left corner. Then ignore the original source position and place the same pattern at the marker. The output is a blank grid except for that copied pattern, recolored to 8.

**Reference program**

```python
def solve_S15_E1(grid):
    return copy_template_to_marker(grid)
```
## S15_E2 — Stamp the Template at All Seeds
**Skills:** template reuse, multi-seed stamping, translation invariance

**Primitive note:** The same relative offset set is reused at every seed, so one normalized template explains all copies.

**Scaffold:**

- Extract one normalized template from the source object.

- Locate every seed cell.

- Stamp the same template at each seed position.

**Train 1 input**

```text
00000000000000
02020000010000
02220000000000
00000000000000
00000000000000
00000000100000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**

```text
00000000000000
00000000080800
00000000088800
00000000000000
00000000000000
00000000808000
00000000888000
00000000000000
00000000000000
```
**Train 2 input**

```text
00000000100000
00000000000000
00000000000000
00000000000000
02200000010000
02200000000000
00200010000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**

```text
00000000880000
00000000880000
00000000080000
00000000000000
00000000088000
00000000088000
00000088008000
00000088000000
00000008000000
00000000000000
```
**Test input**

```text
00000000000000
00000000100000
02200000000000
02000000000000
02200000000000
00000000010000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test output**

```text
00000000000000
00000000880000
00000000800000
00000000880000
00000000000000
00000000088000
00000000080000
00000000088000
00000000000000
00000000000000
```
**Written solution:** Compute the template once by listing the source object's occupied offsets from its top-left corner. Then, for every seed marker, place the same set of offsets into the output grid. All copied cells become color 8 and the original template is not kept.

**Reference program**

```python
def solve_S15_E2(grid):
    return stamp_template_all_markers(grid)
```
## S15_E3 — Horizontally Mirror the Template at the Marker
**Skills:** reflection, bounding-box reasoning, anchor-relative copy

**Primitive note:** Use relative_offsets, but reflect the normalized offsets across the template's vertical axis before stamping.

**Scaffold:**

- Normalize the source object inside its tight bounding box.

- Mirror the occupied offsets left-to-right inside that box.

- Stamp the mirrored version at the marker.

**Train 1 input**

```text
00000000000000
02000000000000
02000000000000
02200000000000
00000000100000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000080000
00000000080000
00000000880000
00000000000000
```
**Train 2 input**

```text
0000000000000
0000000002000
0000000002000
0000000022000
0100000000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0800000000000
0800000000000
0880000000000
0000000000000
```
**Test input**

```text
00000000000000
00000000100000
00000000000000
00000000000000
00220000000000
00200000000000
00220000000000
00000000000000
00000000000000
```
**Test output**

```text
00000000000000
00000000880000
00000000080000
00000000880000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Written solution:** First normalize the template to its tight bounding box. Inside that box, flip every occupied cell horizontally so the left side becomes the right side. Then place that mirrored pattern at the marker and recolor it to 8.

**Reference program**

```python
def solve_S15_E3(grid):
    return hmirror_to_marker(grid)
```
## S15_E4 — Crop the Candidate Congruent to the Source
**Skills:** shape matching, congruence under translation, cropping

**Primitive note:** The candidate search uses relative_offsets as a translation-invariant signature.

**Scaffold:**

- Normalize the source object by its top-left corner.

- Normalize each candidate object the same way.

- Pick the candidate whose offset set matches the source, then crop it tightly.

**Train 1 input**

```text
0000000000000000
0200000033000000
0200000003300000
0220000000000000
0000000000000500
0000000400005550
0000000400000000
0000000440000000
0000000000000000
```
**Train 1 output**

```text
80
80
88
```
**Train 2 input**

```text
0000000000000000
0020000303000000
0222000333000000
0000000000000000
0000000000005500
0000000004005500
0000000044400500
0000000000000000
0000000000000000
```
**Train 2 output**

```text
080
888
```
**Test input**

```text
0000000000000000
0220000030000000
0220000030000000
0020000330005000
0000000000005000
0000000044005500
0000000044000000
0000000004000000
0000000000000000
```
**Test output**

```text
88
88
08
```
**Written solution:** The source object's absolute position does not matter; only its normalized occupied offsets matter. Compare each candidate after top-left normalization, find the one with the same offset pattern, and output that matching shape as a tight crop recolored to 8.

**Reference program**

```python
def solve_S15_E4(grid):
    return crop_matching_candidate(grid)
```
## S15_E5 — Use the Source as a Mask on the Target Rectangle
**Skills:** mask transfer, local coordinates, template/target separation

**Primitive note:** relative_offsets turns the source into a reusable local mask that can be replayed inside the target rectangle.

**Scaffold:**

- Treat the source object as a local mask inside its own bounding box.

- Find the top-left corner of the target rectangle.

- Replay the source mask at that target corner.

**Train 1 input**

```text
0000000000000
0200000033000
0200000033000
0220000033000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 1 output**

```text
0000000000000
0000000080000
0000000080000
0000000088000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 2 input**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000033300
0020000033300
0222000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000008000
0000000088800
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
00000000000000
00000000000000
02200000033000
02000000033000
02200000033000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test output**

```text
00000000000000
00000000000000
00000000088000
00000000080000
00000000088000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Written solution:** Read the source shape as a set of offsets from its own top-left corner. Then find the target rectangle's top-left corner and mark only those target positions whose local coordinates belong to the source mask. The result is the source pattern transferred into the target's frame, recolored to 8.

**Reference program**

```python
def solve_S15_E5(grid):
    return mask_transfer_to_target(grid)
```
## S15_E6 — Copy by Preserving Offsets from the Source Anchor
**Skills:** explicit anchor frames, vector preservation, non-corner anchors

**Primitive note:** Here the anchor is not the bounding-box corner. The important offsets are measured from the special source anchor cell.

**Scaffold:**

- Find the source anchor and the source shape.

- Measure every source cell relative to that anchor, not relative to the bounding box.

- Apply the same anchor-relative offsets at the target anchor.

**Train 1 input**

```text
00000000000000
00010000000000
00002000000000
00002000000000
00002200000000
00000000000000
00000000030000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000008000
00000000008000
00000000008800
```
**Train 2 input**

```text
00000000000000
00000000000000
00000000000000
00300000000000
00000002000000
00000022200000
00000100000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**

```text
00000000000000
00008000000000
00088800000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test input**

```text
000000000000000
000000000000000
000010000000000
002200000000000
002000000000000
002200000000000
000000000030000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000008800000
000000008000000
000000008800000
```
**Written solution:** The source anchor defines the local coordinate frame. Record where each source cell sits relative to that anchor, then recreate those same relative positions around the target anchor. This preserves the source-anchor geometry even when the anchor is outside the shape's top-left corner.

**Reference program**

```python
def solve_S15_E6(grid):
    return anchor_vector_copy(grid)
```
## S15_E7 — Indicator Row of Congruent Candidates
**Skills:** symbolic output, congruence testing, ordering candidates

**Primitive note:** Each candidate is reduced to a normalized offset signature; the final row reports which signatures match the source.

**Scaffold:**

- Normalize the source shape.

- Normalize each candidate and sort the candidates from top-left to bottom-right.

- Write 8 where the candidate matches the source and 0 otherwise.

**Train 1 input**

```text
000000000000000
020000003300000
020000000330000
022000000000000
000000000000000
040000050006000
040000555006000
044000000006600
000000000000000
```
**Train 1 output**

```text
0808
```
**Train 2 input**

```text
000000000000000
002000000300000
022200003330000
000000000000000
000000000000000
040400050006600
044400555006600
000000000000600
000000000000000
```
**Train 2 output**

```text
8080
```
**Test input**

```text
000000000000000
022000003000000
022000003000000
002000003300000
000000000000000
044000550006600
044000500006600
004000550000600
000000000000000
000000000000000
```
**Test output**

```text
0808
```
**Written solution:** Convert the source into a translation-invariant offset signature. Do the same for every candidate, ordered by their top-left positions. The output is a single indicator row: put 8 for each matching candidate and 0 for each non-matching one.

**Reference program**

```python
def solve_S15_E7(grid):
    return indicator_congruent(grid)
```


# Medium

## S15_M1 — Transfer the Whole Multicolor Pattern to the Marker
**Skills:** multicolor stencil transfer, local coordinates, pattern extraction

**Primitive note:** The primitive now carries color labels as well as offsets: a colored local stencil is copied intact to the marker.

**Scaffold:**

- Treat the whole colored motif as one local template inside its bounding box.

- Record each occupied local coordinate together with its color.

- Replay that colored stencil at the marker.

**Train 1 input**

```text
00000000000000
02300000000000
04200000000000
00300000000000
00000000000000
00000000100000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000230000
00000000420000
00000000030000
00000000000000
00000000000000
```
**Train 2 input**

```text
0000000000000
0100000000000
0000000000000
0000000000000
0000000020000
0000000342000
0000000030000
0000000000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0020000000000
0342000000000
0030000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
000000000000000
000000000000000
002030000000000
000400000000000
003020000000000
000000000100000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000203000
000000000040000
000000000302000
000000000000000
000000000000000
```
**Written solution:** Ignore the template's original position and instead read it as a colored map of local offsets. Then place every colored offset at the marker's location. The output is blank except for the copied multicolor motif.

**Reference program**

```python
def solve_S15_M1(grid):
    return multicolor_transfer(grid)
```
## S15_M2 — Stamp the Template in Each Marker's Color
**Skills:** parameterized stamping, color binding, template reuse

**Primitive note:** relative_offsets gives the shape; the marker color supplies the fill color for each copy.

**Scaffold:**

- Extract one normalized monochrome template.

- Find all marker cells and read their colors.

- Stamp the template at each marker using that marker's own color.

**Train 1 input**

```text
0000000000000000
0202000003000000
0222000000000000
0000000000000000
0000000000000000
0000000040000000
0000000000005000
0000000000000000
0000000000000000
0000000000000000
```
**Train 1 output**

```text
0000000000000000
0000000003030000
0000000003330000
0000000000000000
0000000000000000
0000000040400000
0000000044405050
0000000000005550
0000000000000000
0000000000000000
```
**Train 2 input**

```text
0000000000000000
0000000050000000
0000000000000000
0000000000000000
0220000000000000
0200000003000000
0220000000004000
0000000000000000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0000000055000000
0000000050000000
0000000055000000
0000000000000000
0000000003300000
0000000003004400
0000000003304000
0000000000004400
0000000000000000
```
**Test input**

```text
0000000000000000
0000000004000000
0220000000000000
0220000000000000
0020000000000000
0000000050000000
0000000000003000
0000000000000000
0000000000000000
0000000000000000
```
**Test output**

```text
0000000000000000
0000000004400000
0000000004400000
0000000000400000
0000000000000000
0000000055000000
0000000055003300
0000000005003300
0000000000000300
0000000000000000
```
**Written solution:** The shape comes from the source template, but the color comes from each destination marker. Normalize the source once, then stamp it at every marker, filling each copy with the marker's color instead of a fixed output color.

**Reference program**

```python
def solve_S15_M2(grid):
    return marker_colored_stamps(grid)
```
## S15_M3 — Rotate the Template 90 Degrees at the Marker
**Skills:** rotation, bounding-box geometry, anchor-relative replay

**Primitive note:** This is the rotation sibling of E3: rotate the normalized offset set before stamping.

**Scaffold:**

- Normalize the source shape in its tight bounding box.

- Rotate the occupied offsets by 90 degrees.

- Stamp the rotated version at the marker.

**Train 1 input**

```text
0000000000000
0200000000000
0200000000000
0220000000000
0000000010000
0000000000000
0000000000000
0000000000000
```
**Train 1 output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000088800
0000000080000
0000000000000
0000000000000
```
**Train 2 input**

```text
00000000000000
00000000100000
00000000000000
00000000000000
02200000000000
02000000000000
02200000000000
00000000000000
00000000000000
```
**Train 2 output**

```text
00000000000000
00000000888000
00000000808000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test input**

```text
000000000000000
020000000000000
022000000000000
002200000000000
000000000100000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000088000
000000000880000
000000000800000
000000000000000
000000000000000
```
**Written solution:** Treat the source shape as a local bitmap in its bounding box. Rotate that bitmap 90 degrees, convert the rotated occupied cells back into offsets, and place the result at the marker. The copied shape is recolored to 8.

**Reference program**

```python
def solve_S15_M3(grid):
    return rot90_to_marker(grid)
```
## S15_M4 — Transform-Coded Stamps
**Skills:** coded transforms, multiple branches, local-frame replay

**Primitive note:** A single normalized template is reused, but each marker color selects a different transform before stamping.

**Scaffold:**

- Normalize the template once.

- Map each marker color to a transform: identity, horizontal mirror, vertical mirror, or 90-degree rotation.

- Apply the appropriate transform before stamping at that marker.

**Train 1 input**

```text
000000000000000000
022000000300040000
020000000000000000
022000000000000000
000000000000000000
000000000000000000
000000000500060000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000880088000
000000000800008000
000000000880088000
000000000000000000
000000000000000000
000000000880088800
000000000800080800
000000000880000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 input**

```text
000000000000000000
000000000003000400
002000000000000000
002200000000000000
000220000000000000
000000000000000000
000000000050000000
000000000000006000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000008000008
000000000008800088
000000000000880880
000000000000000000
000000000000000000
000000000008800000
000000000088000880
000000000080008800
000000000000008000
000000000000000000
000000000000000000
```
**Test input**

```text
000000000000000000
000000000060000000
000000000000000000
022000000000000000
022000000000000000
002000000400000000
000000000000000000
000000000000030000
005000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
000000000000000000
000000000008800000
000000000088800000
000000000000000000
000000000000000000
000000000880000000
000000000880000000
000000000800088000
000800000000088000
008800000000008000
008800000000000000
000000000000000000
000000000000000000
```
**Written solution:** The template is always the same, but the marker color tells you which version to stamp. Use the learned marker-color map to choose between identity, horizontal mirror, vertical mirror, and 90-degree rotation. Then stamp the chosen variant at the marker, recolored to 8.

**Reference program**

```python
def solve_S15_M4(grid):
    return transform_coded_stamps(grid)
```
## S15_M5 — Stamp the XOR of Two Templates
**Skills:** set operations on shapes, local coordinates, symbolic composition

**Primitive note:** relative_offsets makes it easy to perform a set-theoretic XOR between two normalized templates.

**Scaffold:**

- Normalize both source templates.

- Turn each one into a set of local offsets.

- Keep the offsets that belong to exactly one of the two sets, then stamp that XOR shape at the marker.

**Train 1 input**

```text
000000000000000
020000003000000
020000033300000
022000000000000
000000000000000
000000000010000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000088000
000000000008800
000000000088000
000000000000000
000000000000000
```
**Train 2 input**

```text
000000000000000
000000033000000
000000003300000
000000000000000
022000000000000
020000000000000
022000000010000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000088800
000000000088000
000000000000000
```
**Test input**

```text
000000000000000
000000003030000
022000003330000
022000000000000
002000000000000
000000000000000
000000000010000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000008800
000000000000800
000000000008000
000000000000000
```
**Written solution:** Normalize both source shapes into local offset sets. Compute their symmetric difference: cells present in one template but not both. Then place that resulting offset set at the marker and recolor it to 8.

**Reference program**

```python
def solve_S15_M5(grid):
    return xor_two_templates(grid)
```
## S15_M6 — Crop the Majority Shape
**Skills:** majority reasoning, translation-invariant comparison, cropping

**Primitive note:** All candidates are compared in a common local frame so that translation disappears and only shape remains.

**Scaffold:**

- Normalize every candidate.

- Count which normalized shape appears most often.

- Crop that majority shape tightly and recolor it to 8.

**Train 1 input**

```text
0000000000000000
0200000003000000
0200000033300000
0220000000000000
0000000000000000
0000000000400000
0000000000400000
0000000000440000
0000000000000000
```
**Train 1 output**

```text
80
80
88
```
**Train 2 input**

```text
0000000000000000
0220000000000000
0220000000004400
0020000000004000
0000000000004400
0000000330000000
0000000330000000
0000000030000000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
88
88
08
```
**Test input**

```text
0000000000000000
0200000003030000
0220000003330000
0022000000000000
0000000000000000
0000000000000000
0000000000400000
0000000000440000
0000000000044000
0000000000000000
```
**Test output**

```text
800
880
088
```
**Written solution:** Each candidate may sit in a different place, so first normalize them all by their top-left corners. The normalized pattern that occurs most often is the majority shape. Output a tight crop of that shape, recolored to 8.

**Reference program**

```python
def solve_S15_M6(grid):
    return majority_congruence_crop(grid)
```
## S15_M7 — Indicator Row of Source-or-Mirror Matches
**Skills:** reflection-invariant matching, symbolic reporting, candidate ordering

**Primitive note:** The accepted signature family includes both the source and its horizontal mirror.

**Scaffold:**

- Build two acceptable signatures: the source itself and its horizontal mirror.

- Normalize and sort all candidates.

- Output 8 for candidates matching either acceptable signature and 0 for the rest.

**Train 1 input**

```text
0000000000000000
0220000003300000
0200000003000000
0220000003300000
0000000000000000
0440000050006600
0040000050006600
0440000055000600
0000000000000000
```
**Train 1 output**

```text
8800
```
**Train 2 input**

```text
0000000000000000
0020000030000000
0020000030000000
0220000033000000
0000000000000000
0040000500000600
0040000550006660
0440000050000000
0000000000000000
```
**Train 2 output**

```text
8800
```
**Test input**

```text
0000000000000000
0020000030000000
0020000030000000
0220000033000000
0000000000000000
0040000550006600
0040000055006600
0440000000000600
0000000000000000
```
**Test output**

```text
8800
```
**Written solution:** Normalize the source shape, then also normalize its horizontal mirror. Each candidate is a match if it equals either one of those two signatures. Report the results in a one-row indicator grid ordered by candidate position.

**Reference program**

```python
def solve_S15_M7(grid):
    return reflection_match_indicator(grid)
```


# Hard

## S15_H1 — Learn that the Marker Means the Bottom-Right Corner
**Skills:** latent anchor inference, corner semantics, transfer by corner mode

**Primitive note:** The hard part is realizing that the marker refers to the source shape's bottom-right corner rather than its top-left corner.

**Scaffold:**

- Compare the training outputs to the source shapes and infer which corner of the source is being aligned to the marker.

- Express the source cells as offsets from that corner.

- Replay those corner-relative offsets at the test marker.

**Train 1 input**

```text
000000000000000
020000000000000
020000000000000
022000000000000
000000000000000
000000000000000
000000000010000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000800000
000000000800000
000000000880000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**

```text
000000000000000
000000000000000
000000000010000
000000000000000
002200000000000
002000000000000
002200000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000880000
000000000800000
000000000880000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test input**

```text
00000000000000000
02000000000000000
02200000000000000
00220000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000001000
00000000000000000
00000000000000000
00000000000000000
```
**Test output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000800000
00000000000880000
00000000000088000
00000000000000000
00000000000000000
00000000000000000
```
**Written solution:** The marker does not indicate where the source shape's top-left corner should go. Instead, it indicates where the source shape's bottom-right corner should land. So compute offsets from the source bounding box's bottom-right corner, then stamp those offsets at the marker and recolor them to 8.

**Reference program**

```python
def solve_S15_H1(grid):
    return bottom_right_anchor_copy(grid)
```
## S15_H2 — Anchor-Frame Transform Copy
**Skills:** anchor-frame geometry, signed offsets, transforms about an origin

**Primitive note:** Unlike earlier puzzles, the transforms act on signed offsets about the anchor itself, not merely inside a bounding box.

**Scaffold:**

- Use the special source anchor as the origin of a signed coordinate system.

- Write every source cell as a signed offset from that anchor.

- For each target marker, transform those signed offsets according to the marker color, then replay them around the target.

**Train 1 input**

```text
000000000000000000
000000000000000000
000000000030000000
000000000000000000
000010200000000000
000002220000000000
000000000040005000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
000000000000000000
000000000000000000
000000000000800000
000000000008880000
000000000000000000
000000000000000000
000000000000800000
000000000808880000
000000000880000000
000000000800000000
```
**Train 2 input**

```text
000000000000000000
000000010000000000
000000200000000000
000000200000000000
000000220000000000
000000000000005000
000030000000000000
000000000000040000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000088800800
000800000080000800
000800000000008800
000880000000000000
000000000000000000
000000000000000000
```
**Test input**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000100000000000
0000002000000000000
0000002200000000000
0000300220000005000
0000000000000000000
0000000000000400000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Test output**

```text
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0008000000088000800
0008800000880008800
0000880000800088000
0000000000000000000
0000000000000000000
```
**Written solution:** The source anchor defines an origin. Record the source cells as signed coordinates relative to that origin, including negative directions when needed. Then, depending on the target marker color, either keep those signed offsets, rotate them around the origin, or mirror them across the anchor's vertical axis before stamping them at the target.

**Reference program**

```python
def solve_S15_H2(grid):
    return anchor_frame_transform_copy(grid)
```
## S15_H3 — Pairwise Congruence Matrix
**Skills:** pairwise comparison, symbolic matrices, shape congruence

**Primitive note:** Each component is reduced to a normalized offset signature, and the output matrix reports equality of those signatures pairwise.

**Scaffold:**

- Sort the candidate objects by position.

- Normalize each candidate to a translation-invariant signature.

- Build an N×N matrix with 8 exactly where two candidates share the same signature.

**Train 1 input**

```text
00000000000000
02000000030000
02000000333000
02200000000000
00000000000000
00000000400000
00000000400000
00000000440000
00000000000000
```
**Train 1 output**

```text
808
080
808
```
**Train 2 input**

```text
0000000000000000
0220000000000000
0220000000004400
0020000000004000
0000000000004400
0000000033000000
0000000033000000
0000000003000000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
808
080
808
```
**Test input**

```text
0000000000000000
0200000003030000
0220000003330000
0022000000000000
0000000000000000
0000000000000000
0000000000400000
0000000000440000
0000000000044000
0000000000000000
```
**Test output**

```text
808
080
808
```
**Written solution:** List the candidate objects in reading order and normalize each one so translation disappears. Then compare every pair. Put 8 in the matrix when two candidates are congruent and 0 otherwise, including the diagonal where a shape always matches itself.

**Reference program**

```python
def solve_S15_H3(grid):
    return pairwise_congruence_matrix(grid)
```
## S15_H4 — Multicolor Transform-Coded Stamps
**Skills:** multicolor transforms, coded control flow, template replay

**Primitive note:** This is the multicolor extension of transform-coded stamping: the local stencil carries color labels through the chosen transform.

**Scaffold:**

- Extract the multicolor template as colored local offsets.

- Read the transform code from each marker color.

- Apply the chosen transform to the whole colored stencil and stamp it at the marker.

**Train 1 input**

```text
0000000000000000000
0270000000300040000
0820000000000000000
0090000000000000000
0000000000000000000
0000000000000000000
0000000000500060000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 1 output**

```text
0000000000000000000
0000000000270072000
0000000000820028000
0000000000090090000
0000000000000000000
0000000000000000000
0000000000090008200
0000000000820092700
0000000000270000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 2 input**

```text
0000000000000000000
0000000000060000000
0002000000000000000
0078900000000000000
0002000000000000000
0000000000000000000
0000000000400000000
0000000000000030000
0050000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```
**Train 2 output**

```text
0000000000000000000
0000000000007000000
0000000000028200000
0000000000009000000
0000000000000000000
0000000000000000000
0000000000020000000
0000000000987002000
0002000000020078900
0078900000000002000
0002000000000000000
0000000000000000000
0000000000000000000
```
**Test input**

```text
00000000000000000000
00000000000300040000
00207000000000000000
00080000000000000000
00902000000000000000
00000000000000000000
00000000000000000000
00000000000500060000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```
**Test output**

```text
00000000000000000000
00000000000207070200
00000000000080008000
00000000000902020900
00000000000000000000
00000000000000000000
00000000000000000000
00000000000902090200
00000000000080008000
00000000000207020700
00000000000000000000
00000000000000000000
00000000000000000000
```
**Written solution:** The source motif is not just a shape; it is a colored stencil. Normalize it into local colored offsets, then use the marker-color code to choose the appropriate transform. After transforming the whole stencil, stamp it at the marker while preserving the internal colors.

**Reference program**

```python
def solve_S15_H4(grid):
    return multicolor_transform_coded(grid)
```
## S15_H5 — Header Chooses the Set Operation
**Skills:** header-controlled operations, set logic, normalized crops

**Primitive note:** relative_offsets lets the two templates become pure sets, and the header selects which set operation to apply.

**Scaffold:**

- Normalize both source shapes into local offset sets.

- Read the header color to choose the operation.

- Apply either intersection or symmetric difference, then crop the result tightly.

**Train 1 input**

```text
70000000000000
00000000000000
02000000330000
02000000330000
02200000030000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**

```text
80
80
08
```
**Train 2 input**

```text
90000000000000
00000000000000
02200000030000
02000000333000
02200000000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**

```text
800
088
880
```
**Test input**

```text
700000000000000
000000000000000
020000003030000
022000003330000
002200000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
80
88
```
**Written solution:** First turn both source templates into normalized offset sets. The header color tells you whether to keep only the shared cells or to keep the cells that belong to exactly one template. After computing that set operation, output the resulting shape as a tight crop recolored to 8.

**Reference program**

```python
def solve_S15_H5(grid):
    return header_setop_crop(grid)
```
## S15_H6 — Priority Stamps with Walls
**Skills:** clipping, overlap priority, constraint-aware stamping

**Primitive note:** The same local template is stamped multiple times, but wall cells block placement and higher-priority markers win overlaps.

**Scaffold:**

- Normalize the source template.

- Stamp it at every marker, but skip any destination cell that lands on a wall or out of bounds.

- When two stamps compete for the same cell, keep the one from the higher-priority marker color.

**Train 1 input**

```text
000000000000000
002000000000000
022200000000000
000000000000000
000000000000000
000000034090000
000000000990000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000008800000
000000088000000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**

```text
000000000000000
020000000000000
020000000000000
022000000000000
000000040000000
000000300000000
000000009000000
000000009900000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000080000000
000000880000000
000000880000000
000000880000000
000000000000000
000000000000000
```
**Test input**

```text
0000000000000000
0220000000000000
0220000000000000
0020000000000000
0000000000000000
0000000040000000
0000000300900000
0000000009900000
0000000000900000
0000000000000000
0000000000000000
```
**Test output**

```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000088000000
0000000888000000
0000000880000000
0000000080000000
0000000000000000
0000000000000000
```
**Written solution:** Take the source template and try to stamp it at each marker. Any cell that would fall on a wall or outside the grid is discarded. If two surviving stamps overlap, the copy associated with the higher-priority marker color wins that cell. The surviving painted cells are recolored to 8.

**Reference program**

```python
def solve_S15_H6(grid):
    return priority_walls_stamps(grid)
```
## S15_H7 — Crop the Odd Shape under Rotation or Reflection
**Skills:** dihedral invariance, odd-one-out reasoning, cropping

**Primitive note:** The comparison is no longer translation-invariant only; you must canonicalize under rotations and reflections.

**Scaffold:**

- For each candidate, generate a canonical signature that treats rotations and reflections as equivalent.

- Find the one candidate whose canonical signature occurs only once.

- Crop that odd shape in its observed orientation and recolor it to 8.

**Train 1 input**

```text
00000000000000
02000000030000
02000000030000
02200000330000
00000000000000
04400000050000
00400000555000
00400000000000
00000000000000
```
**Train 1 output**

```text
080
888
```
**Train 2 input**

```text
00000000000000
02200000300000
00200000300000
00200000330000
00000000000000
00400000505000
00400000555000
04400000000000
00000000000000
```
**Train 2 output**

```text
808
888
```
**Test input**

```text
00000000000000
00200000330000
00200000030000
02200000030000
00000000000000
04000000500000
04000000550000
04400000050000
00000000000000
```
**Test output**

```text
80
88
08
```
**Written solution:** Normalize every candidate, but do not stop at translation. Also consider all rotated and reflected versions and choose one canonical dihedral signature for each candidate. Three candidates share a family, while one does not. Output that odd candidate as a tight crop, recolored to 8.

**Reference program**

```python
def solve_S15_H7(grid):
    return odd_dihedral_crop(grid)
```