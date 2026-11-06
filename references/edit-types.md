# Edit types: templates and vocabulary

One short template per common edit. Fill the brackets from the scene inventory; the general rules
are in [prompting.md](prompting.md). Examples are for illustration, not to copy.

## Replace an object
```text
Change: replace [the exact object, count, location] with [new object + 2–3 visual traits].
Placement and size: each [new object] stands on the same [contact point] as the [old one]; [a limit to stay under].
Keep: [look-alikes]. Keep the rest unchanged.
```
Vocabulary: name species, material and form, not a brand ("royal palm", "Scots pine with
reddish-brown bark", "white marble sculpture, a tall twisting ribbon").
Example: two palms → pines: contact point = trunk base on the pool deck; limits = same
strip of sky above the crown, crown no wider than the palm's.

## Remove an object
```text
Change: remove [the exact object and what sits on it, location]. The space stays empty.
Keep: [what stands behind and beside it]. Keep the rest unchanged.
```
Remove whole groups: when the target stands among look-alikes, remove the group or ask
([prompting.md](prompting.md) rule 16).
Example: "remove the dark carved stone reception desk in the centre, with its wooden top and the
brass table lamp on it. The space stays empty."

## Add people or objects
```text
Change: add [count] [who/what, clothing or type] [doing what].
Placement and size: [where each one goes, or the area they spread over]; scale each to [a nearby anchor]; none in [area to keep empty].
Keep: [furniture and objects they must not move]. Keep the rest unchanged.
```
Vocabulary: pose (swimming, standing in waist-deep water, lying asleep on their back), clothing
(swimwear, business casual), age range only if the user asks.
Anchor: a person lying down is as long as a lounger; a standing adult reaches a little below the
top of a door. Several people: give each a location, or they cluster.

## Change a material or colour
```text
Change: change [every part of the surface or object, location] from [current material] to [new material + finish + colour, in the new material's real format]. Only the material changes: [each part] keeps its shape, profile and size.
Keep: [the other parts of the same object]; [nearby things of the old or the new material, with their current material]. Keep the rest unchanged.
```
Read the object's parts first (a handrail = a metal support and a timber top cap; a floor = field
tiles, stone bands, inlay). Name every part that changes and every part that stays.

**A surface with a pattern of parts gets a material map,** one new finish per part, so the pattern
still has something to show. Never write "everything becomes X, keep the pattern": in testing that
contradiction made the model keep old bands or redraw the pattern. If the user names one material
for a patterned surface, ask whether the pattern parts take a lighter or darker tone (RULES EDT_02).

**Use the new material's real format,** not the old one's joints:

| Material | Format to write |
|---|---|
| terrazzo, poured resin, microcement | one seamless poured surface, no tile or panel joints; the pattern shows only where the colour changes |
| stone, porcelain tiles | slabs of [size], [laying pattern], fine joints |
| timber flooring, decking | boards of [width] running [direction] |
| timber veneer on a column or wall | vertical grain, no visible joints unless the user asks |

Example (a patterned floor to terrazzo): "change the whole floor in view to one seamless poured
terrazzo surface with no tile or panel joints: the field areas and the inlay squares in polished
dark charcoal terrazzo with small white and grey chips; the stone bands and the inlay outlines in a
light grey terrazzo with the same chips. The bands and the rounded-square inlay keep their shapes,
widths and positions."

## Planting
Use Replace or Add. Name the plant type, height against an anchor, crown shape and density
("low clipped box hedge, knee high", "multi-stem olive tree, crown below the first-floor window").

## Sky, time of day, light, season
```text
Change: make it [late afternoon / dusk / overcast / winter], with [sun direction or light quality, sky colour].
Keep: [all objects and materials], the camera and framing. Change only light, shadows, sky [and season cues].
```
Describe what the sky and the lights look like, not just the word:

| User's word | Write in the prompt |
|---|---|
| sunset, golden hour | low warm sun from [side], long shadows, sky warm near the horizon |
| dusk, blue hour | sun gone, sky deep blue with a faint warm band at the horizon, existing lights on |
| evening, night | dark navy night sky, no sunlight, no shadows from the sun, existing lights on |
| overcast | even grey sky, soft light, no hard shadows |

"Evening" has two readings, dusk or night (RULES EDT_02). Name the existing light
fixtures that should glow and add "Add no other lights." This edit changes every region on
purpose: the drift flag will light up everywhere, so check the objects, not the numbers. Season
cues to name: bare branches, snow on flat surfaces only, autumn leaf colour.
