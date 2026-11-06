# Check: did the change happen, did anything else change

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
   - text: readable and spelled as before, or flagged to the user.
5. Write the verdict and the failure name (from the table in [prompting.md](prompting.md)) to
   `log.md`.

## Pass, retry, escalate (RULES CHK_02, MOD_01)
- **Pass:** all lines hold → deliver.
- **Fail:** look up the failure in [prompting.md](prompting.md) › Failure → prompt fix.
- **Escalating:** run the best prompt so far on Pro; tell the user which part kept failing.
- **Small text:** it garbles in nearly every run (16 of 16 in testing). Do not retry for it; tell
  the user which text broke, they fix it outside this skill.

## Follow-up edits (RULES EDT_04)
Why: each pass redraws and shrinks the whole image, so an edit chained on an earlier result
drifts further from the original with every step. How: add the new change to the edit spec as one
more Change line. A chained step, when the rule allows one, uses the accepted try as
`input_image_path` while `compare.py` and the sheet still take the original as the input.

## Deliver (RULES CHK_03)
Build the sheet with `sheet.py`, labels like `try-01 nb2 fail: merged`. Delete `input.jpg`, the
prepared references and any crop sheets; keep the tries, `sheet.jpg` and `log.md`.
