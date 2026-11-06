"""Prepare full-resolution JPEG copies within Rook's byte limits."""

import argparse
import io
import json
from pathlib import Path
import sys

from PIL import Image, ImageOps


IMAGE_LIMIT = 10_000_000
TOTAL_LIMIT = 15_000_000


def prepare(paths, out_dir):
    if len(paths) > 9:
        raise ValueError("Rook allows at most 8 references.")
    destinations = [out_dir / "input.jpg"] + [
        out_dir / f"ref-{index:02d}.jpg" for index in range(1, len(paths))]
    sources = {path.resolve() for path in paths}
    for destination in destinations:
        if destination.resolve() in sources or destination.exists():
            raise ValueError(f"Refusing to overwrite: {destination}")

    images, records, profiles = [], [], []
    for path, destination in zip(paths, destinations):
        with Image.open(path) as source:
            images.append(ImageOps.exif_transpose(source).convert("RGB"))
            profiles.append(source.info.get("icc_profile") if source.mode == "RGB" else None)
        records.append({"source": str(path.resolve()),
                        "path": str(destination.resolve()),
                        "original_bytes": path.stat().st_size,
                        "pixel_size": images[-1].size})

    # Lower the whole batch together so the aggregate cap includes every reference.
    for quality in (95, 90, 85, 80):
        encoded = []
        for image, profile in zip(images, profiles):
            stream = io.BytesIO()
            image.save(stream, "JPEG", quality=quality, subsampling=0,
                       icc_profile=profile)
            encoded.append(stream.getvalue())
        sizes = [len(data) for data in encoded]
        if max(sizes) < IMAGE_LIMIT and sum(sizes) < TOTAL_LIMIT:
            break
    else:
        raise ValueError("Quality 80 still exceeds the 10 MB/image or 15 MB total cap; "
                         "resizing is needed. No files written.")

    out_dir.mkdir(parents=True, exist_ok=True)
    for destination, data, record in zip(destinations, encoded, records):
        with destination.open("xb") as stream:
            stream.write(data)
        record.update(new_bytes=len(data), quality=quality)
    return {"images": records, "total_bytes": sum(sizes)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--refs", nargs="+", type=Path, default=[], help="Reference images.")
    args = parser.parse_args()
    try:
        print(json.dumps(prepare([args.image, *args.refs], args.out_dir)))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
