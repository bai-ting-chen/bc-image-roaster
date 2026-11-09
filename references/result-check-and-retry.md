# Result check and retry: did the change happen, did anything else change

Two separate questions, judged separately (as in VIEScore and GEditBench): an image that barely
changed is not a pass just because it drifted little.

## Steps per try
1. **Compare sheet** of the input and this try (`scripts/sheet.py`), whole image. Look for the
   change, for objects added or gone, and for a moved camera or crop.
2. **Full-size crops** with `sheet.py --box` around each edit target, each look-alike and each
   at-risk item (text, faces). Judging from a reduced view misled twice; crops decide.
3. **Drift flags:** `scripts/compare.py <original> <try> <dir> --no-crops`. Any region over 3 %
   that the edit spec does not touch → inspect that region in a crop. The number only says where
   to look; it cannot judge success, and a light or sky edit flags every region on purpose.
4. **Verdict** against the inventory, one line each:
   - every Change done, with the right count, kind, place and size, on every part named;
   - a material change kept the shape and profile of what it changed, and on a patterned surface
     the pattern (positions, widths, which parts are light or dark per the material map); the new
     material reads as itself at full size (terrazzo shows its chips) and has its real format
     (no tile joints on poured terrazzo). Judge this only from a full-size crop of the surface;
     a reduced view passed a floor that had lost its pattern;
   - every Keep item and look-alike still there and unchanged;
   - nothing added, nothing moved, framing the same;
   - every Geometry line of the inventory still true
     ([scene-inventory.md](scene-inventory.md)), checked in crops of the whole image, not only
     around the changed parts;
   - every part on the passed list (below) still as good as in the best try;
   - text: readable and spelled as before, or flagged to the user.
5. Write the verdict and the failure name (from the table in [prompt-writing.md](prompt-writing.md)) to
   `log.md`.

## Protect what passed
Why: every retry from the original redraws the whole image, so parts that were right in one try
come out wrong in the next; in testing, three of five retries broke parts an earlier try had right.
- **Passed list:** after each check, list in `log.md` the parts that are right in the best try so
  far (framing, roof, each material, planting, people, shadows). The best try is the one with the
  fewest failures, by the user's review when there is one.
- **Regression fails a try:** a retry that fixes its target but makes a passed part worse fails.
  Compare those parts in crops against the best try, not only against the original.
- **Stop on regression:** after two retries in a row that are worse than the best try, stop and
  offer the best try with a fix on it (below), even under the retry cap. At the retry cap, ask
  the user.

## Recommend one from the ladder
After the three ladder tries are checked:
1. **One sheet** of the input and the three tries, labelled with rung, model and verdict:
   `try-01 simple nb2 pass`, `try-02 structured nb2 fail: look-alike changed`.
2. **Recommend one** to the user, by this order: the most Change lines done, then the fewest Keep
   failures, then the best look as a whole (light, material realism, no AI artefacts). Give the
   reasons in two or three plain lines and say what the recommended try still gets wrong.
3. **One line per other try:** what it did better or worse than the recommended one. When a
   simpler rung did as well as a longer one, say so: it shows this kind of edit needs less wording.
4. **Stop for the user's pick.** The user may pick another try, ask for a retry from one of them, or
   take one as it is. Write the recommendation and the pick to `log.md`.

## Pass, retry, escalate
- **Pass:** the picked try holds all lines, or the user takes it as it is → deliver.
- **Fail on one or two local parts** (a figure, an object, one material): fix on the best try (below).
- **Fail on the whole image** (wrong light, wrong style, many parts): retry from the picked try's
  prompt on the original; look up the failure in [prompt-writing.md](prompt-writing.md) ›
  Failure → prompt fix. Retries run one prompt at a time.
- **Switching to Pro:** any retry may run on Pro, without asking, when the same part failed twice
  on NB2 after prompt fixes, or the failure is detail or realism the wording already asks for
  (sparse foliage, flat materials). Name the model in the sheet label and the log, and tell the
  user which part kept failing.
- **Exact tones:** a number like "15 % lighter" is not reached; the model lands near "lighter"
  (asked 1.15, measured 1.7–2.0 on four tries). Say this before running, describe the tone in words
  ("one shade lighter, almost the same colour"), and when the user needs the exact value, offer the
  a fix on the accepted image or a tone fix in an image editor.
- **Small text:** it garbles in nearly every run (16 of 16 in testing). Do not retry for it; tell
  the user which text broke, they fix it outside this skill.

## Fix on the best try
When the best try is right except for one or two local parts, edit that try instead of redrawing
from the original. A local edit on a good result keeps what passed; a full retry rolls everything
again.
- Input: the best try as `input_image_path`, no reference images unless the fix needs one.
- Prompt: the light-edit form, one Change line per part, then "Keep everything else in the image
  exactly as it is: the camera, the light and shadows, every material and object." No scene
  description: the long prompt is what invites the redraw.
- Check against the best try first: `compare.py <best try> <fix>` should flag only the regions
  of the fixed parts; then the geometry and passed list against the original.
- One fix step per round. A fix on a fix drifts like any chain; a second round starts from the
  best try again with all the fixes in one prompt.

## Follow-up edits
A local follow-up (one object, one person, one material) runs on the accepted image, the same way
as a fix on the best try. A follow-up that changes the whole image (light, season, style) starts
again from the original with the new change added to the edit spec as one more Change line: a
whole-image redraw chained on an earlier result drifts further from the original with every step.

## Deliver
Rebuild the sheet with `sheet.py` when retries were added (input, the ladder, every retry), labels
like `try-04 nb2 pass (from structured)`. Delete `input.jpg`, the
prepared references and any crop sheets; keep the tries, `sheet.jpg` and `log.md`.
