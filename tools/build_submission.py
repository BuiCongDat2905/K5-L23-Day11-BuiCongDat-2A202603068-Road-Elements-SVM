"""Dung hai file nop bai tu mot file CVAT for images 1.1 cua job 59.

Viec script lam, theo thu tu:
1. Tach <image> thanh tung block text, giu nguyen dinh dang goc.
2. Camera hai ben (B05, B07, B08): moi lane doi position thanh other (QC1-03).
3. Xoa diem lap lien nhau trong points= (QC1-12: click hai lan mot cho).
4. Danh so lai id 0..n-1 va sua <job><size>, <stop_frame>, <segment><stop> cho khop.
5. Ghi hai zip: <ten>-front.zip (A01..A16) va <ten>-fisheye.zip (B01..B12).

Chay tu goc repo:
    python tools/build_submission.py <zip-goc> submission <ten>
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

IMAGE_OPEN = re.compile(r'<image\b[^>]*\bname="([^"]+)"[^>]*>')
IMG_CLOSE = "</image>"
POINTS = re.compile(r'(points=")([^"]*)(")')
LANE_POLY = re.compile(r'<polyline label="lane".*?</polyline>', re.S)
POSITION_ATTR = re.compile(r'(<attribute name="position">)([^<]*)(</attribute>)')

# Camera hai ben: position luon la other.
SIDE_CAMERA_SLOTS = {"B05", "B07", "B08"}


def image_blocks(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    pos = 0
    while True:
        m = IMAGE_OPEN.search(text, pos)
        if not m:
            break
        end = text.find(IMG_CLOSE, m.end())
        if end < 0:
            raise SystemExit(f"thieu </image> sau {m.group(1)}")
        end += len(IMG_CLOSE)
        slot = Path(m.group(1)).name.split("_")[0]
        out.append((slot, text[m.start():end]))
        pos = end
    return out


def dedupe_points(block: str) -> str:
    def fix(m: re.Match[str]) -> str:
        raw = m.group(2)
        pts = raw.split(";")
        kept: list[str] = []
        for p in pts:
            if not kept or p != kept[-1]:
                kept.append(p)
        return m.group(1) + ";".join(kept) + m.group(3)

    return POINTS.sub(fix, block)


def force_other(block: str) -> str:
    def fix_poly(m: re.Match[str]) -> str:
        return POSITION_ATTR.sub(lambda a: a.group(1) + "other" + a.group(3), m.group(0))

    return LANE_POLY.sub(fix_poly, block)


def renumber(block: str, new_id: int) -> str:
    return re.sub(r'(<image\b[^>]*\bid=")\d+(")', lambda m: m.group(1) + str(new_id) + m.group(2), block, count=1)


def fix_meta(header: str, count: int) -> str:
    header = re.sub(r"(<size>)\d+(</size>)", lambda m: m.group(1) + str(count) + m.group(2), header, count=1)
    header = re.sub(r"(<stop_frame>)\d+(</stop_frame>)", lambda m: m.group(1) + str(count - 1) + m.group(2), header, count=1)
    # segment cua job: start 0, stop count-1
    header = re.sub(r"(<segments>\s*<segment>\s*<id>[^<]*</id>\s*<start>)\d+(</start>\s*<stop>)\d+(</stop>)",
                    lambda m: m.group(1) + "0" + m.group(2) + str(count - 1) + m.group(3), header, count=1)
    return header


def build(text: str, slots_wanted: list[str]) -> str:
    blocks = image_blocks(text)
    first = IMAGE_OPEN.search(text)
    last_end = text.rfind(IMG_CLOSE) + len(IMG_CLOSE)
    header = text[: first.start()]
    footer = text[last_end:]

    by_slot: dict[str, list[str]] = {}
    for slot, block in blocks:
        by_slot.setdefault(slot, []).append(block)

    picked: list[str] = []
    for i, slot in enumerate(slots_wanted):
        for block in by_slot.get(slot, []):
            if slot in SIDE_CAMERA_SLOTS:
                block = force_other(block)
            block = dedupe_points(block)
            picked.append(renumber(block, i))

    return fix_meta(header, len(picked)) + "\n".join(picked) + footer


def write_zip(path: Path, xml: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("annotations.xml", xml)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip())
        return 2
    src, out_dir, name = Path(argv[1]), Path(argv[2]), argv[3]
    with zipfile.ZipFile(src) as zf:
        text = zf.read("annotations.xml").decode("utf-8")

    slots = [slot for slot, _ in image_blocks(text)]
    front = [f"A{i:02d}" for i in range(1, 17)]
    fisheye = [f"B{i:02d}" for i in range(1, 13)]

    missing = [s for s in front + fisheye if s not in slots]
    if missing:
        raise SystemExit(f"thieu anh trong zip goc: {missing}")

    p_front = out_dir / f"{name}-front.zip"
    p_fish = out_dir / f"{name}-fisheye.zip"
    write_zip(p_front, build(text, front))
    write_zip(p_fish, build(text, fisheye))

    print(f"front   : {p_front}  ({len(front)} anh)")
    print(f"fisheye : {p_fish}  ({len(fisheye)} anh)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
