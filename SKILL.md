---
name: bc-image-roaster
description: >-
  Quick AI edits of an existing image (render, viewport capture or photo) with Nano Banana 2 / Pro
  through Rook: turns the user's rough request into a precise edit prompt, runs it, checks the
  result for the change and for drift, and retries with a fixed prompt. Use whenever the user wants
  to change something in an image (swap or remove an object, change a material, planting, sky,
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
   item → [scene-inventory.md](references/scene-inventory.md).
2. **Edit spec:** what changes, what stays, anchors for size and position. Take the user's words at
   their full scope. Ask back only when the request and the image disagree (count, which object) or
   a word has two readings (evening: dusk or night); otherwise decide and say what was decided.
3. **Prompt:** the spec in the template → [prompt-writing.md](references/prompt-writing.md),
   [prompt-templates-per-edit.md](references/prompt-templates-per-edit.md). Before the first
   run, show the prompt as it will be sent with one plain-English line on why; warn when the image
   holds small text.
4. **Run** one call through Rook on the prepared input, with the defaults under Parameters →
   [model-and-rook-call.md](references/model-and-rook-call.md).
5. **Check** the change and the preservation separately, from full-size crops against the
   inventory; the drift number only says where to look →
   [result-check-and-retry.md](references/result-check-and-retry.md). A try fails: name the
   failure, change one thing in the prompt, retry. After the retry cap, run the best prompt once on
   `fal-ai/nano-banana-pro`, or ask the user.
6. **Deliver** the final image, the compare sheet of the input and every try, and one line per
   failed try; then delete prepared copies and crops.

A prompt the user hands in: tighten it in steps 1–3, show it, then run it (steps 4–6) unless the
user said not to.

A follow-up edit: start again from the original image and merge the new change into one prompt.
Offer one chained step only after the retry cap, still checked against the original
([result-check-and-retry.md](references/result-check-and-retry.md) › Follow-up edits).

## Parameters
| Parameter | Default | Where |
|---|---|---|
| model | `fal-ai/nano-banana-2` | model-and-rook-call.md |
| resolution | `2K` | model-and-rook-call.md |
| aspect_ratio | the input's ratio, or `auto` | model-and-rook-call.md |
| retry cap | 3 tries | step 5 |
| drift review threshold | 3 % per region | result-check-and-retry.md |

## Repository map
| Topic | Reference | Code |
|---|---|---|
| Scene inventory | `references/scene-inventory.md` | — |
| Template, rules, failure → prompt fix | `references/prompt-writing.md` | — |
| Templates per kind of edit | `references/prompt-templates-per-edit.md` | — |
| Model choice, input preparation, the Rook call | `references/model-and-rook-call.md` | `scripts/prep_input.py` |
| Judging a try, drift per region | `references/result-check-and-retry.md` | `scripts/compare.py` |
| Compare sheet | `references/result-check-and-retry.md` | `scripts/sheet.py` |

Run a script with `python -I <skill>/scripts/<name>.py --help` for its arguments.

## Example output
A work folder in the current project, `image-roaster/<yymmdd>-<short-name>/`, holding `try-01.png`
… (the last one is the result), `sheet.jpg` (input and every try side by side, each labelled with
model and verdict) and `log.md` (request, inventory, each prompt, each check).

## Changing this skill
The repo is public (`github.com/bai-ting-chen/bc-image-roaster`). Pull before editing
(`git pull --ff-only origin main`); commit as `bai-ting-chen` / `baitingchen.arch@gmail.com`.
Add only what holds for any image: prompt rules, failure → fix rows in prompt-writing.md, model facts
with their check date. Never project images, names or paths; one edit's results stay in its work
folder.
