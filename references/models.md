# Models and the Rook call

Checked 2026-11-06. Prices change; recheck the fal
pages before quoting them to the user.

## Which model
| Model id | Use | 2K price | Time per call |
|---|---|---:|---:|
| `fal-ai/nano-banana-2` | **default** | $0.12 | 23–28 s |
| `fal-ai/nano-banana-pro` | escalation, once, after the retry cap (RULES CHK_02) | $0.15 | 30–56 s |

In testing (3 images × 4 prompt forms) NB2 did at least as well as Pro on every image; Pro made the
larger unrequested changes (reframing, extra objects). GPT Image 2 is not used: Rook's tool fails
on fal async jobs for it.

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

Copy the result into the work folder as `try-NN.png`. Rook also keeps every result and its prompt
in `%APPDATA%\Rook\artifacts\`.

## Limits
- Rook: 10 MB per image, 15 MB for input + references together, prompt up to 16 KB.
  `prep_input.py` handles the sizes.
- Rook does not expose seed, number of outputs or output format, though fal supports them.
- Outputs come back smaller than large inputs: 5000 px wide in, 2752 px out at 2K. Small text
  and fine detail do not survive the redraw.
