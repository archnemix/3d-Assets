"""Combine recorded motion frames into a labelled inspection sheet."""

import sys
from pathlib import Path

from PIL import Image, ImageDraw


def main(directory: Path) -> None:
    frames = sorted(directory.glob("frame-*.jpg"))
    if len(frames) != 12:
        raise ValueError(f"Expected 12 sampled frames, got {len(frames)}")
    sheet = Image.new("RGB", (4 * 384, 3 * 414), "#f3f5f1")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(frames):
        x, y = (index % 4) * 384, (index // 4) * 414
        with Image.open(path) as image:
            sheet.paste(image.resize((384, 384)), (x, y))
        draw.text((x + 8, y + 390), path.stem, fill="#18242b")
    sheet.save(directory / "motion-contact.jpg", quality=90)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
