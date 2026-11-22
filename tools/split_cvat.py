"""Tach mot file CVAT for images 1.1 thanh hai file theo khoang slot.

Cach lam: cat o muc text, giu nguyen dinh dang goc (khong parse lai XML),
nen header <meta>, thu tu thuoc tinh va khoang trang trong tung <image> giu nguyen.

Chay tu goc repo:
    python tools/split_cvat.py <zip-goc> <out-dir>
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

IMAGE_OPEN = re.compile(r'<image\b[^>]*\bname="([^"]+)"[^>]*>')
IMG_CLOSE = "</image>"


def collect_slots(text: str) -> list[tuple[str, str]]:
    """Tra ve danh sach (slot, doan_text_cua_image)."""
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
        name = m.group(1)
        slot = Path(name).name.split("_")[0]
        out.append((slot, text[m.start():end]))
        pos = end
    return out


def split_text(text: str, keep: set[str]) -> str:
    first = IMAGE_OPEN.search(text)
    if not first:
        raise SystemExit("khong tim thay the <image> nao")
    last_end = text.rfind(IMG_CLOSE) + len(IMG_CLOSE)
    header = text[: first.start()]
    footer = text[last_end:]
    parts = [seg for slot, seg in collect_slots(text) if slot in keep]
    if not parts:
        raise SystemExit("khong co image nao khop")
    return header + "\n".join(parts) + footer


def write_zip(path: Path, xml: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("annotations.xml", xml)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip())
        return 2
    src = Path(argv[1])
    out_dir = Path(argv[2])
    with zipfile.ZipFile(src) as zf:
        text = zf.read("annotations.xml").decode("utf-8")

    slots = [slot for slot, _ in collect_slots(text)]
    print(f"tong so image: {len(slots)}")
    print("  ", " ".join(slots))

    # File 1: 16 anh dau (A01..A16). File 2: phan con lai (B01..B12).
    part1 = set(slots[:16])
    part2 = set(slots[16:])

    p1 = out_dir / (src.stem.split("_annotations")[0] + "_part1_" + sorted(part1)[0] + "-" + sorted(part1)[-1] + ".zip")
    p2 = out_dir / (src.stem.split("_annotations")[0] + "_part2_" + sorted(part2)[0] + "-" + sorted(part2)[-1] + ".zip")

    write_zip(p1, split_text(text, part1))
    write_zip(p2, split_text(text, part2))

    print(f"file 1: {p1.name}  ({len(part1)} anh: {sorted(part1)[0]}..{sorted(part1)[-1]})")
    print(f"file 2: {p2.name}  ({len(part2)} anh: {sorted(part2)[0]}..{sorted(part2)[-1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
