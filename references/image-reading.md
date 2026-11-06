# Image reading: the scene inventory

Read the input before writing any prompt. The user names things loosely ("coconut trees" for
royal palms, "the bonsai" when there are two); the model needs exact names, and the check needs a
list to compare against. Look at the image at full size around the edit area: a reduced view
misled twice in testing (a second bonsai hidden behind a hedge, cropped palms at the edges).

## What to note
Write the inventory into the edit's `log.md`. Short lines, no prose.

| Field | Note |
|---|---|
| Image type | render, viewport capture, photo, illustration, diagram |
| Camera | eye level or high, wide or tight, horizon position |
| Light | sun direction, time of day, hard or soft shadows, artificial light |
| Style | photoreal, stylised, colour grading |
| Edit targets | each one by precise name (see [edit-types.md](edit-types.md) for vocabulary), how many, where (left of the stairs, in the grey stone pot), how big against a visible anchor |
| Look-alikes | anything the edit could hit by mistake: the same kind of object elsewhere, half-hidden copies, objects cut by the image edge |
| At risk | small text and signs, faces, reflections, objects touching the target, thin lines (railings, cables) |
| Empty space | what lies behind a target that will be removed |

Anchors are visible things of known size or position the prompt can point at: a door, a floor
joint, a roof edge, a lounger, the gap of sky above a crown.

## Example (an interior entrance)
- Image type: photoreal render; camera eye level, wide; light: low sun from the right, hard
  shadows on the floor, warm backlit screens.
- Edit targets: one dark carved stone reception desk (wooden top, brass table lamp on it) in front
  of the backlit wooden lattice screen, centre right; two bonsai pines in grey stone pots on the
  left — a large one in front, a smaller one behind it, its pot half hidden by a hedge.
- Look-alikes: potted plants in wooden pots on the right (not stone, not bonsai); a tree top right.
- At risk: a carved name sign on the left wall (Latin and Chinese characters) and a small wall
  sign beside the bonsai (small text).
- Empty space: lattice screen down to the floor and cream floor tiles behind the desk.

The same inventory is the checklist in [check.md](check.md): every target changed, every
look-alike and at-risk item still there.
