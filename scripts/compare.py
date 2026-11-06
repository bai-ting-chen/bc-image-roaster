"""Align two images and flag regional changes. Requires Pillow; no numpy.

Usage: python compare.py INPUT OUTPUT OUT_FOLDER [--no-crops]
The score measures appearance change, not edit success or unwanted change.
"""

import argparse
import csv
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, ImageStat


def load_rgb(path):
    with Image.open(path) as image:
        return ImageOps.exif_transpose(image).convert("RGB")


def warp(image, scale, dx, dy, resample=Image.Resampling.BICUBIC):
    """Output coordinates sample source at center + scale * offset + shift."""
    width, height = image.size
    return image.transform(image.size, Image.Transform.AFFINE,
                           (scale, 0, (1 - scale) * width / 2 + dx,
                            0, scale, (1 - scale) * height / 2 + dy),
                           resample=resample)


def region_boxes(width, height, inset=(0, 0)):
    for row in range(3):
        for col in range(3):
            yield f"r{row + 1}c{col + 1}", (
                max(inset[0], col * width // 3),
                max(inset[1], row * height // 3),
                min(width - inset[0], (col + 1) * width // 3),
                min(height - inset[1], (row + 1) * height // 3))


def alignment_loss(original, candidate):
    # Drop the three most changed tiles so one local edit cannot steer alignment.
    diff = ImageChops.difference(original, candidate)
    width, height = diff.size
    tiles = []
    for row in range(4):
        for col in range(4):
            box = (int((.06 + col * .22) * width),
                   int((.06 + row * .22) * height),
                   int((.06 + (col + 1) * .22) * width),
                   int((.06 + (row + 1) * .22) * height))
            tiles.append(ImageStat.Stat(diff.crop(box)).mean[0])
    return sum(sorted(tiles)[:13]) / 13


def align(original, output):
    best = (1.0, 0.0, 0.0)
    loss = None
    # Search scale and shifts jointly: they interact, especially near sharp edges.
    for max_side, scale_step, shift_step in [(256, .01, None),
                                             (384, .0025, .5),
                                             (768, .0005, .25)]:
        size = (max(24, round(original.width * max_side / max(original.size))),
                max(24, round(original.height * max_side / max(original.size))))
        a = original.resize(size, Image.Resampling.LANCZOS).convert("L")
        b = output.resize(size, Image.Resampling.LANCZOS).convert("L")
        if shift_step is None:
            candidates = ((1 + si * scale_step, x / size[0], y / size[1])
                          for si in range(-3, 4)
                          for x in sorted({0, *range(-math.ceil(size[0] * .025),
                                                    math.ceil(size[0] * .025) + 1, 2)})
                          for y in sorted({0, *range(-math.ceil(size[1] * .025),
                                                    math.ceil(size[1] * .025) + 1, 2)}))
            loss = float("inf")
            for scale, dx, dy in candidates:
                score = alignment_loss(a, warp(b, scale, dx * size[0], dy * size[1]))
                if score < loss:
                    best, loss = (scale, dx, dy), score
        else:
            loss = alignment_loss(a, warp(b, best[0], best[1] * size[0], best[2] * size[1]))
            center = best
            scale_radius = 4 if max_side == 384 else 2
            for si in range(-scale_radius, scale_radius + 1):
                for xi in range(-2, 3):
                    for yi in range(-2, 3):
                        trial = (center[0] + si * scale_step,
                                 center[1] + xi * shift_step / size[0],
                                 center[2] + yi * shift_step / size[1])
                        if not (.965 <= trial[0] <= 1.035 and
                                abs(trial[1]) <= .035 and abs(trial[2]) <= .035):
                            continue
                        score = alignment_loss(a, warp(b, trial[0], trial[1] * size[0],
                                                       trial[2] * size[1]))
                        if score < loss:
                            best, loss = trial, score
    return best, loss


def measure_regions(original, aligned):
    # A fixed 6% border keeps interpolation and missing shifted pixels out of scores.
    analysis_size = (max(24, round(original.width * 768 / max(original.size))),
                     max(24, round(original.height * 768 / max(original.size))))
    a = original.resize(analysis_size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    b = aligned.resize(analysis_size, Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    diff = ImageChops.difference(a, b)
    inset = tuple(math.ceil(side * .06) for side in analysis_size)
    rows = []
    for name, box in region_boxes(*analysis_size, inset):
        crop = diff.crop(box)
        channels = crop.split()
        max_channel = ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]), channels[2])
        histogram = max_channel.histogram()
        mean_pct = sum(ImageStat.Stat(crop).mean) / 3 / 255 * 100
        changed_pct = sum(histogram[25:]) / (crop.width * crop.height) * 100
        rows.append({"region": name, "mean_drift_pct": round(mean_pct, 4),
                     "pixels_over_24_pct": round(changed_pct, 4),
                     "review": mean_pct > 3.0})
    return rows, analysis_size, inset


def write_crops(original, native, aligned, scale_shift, out_folder):
    scale, dx, dy = scale_shift
    for name, box in region_boxes(*original.size):
        left, middle = original.crop(box), aligned.crop(box)
        # Third panel is the corresponding output crop at native 100% pixel scale.
        x0, y0, x1, y1 = box
        mapped = ((scale * x0 + (1 - scale) * original.width / 2 + dx * original.width) * native.width / original.width,
                  (scale * y0 + (1 - scale) * original.height / 2 + dy * original.height) * native.height / original.height,
                  (scale * x1 + (1 - scale) * original.width / 2 + dx * original.width) * native.width / original.width,
                  (scale * y1 + (1 - scale) * original.height / 2 + dy * original.height) * native.height / original.height)
        native_box = (max(0, round(mapped[0])), max(0, round(mapped[1])),
                      min(native.width, round(mapped[2])), min(native.height, round(mapped[3])))
        right = native.crop(native_box)
        canvas = Image.new("RGB", (left.width + middle.width + right.width,
                                   max(left.height, right.height) + 30), "#333333")
        canvas.paste(left, (0, 30))
        canvas.paste(middle, (left.width, 30))
        canvas.paste(right, (left.width + middle.width, 30))
        draw = ImageDraw.Draw(canvas)
        for x, title in [(0, "INPUT 100%"), (left.width, "OUTPUT aligned / resampled to input"),
                         (left.width + middle.width, "OUTPUT native 100%")]:
            draw.text((x + 5, 7), title, fill="white")
        canvas.save(out_folder / f"{name}-crops.png")


def write_table(result, out_folder):
    rows = result["regions"]
    scale = result["scale"]
    dx, dy = result["shift_fraction_x"], result["shift_fraction_y"]
    (out_folder / "drift.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (out_folder / "drift.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("| Region | Mean drift % | Pixels >24 % | Review >3% |")
    print("|---|---:|---:|---|")
    for row in rows:
        print(f"| {row['region']} | {row['mean_drift_pct']:.4f} | "
              f"{row['pixels_over_24_pct']:.4f} | {row['review']} |")
    print(f"Alignment scale={scale:.6f}, shift=({dx:.6f}, {dy:.6f}); "
          f"max drift={result['max_region_drift_pct']:.4f}%")


def compare(input_path, output_path, out_folder, no_crops=False):
    original, native = load_rgb(input_path), load_rgb(output_path)
    scale_shift, loss = align(original, native)
    scale, dx, dy = scale_shift
    normalized = native.resize(original.size, Image.Resampling.LANCZOS)
    aligned = warp(normalized, scale, dx * original.width, dy * original.height)
    rows, analysis_size, inset = measure_regions(original, aligned)
    out_folder.mkdir(parents=True, exist_ok=True)
    if not no_crops:
        write_crops(original, native, aligned, scale_shift, out_folder)
    result = {"input": str(input_path.resolve()), "output": str(output_path.resolve()),
              "input_size": original.size, "output_size": native.size,
              "scale": scale, "shift_fraction_x": dx, "shift_fraction_y": dy,
              "alignment_loss_255": loss, "analysis_size": analysis_size,
              "excluded_border_px": inset, "threshold_mean_pct": 3.0,
              "max_region_drift_pct": max(row["mean_drift_pct"] for row in rows),
              "regions": rows}
    write_table(result, out_folder)
    return result


def main():
    parser = argparse.ArgumentParser(description="Align images and report regional drift (>3% flags review).")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("out_folder", type=Path)
    parser.add_argument("--no-crops", action="store_true", help="Write only drift.csv/json.")
    args = parser.parse_args()
    # Keep generated evidence away from either source image.
    if args.out_folder.resolve() in (args.input.resolve().parent, args.output.resolve().parent):
        parser.error("Use a separate output folder.")
    compare(args.input, args.output, args.out_folder, args.no_crops)


if __name__ == "__main__":
    main()
