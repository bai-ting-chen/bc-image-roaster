# Prompt writing: from request to prompt

The prompt is the whole control we have: the model redraws the entire image every time, guided by
the picture and the words. These rules are a generic base for image-edit models, ranked by how
many independent official guides agree (research 2026-11-06), then tested on Nano Banana 2 and Pro
on three images × four prompt forms.

## The template

```text
Edit the supplied [render / photo / illustration]. [The second image is a reference of <what>.]
Change: <operation> <exact target, with where it is> <into what, with 2–3 visual traits>.
Change: <second change, its own line, its own location>
Placement and size: <only if size or position matters: contact point + a limit to stay under>
Keep: <look-alikes and at-risk items, by name and position>. Keep the rest unchanged.
```

Leave out lines that have nothing to say. One simple change may fit in one Change line and Keep.

## Rules
1. **Separate what changes from what stays.** Change lines, then a Keep line. In testing a plain
   sentence never passed cleanly; change/keep won every test.
2. **Name the operation and the exact target:** replace, remove, add, recolour, resize — "the two
   tall palm trees, one left and one right of the central stairs", not "the trees".
3. **Describe the new thing with two or three visual traits.** "Pine" alone gave a fir; "straight
   reddish-brown trunk, dark-green needle crown" gave a pine every time.
4. **Several changes: one short line each, each with its own location.** Keep them apart in the
   words. In testing the model merged "remove the desk" and "add a sculpture" into a sculpture where the
   desk stood in 5 of 8 runs.
5. **A removal says the space stays empty** ("the space stays empty"). Do not describe what to show
   there in detail: that sentence invited the model to fill the gap with the other change.
6. **Anchors: a limit to stay under, never an edge to reach.** "Its top reaches the same point near
   the top edge" pushed crowns past the edge in 2 of 4 runs. Say "leave the same strip of sky above
   the crown as above the palm", "no wider than the palm's crown", "well below the ceiling".
   Separate height, width and uniform scale; give a contact point (trunk base, pot centre).
7. **Keep list: short to medium.** Name look-alikes and items at risk, with position. No full scene
   description: in testing the long list won one test and lost another on both models.
8. **Stay with the request.** Add no lighting, mood, lens or style the user did not ask for, and no
   detail the image does not show.
9. **Positive wording first,** but keep a concrete "no" when it settles a real doubt ("one sculpture
   in each pot, nothing where the desk was").
10. **Reference images get a role in words:** "The second image is a reference photo of the
    sculpture." Do not rely on "image 2" numbering alone.
11. **Quote text to render, spelled exactly.** Small existing text will still break (see
    [result-check-and-retry.md](result-check-and-retry.md)); warn the user before running.
12. **Plain sentences in short blocks.** No keyword lists, no weight syntax like `(tree:1.5)`, no
    JSON.
13. **On a retry, restate the important keeps.** Each call is fresh; it does not remember the
    last prompt. A fix for one failure can cause another (a retry that saved the planters changed
    the rail profile), so the check of every retry covers all Change and Keep lines again.
14. **Take the user's words at their full scope.** "The floor" is every floor surface in view:
    field tiles, stone bands, inlays, borders. List each part in the Change line. Do not leave a
    part out because it looks like a design feature; if a part may be meant to stay, ask.
15. **A material change keeps the shape.** Describe the object's parts from the inventory and say
    which part changes: "only the timber top cap of each handrail becomes brushed champagne metal;
    the cap keeps its rounded profile and size; the slim metal support below stays as it is". A
    patterned surface gets a material map in the new material's real format
    ([prompt-templates-per-edit.md](prompt-templates-per-edit.md) › Change a material).
16. **Remove whole groups, not part of a group of look-alikes.** Removing two pots out of six
    standing together failed three times (left, swapped or turned into trees); removing both whole
    groups worked at once. If the user's count and the image disagree, ask which they mean.
17. **Light and time of day: describe the sky and the lights you can see,** not just a word.
    "Evening" was read as dusk every time while the user meant night. Use the table in
    [prompt-templates-per-edit.md](prompt-templates-per-edit.md) › Sky, time of day.

## Failure → prompt fix

| Seen in the check | Fix in the next prompt |
|---|---|
| Wrong kind of object (fir for pine) | add 2–3 visual traits of the wanted object |
| Too tall, cut by the image edge | replace the edge anchor with a gap to keep ("same strip of sky above") |
| Too wide, hides things behind | add a width limit against the old object or a neighbour |
| Two changes merged (new object where the removed one was) | one line per change with its own location; removal line says "the space stays empty"; add "nothing stands where the desk was" |
| Target only half changed (one of two replaced) | give the count and each location ("the large one in front and the smaller one behind it") |
| Look-alike changed too | name it in Keep with its position |
| Unrequested object added (waterfall, extra lounger, extra palm) | name the area in Keep ("the pool edge and the deck stay as they are"); try "Add nothing else." |
| Framing or camera moved | add "Keep the camera, framing and crop exactly as they are." to Keep |
| People clustered in one posed group | give each person a location ("one near the left steps, one in the middle …") |
| Door opened, or a closed object changed state | name it in Keep with its state ("both bronze doors stay closed") |
| Light fixtures changed form or new lamps added | describe the existing fixtures exactly; add "Add no other lights." |
| Material spread to look-alikes (stone planters turned timber) | name them in Keep with their current material ("stay pale cream stone, not wood") |
| Object's profile or shape changed in a material swap | name the parts and say the shape and size stay (rule 15) |
| Part of a look-alike group left, swapped or transformed instead of removed | remove the whole group, or ask the user (rule 16) |
| Part of a named surface left unchanged (stone bands, inlay) | list every part of the surface in the Change line (rule 14) |
| Pattern of a surface lost, inverted or kept in the old material | give each part its own new finish (material map, rule 15) |
| Larger sign text garbled | quote the sign text exactly in Keep; this saved a name sign once. Tiny text still breaks: tell the user (see result-check-and-retry.md) |

When a new failure and a fix that worked turn up, add a row here.

## Showing the prompt to the user
Show the prompt as it will be sent, then one line in plain English on why it is phrased that way
("I named both bonsai and their pots so the model does not leave one; the desk line says the space
stays empty so the sculpture does not move there."). Keep the explanation short and concrete; the
user reads English as a second language.
