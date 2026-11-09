---
name: bc-image-roaster
description: >-
  Quick AI edits of an existing image (render, viewport capture or photo) with Nano Banana 2 / Pro
  through Rook: turns the user's rough request into three edit prompts from simple to detailed,
  runs each on both models, checks the six results for the change and for drift, puts them on one
  compare sheet with a recommendation for the user to pick, and retries from the pick. Use
  whenever the user wants to change something in an image (swap or remove an object, change a material, planting, sky,
  light or season, add people), asks to "roast", touch up or AI-edit a picture, or hands over an
  image-edit prompt to tighten, even if they do not name the skill or the model.
---
<!-- bc-image-roaster-skill-loaded-marker -->

# bc-image-roaster

Light, fast edits on top of an existing image. The core is the prompt, because the user writes
rough English (not their first language). No compositing or masking: drift is fought with wording,
checking and retries. Read the reference named in the step you are in.

## Prerequisites
- Rook connected (`rhino_ping` returns pong); `rhino_render_view` reachable.
- Python 3.11 with Pillow (no numpy needed) for the scripts.
- The input image on disk; any reference image (an object to insert) on disk too.

## Workflow
1. **Read the image** at full size into a scene inventory: every target, look-alike and at-risk
   item, and the geometry a redraw could get wrong → [scene-inventory.md](references/scene-inventory.md).
2. **Edit spec:** what changes, what stays, anchors for size and position. Take the user's words at
   their full scope. Ask back only when the request and the image disagree (count, which object) or
   a word has two readings (evening: dusk or night); otherwise decide and say what was decided.
3. **Prompt ladder:** write the same spec as three prompts, from simple to detailed (simple,
   structured, detailed) → [prompt-writing.md](references/prompt-writing.md) › Prompt ladder,
   [prompt-templates-per-edit.md](references/prompt-templates-per-edit.md). One spec, three
   wordings: what differs is how much the words control, so the sheet shows which level this edit
   needs. Show the three prompts as they will be sent, with one plain-English line each on what it
   adds; warn when the image holds small text.
4. **Run** each of the three prompts on both `fal-ai/nano-banana-2` and `fal-ai/nano-banana-pro`:
   six calls through Rook on the prepared input, with the defaults under Parameters →
   [model-and-rook-call.md](references/model-and-rook-call.md).
5. **Check and recommend:** check each of the six tries, the change and the preservation
   separately, from full-size crops against the inventory; the drift number only says where to
   look. Put the input and the six tries on one compare sheet, then recommend one with its reasons
   and name what each got wrong → [result-check-and-retry.md](references/result-check-and-retry.md).
   Stop here: the user reviews the sheet and picks.
6. **Retry** only from the try the user picked, when it still needs fixing. Keep a list of the
   parts that already pass; a retry that makes one of them worse fails. One or two local parts
   wrong: fix them on the best try with a short local prompt. Whole image wrong: name the
   failure, change one thing in the prompt, retry from the original. Retries run on the picked
   try's model; switch to the other model when the failure looks like a model limit rather than
   wording, no need to ask. When to stop and ask the user →
   [result-check-and-retry.md](references/result-check-and-retry.md) › Protect what passed.
7. **Deliver** the chosen image, the compare sheet of the input and every try, and one line per
   try; then delete prepared copies and crops.

A prompt the user hands in: it takes the simple rung as given; write the structured and detailed
rungs from it in steps 1–3, show all three, then run them unless the user said not to.

A follow-up edit on an accepted image: a local change runs on the accepted image (as a fix on the
best try); a change to the whole image starts again from the original with the new change merged
into one prompt ([result-check-and-retry.md](references/result-check-and-retry.md) › Follow-up
edits).

## Parameters
| Parameter | Default | Where |
|---|---|---|
| model | ladder: `fal-ai/nano-banana-2` and `fal-ai/nano-banana-pro`; retries and fixes: the picked try's model | model-and-rook-call.md |
| resolution | `2K` | model-and-rook-call.md |
| aspect_ratio | the input's ratio, or `auto` | model-and-rook-call.md |
| prompt ladder | 3 prompts (simple, structured, detailed) × 2 models = 6 tries | steps 3–4 |
| retry cap | 5 tries after the ladder | step 6 |
| drift review threshold | 3 % per region | result-check-and-retry.md |

## Repository map
| Topic | Reference | Code |
|---|---|---|
| Scene inventory | `references/scene-inventory.md` | — |
| Template, prompt ladder, rules, failure → prompt fix | `references/prompt-writing.md` | — |
| Templates per kind of edit | `references/prompt-templates-per-edit.md` | — |
| Model choice, input preparation, the Rook call | `references/model-and-rook-call.md` | `scripts/prep_input.py` |
| Judging a try, recommending one, drift per region | `references/result-check-and-retry.md` | `scripts/compare.py` |
| Compare sheet | `references/result-check-and-retry.md` | `scripts/sheet.py` |

Run a script with `python -I <skill>/scripts/<name>.py --help` for its arguments.

## Example output
A work folder `<yymmdd>-<short-name>/` inside the folder that holds the input image, so the tries sit
next to the image they came from. It holds the ladder `try-01-simple-nb2.png`,
`try-02-simple-pro.png`, `try-03-structured-nb2.png`, `try-04-structured-pro.png`,
`try-05-detailed-nb2.png`, `try-06-detailed-pro.png`, any retries `try-07-<model>.png` …,
`sheet.jpg` (input and every try side by side, each labelled with rung, model and verdict) and
`log.md` (request, inventory, each prompt, each check, the recommendation, the user's pick).

## Changing this skill
The repo is public (`github.com/bai-ting-chen/bc-image-roaster`). Pull before editing
(`git pull --ff-only origin main`); commit as `bai-ting-chen` / `baitingchen.arch@gmail.com`.
Add only what holds for any image: prompt rules, failure → fix rows in prompt-writing.md, model facts
with their check date. Never project images, names or paths; one edit's results stay in its work
folder.
