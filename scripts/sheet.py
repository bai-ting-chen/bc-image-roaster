"""Make a labelled comparison grid (input first), at most three columns."""

import argparse
import io
import json
import math
from pathlib import Path
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps


def parse_box(value):
    try:
        box = tuple(float(part) for part in value.split(","))
        if (len(box) == 4 and all(math.isfinite(v) and 0 <= v <= 1 for v in box)
                and box[0] < box[2] and box[1] < box[3]):
            return box
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Use x0,y0,x1,y1 in 0..1, with x0<x1 and y0<y1.")


def make_sheet(paths, destination, box, labels):
    if labels is None:
        labels = [path.name for path in paths]
    if len(labels) != len(paths):
        raise ValueError("Supply one label per image, including the input.")
    if destination.exists() or destination.resolve() in {p.resolve() for p in paths}:
        raise ValueError(f"Refusing to overwrite: {destination}")
    tiles = []
    for path in paths:
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
        if box:
            bounds = tuple(round(v * image.size[i % 2]) for i, v in enumerate(box))
            if bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
                raise ValueError(f"Crop is smaller than one pixel: {path}")
            image = image.crop(bounds)
        tiles.append(image)
    width = tiles[0].width if box else min(1000, *(image.width for image in tiles))
    tiles = [image.resize((width, max(1, round(image.height * width / image.width))),
                          Image.Resampling.LANCZOS) for image in tiles]
    font = ImageFont.load_default(size=20)
    wrapped = [textwrap.wrap(label, width=max(1, width // 12)) or [""] for label in labels]
    label_height = max(map(len, wrapped)) * 26 + 16
    height = max(image.height for image in tiles) + label_height
    columns = min(3, len(tiles))
    rows = math.ceil(len(tiles) / columns)
    canvas = Image.new("RGB", (columns * width, rows * height), "#333333")
    draw = ImageDraw.Draw(canvas)
    for index, (image, lines) in enumerate(zip(tiles, wrapped)):
        x, y = index % columns * width, index // columns * height
        draw.multiline_text((x + 6, y + 6), "\n".join(lines), font=font,
                            fill="white", spacing=6)
        canvas.paste(image, (x, y + label_height))

    # Inspection crops keep their pixel scale; only overview sheets may shrink.
    while True:
        for quality in ((95, 90, 85, 80, 75, 70) if box else (95, 90, 85, 80)):
            stream = io.BytesIO()
            canvas.save(stream, "JPEG", quality=quality)
            data = stream.getvalue()
            if len(data) <= 5_000_000:
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("xb") as output:
                    output.write(data)
                return {"path": str(destination.resolve()), "bytes": len(data),
                        "pixel_size": canvas.size, "quality": quality,
                        "tile_count": len(tiles), "columns": columns, "rows": rows,
                        "box": box, "labels": labels}
        if box:
            raise ValueError("Quality 70 still exceeds 5 MB; use a smaller box.")
        canvas = canvas.resize((max(1, round(canvas.width * .85)),
                                max(1, round(canvas.height * .85))),
                               Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("tries", nargs="+", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--box", type=parse_box, help="Fractional crop x0,y0,x1,y1.")
    parser.add_argument("--labels", nargs="+", help="Labels in image order (quote spaces).")
    args = parser.parse_args()
    try:
        print(json.dumps(make_sheet([args.input, *args.tries], args.out, args.box, args.labels)))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
