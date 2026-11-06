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

Read [RULES.md](RULES.md), then the reference for the step you are in. Light, fast edits on top of
an existing image; the core is the prompt, because the user writes rough English (not their first
language). No compositing or masking: drift is fought with wording, checking and retries. For slow,
exact photoreal renders use bc-archviz.

## Prerequisites
- Rook connected (`rhino_ping` returns pong); `rhino_render_view` reachable.
- Python 3.11 with Pillow (no numpy needed) for the scripts.
- The input image on disk; any reference image (an object to insert) on disk too.

## Workflow
1. **Read the image.** Intent: a scene inventory of targets, look-alikes and at-risk items
   (RULES EDT_01) → [image-reading.md](references/image-reading.md).
2. **Edit spec.** Intent: what changes, what stays, anchors for size and position; ask back only
   when needed (EDT_02).
3. **Prompt.** Intent: the spec in the prompt template, shown to the user before it runs (EDT_03)
   → [prompting.md](references/prompting.md), [edit-types.md](references/edit-types.md).
4. **Run.** Intent: one call through Rook on the prepared input (MOD_01) →
   [models.md](references/models.md).
5. **Check.** Intent: change done, nothing else changed; retry with one prompt fix (CHK_01, CHK_02)
   → [check.md](references/check.md).
6. **Deliver.** Intent: final image, compare sheet, one line per failed try (CHK_03).

A prompt handed in only to be tightened: steps 1–3. A follow-up edit: EDT_04.

## Parameters
| Parameter | Default | Where |
|---|---|---|
| model | `fal-ai/nano-banana-2` | models.md |
| resolution | `2K` | models.md |
| aspect_ratio | the input's ratio, or `auto` | models.md |
| retry cap | 3 tries | RULES CHK_02 |
| drift review threshold | 3 % per region | check.md |

## Task router
- [Image reading](references/image-reading.md): the scene inventory
- [Prompting](references/prompting.md): template, rules, failure → prompt fix
- [Edit types](references/edit-types.md): templates and vocabulary per kind of edit
- [Models](references/models.md): model choice, the Rook call, limits, prices
- [Check](references/check.md): judging a try, retries, delivery
- [Maintaining](references/skill-maintaining.md): skill changes, Git, sync

## Repository map
| Topic | Reference | Code |
|---|---|---|
| Input preparation, the Rook call | `references/models.md` | `scripts/prep_input.py` |
| Drift per region | `references/check.md` | `scripts/compare.py` |
| Compare sheet | `references/check.md` | `scripts/sheet.py` |

Run a script with `python -I <skill>/scripts/<name>.py --help` for its arguments.

## Example output
A work folder in the current project, `image-roaster/<yymmdd>-<short-name>/`, holding `try-01.png`
… (the last one is the result), `sheet.jpg` (input and every try side by side, each labelled with
model and verdict) and `log.md` (request, inventory, each prompt, each check).
