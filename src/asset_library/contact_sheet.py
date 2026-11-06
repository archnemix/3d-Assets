"""Build a labeled review sheet from full-resolution inspection images."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LABELS = {
    "orbit-00": "01 / front (+Z)",
    "orbit-01": "02 / front-right",
    "orbit-02": "03 / right",
    "orbit-03": "04 / back-right",
    "orbit-04": "05 / back",
    "orbit-05": "06 / back-left",
    "orbit-06": "07 / left",
    "orbit-07": "08 / front-left",
    "top": "09 / top",
    "bottom": "10 / bottom",
    "clay": "11 / clay",
    "wireframe": "12 / triangle wireframe",
}


def build(previews: Path, title: str) -> Path:
    cell_width, cell_height, columns = 426, 462, 3
    sheet = Image.new("RGB", (columns * cell_width, 4 * cell_height + 70), "#f4f5f7")
    draw = ImageDraw.Draw(sheet)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = (
        ImageFont.truetype(font_path, 17) if Path(font_path).exists() else ImageFont.load_default()
    )
    draw.text((20, 15), title[:78], fill="#17212b", font=font)
    draw.text(
        (20, 42),
        "CANDIDATE - not approved | Full-size views are beside this sheet",
        fill="#596575",
        font=font,
    )
    for index, (name, label) in enumerate(LABELS.items()):
        left = index % columns * cell_width
        top = index // columns * cell_height + 70
        with Image.open(previews / f"{name}.jpg") as image:
            image = image.convert("RGB").resize((426, 426), Image.Resampling.LANCZOS)
            sheet.paste(image, (left, top))
        draw.text((left + 12, top + 434), label, fill="#17212b", font=font)
    path = previews / "contact-sheet.jpg"
    sheet.save(path, quality=91, optimize=True)
    return path
