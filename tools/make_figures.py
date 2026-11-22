"""Sinh hinh minh hoa cho bao cao tu file nhan va anh goc.

Bon hinh:
  fig1-labels.png  : danh sach 6 label + 4 tag, ve tu taxonomy.py
  fig2-front-A08.png : anh A08 voi nhan ve chong len (lane, drivable, box)
  fig3-fisheye-B01.png : anh B01 + khung phong to doan polyline cong
  fig4-xml.png     : doan annotations.xml co <polyline label="lane">

Chay tu goc repo:
    python tools/make_figures.py submission/buicongdat-front.zip submission/buicongdat-fisheye.zip submission/figures
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from road_lab import cvat_xml  # noqa: E402

W = 1280
COLORS = {
    "lane": (255, 210, 0),
    "road_curb": (255, 120, 0),
    "crosswalk": (0, 220, 255),
    "drivable": (80, 255, 120),
    "traffic_light": (255, 60, 60),
    "traffic_sign": (120, 140, 255),
}


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in (
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def load(images: list[cvat_xml.Image], slot: str) -> cvat_xml.Image:
    for im in images:
        if Path(im.name).name.startswith(slot):
            return im
    raise SystemExit(f"khong thay anh {slot}")


def draw_shapes(img: Image.Image, im: cvat_xml.Image, width: int = 3) -> Image.Image:
    out = img.convert("RGB").copy()
    d = ImageDraw.Draw(out)
    for s in im.shapes:
        col = COLORS.get(s.label, (255, 255, 255))
        if s.kind == "rectangle":
            x1, y1 = s.points[0]
            x2, y2 = s.points[1]
            d.rectangle([x1, y1, x2, y2], outline=col, width=width)
        elif s.kind == "polygon":
            if len(s.points) >= 3:
                d.polygon([(x, y) for x, y in s.points], outline=col)
                d.line([(x, y) for x, y in s.points] + [s.points[0]], fill=col, width=width)
        elif s.kind == "polyline":
            if len(s.points) >= 2:
                d.line([(x, y) for x, y in s.points], fill=col, width=width)
    return out


def legend(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    f = font(22)
    for i, (name, col) in enumerate(COLORS.items()):
        yy = y + i * 30
        d.rectangle([x, yy + 6, x + 22, yy + 24], fill=col)
        d.text((x + 32, yy), name, fill=(255, 255, 255), font=f)


def fig_labels(out: Path) -> None:
    rows = [
        ("lane", "polyline", "position L1/R1/L2/R2/other, style solid/dashed, color white/yellow/other, kind single/double"),
        ("road_curb", "polyline", "khong thuoc tinh"),
        ("crosswalk", "polygon", "khong thuoc tinh"),
        ("drivable", "polygon", "area_type direct/alternative"),
        ("traffic_light", "rectangle", "color red/yellow/green/off/unknown, type vehicle/pedestrian/beacon, facing front/side/back, edge_zone"),
        ("traffic_sign", "rectangle", "group prohibitory/mandatory/warning/information/supplementary/other, facing, edge_zone"),
        ("camera (tag)", "tag", "value front/fisheye_front/fisheye_rear/fisheye_left/fisheye_right"),
        ("timeofday (tag)", "tag", "value day/dusk/night"),
        ("weather (tag)", "tag", "value clear/overcast/rain/fog/other"),
        ("source (tag)", "tag", "value real/simulated"),
    ]
    h = 90 + len(rows) * 54
    img = Image.new("RGB", (W, h), (28, 30, 34))
    d = ImageDraw.Draw(img)
    d.text((30, 24), "Road v1.0 - 6 label ve + 4 label Tag (sinh tu taxonomy.py)", fill=(255, 255, 255), font=font(28))
    f, fb = font(20), font(20)
    for i, (name, kind, attrs) in enumerate(rows):
        y = 88 + i * 54
        d.text((30, y), name, fill=(255, 210, 0), font=f)
        d.text((300, y), kind, fill=(140, 220, 255), font=f)
        d.text((470, y), attrs, fill=(210, 210, 210), font=fb)
    img.save(out)
    print("fig1:", out)


def fig_front(front: list[cvat_xml.Image], out: Path, slot: str = "A08") -> None:
    im = load(front, slot)
    src = Path("data") / Path(im.name).name
    base = Image.open(src)
    drawn = draw_shapes(base, im, width=4)
    d = ImageDraw.Draw(drawn)
    legend(d, 20, 20)
    n = len(im.shapes)
    caption(drawn, f"{slot} - {n} shape, {len(im.tags)} tag")
    drawn.save(out)
    print("fig2:", out)


def caption(img: Image.Image, text: str) -> None:
    d = ImageDraw.Draw(img)
    f = font(24)
    x, y = 18, img.height - 40
    w = d.textlength(text, font=f)
    d.rectangle([x - 8, y - 6, x + w + 8, y + 32], fill=(20, 22, 26))
    d.text((x, y), text, fill=(255, 255, 255), font=f)


def fig_fisheye(fish: list[cvat_xml.Image], out: Path) -> None:
    # Chon anh fisheye co polyline lane nhieu diem nhat de phong to doan cong.
    best: tuple[int, cvat_xml.Image] | None = None
    for im in fish:
        for s in im.shapes:
            if s.label == "lane" and (best is None or len(s.points) > best[0]):
                best = (len(s.points), im)
    if best is None:
        raise SystemExit("khong co lane nao trong file fisheye")
    im = best[1]
    slot = Path(im.name).name.split("_")[0]
    src = Path("data") / Path(im.name).name
    base = Image.open(src).convert("RGB")
    drawn = draw_shapes(base, im, width=4)
    legend(ImageDraw.Draw(drawn), 20, 20)

    lanes = [s for s in im.shapes if s.label == "lane"]
    if lanes:
        pts = lanes[0].points
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        box = (max(0, min(xs) - 60), max(0, min(ys) - 60), min(base.width, max(xs) + 60), min(base.height, max(ys) + 60))
        ImageDraw.Draw(drawn).rectangle(box, outline=(255, 255, 255), width=3)
        crop = drawn.crop(box)
        scale = min(2.0, 520 / max(1, crop.width), 520 / max(1, crop.height))
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
        canvas = Image.new("RGB", (base.width, base.height + crop.height + 20), (28, 30, 34))
        canvas.paste(drawn, (0, 0))
        canvas.paste(crop, (0, base.height + 10))
        caption(canvas, f"{slot} - phong to polyline cong ({len(pts)} diem)")
        canvas.save(out)
    else:
        drawn.save(out)
    print("fig3:", out)


def fig_xml(zip_path: Path, out: Path) -> None:
    text = zipfile.ZipFile(zip_path).read("annotations.xml").decode("utf-8")
    m = re.search(r'(<image\b[^>]*name="[^"]*A01[^"]*"[^>]*>.*?</image>)', text, re.S)
    block = m.group(1)
    lane = re.search(r'(<polyline label="lane".*?</polyline>)', block, re.S).group(1)
    head = m.group(1).split("\n")[0]
    lines = [head] + ["    " + ln.strip() for ln in lane.splitlines()]
    lines.append("  </image>")
    f = font(20)
    pad, lh = 24, 30
    img = Image.new("RGB", (W, pad * 2 + lh * len(lines) + 60), (30, 32, 36))
    d = ImageDraw.Draw(img)
    d.text((pad, pad), "annotations.xml - <polyline label=\"lane\"> cua A01", fill=(255, 255, 255), font=font(26))
    for i, ln in enumerate(lines):
        d.text((pad, pad + 56 + i * lh), ln, fill=(190, 230, 190), font=f)
    img.save(out)
    print("fig4:", out)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip())
        return 2
    front_zip, fish_zip, out_dir = Path(argv[1]), Path(argv[2]), Path(argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)
    front = cvat_xml.load(front_zip)
    fish = cvat_xml.load(fish_zip)

    fig_labels(out_dir / "fig1-labels.png")
    fig_front(front, out_dir / "fig2-front-A08.png")
    fig_fisheye(fish, out_dir / "fig3-fisheye-B01.png")
    fig_xml(front_zip, out_dir / "fig4-xml.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
