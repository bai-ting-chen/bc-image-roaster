# Model and Rook call: which model, input preparation, the call, limits

Checked 2026-11-06. Prices change; recheck the fal
pages before quoting them to the user.

## Which model
| Model id | Use | 2K price | Time per call |
|---|---|---:|---:|
| `fal-ai/nano-banana-2` | every ladder prompt; retries and fixes when the picked try is NB2 | $0.12 | 23–28 s |
| `fal-ai/nano-banana-pro` | every ladder prompt; retries and fixes when the picked try is Pro | $0.15 | 30–56 s |

The ladder runs on both: 3 × $0.12 + 3 × $0.15 ≈ $0.81 per edit before retries. Why both: which
model suits an edit is not known in advance. On small edits (3 images × 4 prompt forms) NB2 did at
least as well as Pro and Pro made the larger unrequested changes (reframing, extra objects); on a
whole-image render of a viewport capture Pro gave more realistic planting and people but drifted
more in geometry (roof, shadows). GPT Image 2 is not used: Rook's tool fails on fal async jobs for
it.

## The call
Check Rook first (`rhino_ping`). Call `rhino_render_view` (if hidden, find it with
`rook_tools_search`):

| Argument | Value |
|---|---|
| `input_image_path` | absolute path of the prepared `input.jpg` (from `scripts/prep_input.py`) |
| `prompt` | the prompt as shown to the user, word for word |
| `model` | `fal-ai/nano-banana-2` (or `-pro`) |
| `resolution` | `2K` (default); `1K` for a quick look; `4K` only if the user asks |
| `aspect_ratio` | the input's ratio, e.g. `16:9`, or `auto`; never `match_input_image` |
| `reference_image_paths` | prepared reference images, at most 8 |
| `port` | the Rhino instance from `rhino_ping`; needed when several Rhino windows are open (the call is refused without it) |

Copy the result into the work folder as `try-NN-<rung>-<model>.png` (ladder) or
`try-NN-<model>.png` (retries), model `nb2` or `pro`. Rook also keeps every result and its prompt
in `%APPDATA%\Rook\artifacts\`.

## Limits
- Rook: 10 MB per image, 15 MB for input + references together, prompt up to 16 KB.
  `prep_input.py` handles the sizes.
- Rook does not expose seed, number of outputs or output format, though fal supports them.
- Outputs come back smaller than large inputs: 5000 px wide in, 2752 px out at 2K. Small text
  and fine detail do not survive the redraw.
