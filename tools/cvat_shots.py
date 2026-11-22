"""Chup 4 man hinh CVAT that cho bao cao.

1. cvat1-labels.png   task day11 (#67) voi du 6 label ve + 4 label Tag
2. cvat2-front.png    job 59 frame 7 (A08) da gan du
3. cvat3-fisheye.png  job 59 frame 22 (B07) fisheye, phong to doan polyline cong
4. cvat4-xml.png      annotations.xml mo trong trinh duyet

Chay:
    $env:CVAT_USER="..."; $env:CVAT_PASS="..."; $env:CVAT_XML="<duong dan zip hoac xml>"
    python tools/cvat_shots.py
"""

from __future__ import annotations

import os
import tempfile
import traceback
import zipfile
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

BASE = "http://localhost:8080"
OUT = Path("submission/figures")


def login(page: Page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    page.fill("#credential", os.environ["CVAT_USER"])
    page.keyboard.press("Enter")
    page.wait_for_selector("#password", timeout=15000)
    page.fill("#password", os.environ["CVAT_PASS"])
    page.keyboard.press("Enter")
    page.wait_for_timeout(5000)
    print("sau dang nhap:", page.url)


def shot_task_labels(page: Page) -> None:
    page.goto(f"{BASE}/tasks/67", wait_until="networkidle")
    page.wait_for_timeout(3000)
    page.screenshot(path=str(OUT / "cvat1-labels.png"))
    print("cvat1:", page.url)


def shot_job(page: Page, frame: int, name: str, zoom_steps: int = 0) -> None:
    page.goto(f"{BASE}/tasks/67/jobs/59?frame={frame}", wait_until="networkidle")
    page.wait_for_timeout(6000)
    box = page.query_selector(".cvat-canvas-container") or page.query_selector("canvas")
    if box and zoom_steps:
        b = box.bounding_box()
        if b:
            page.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.keyboard.down("Control")
            for _ in range(zoom_steps):
                page.mouse.wheel(0, -220)
                page.wait_for_timeout(600)
            page.keyboard.up("Control")
            page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / name))
    print(name + ":", page.url)


def shot_xml(page: Page, xml_path: Path) -> None:
    """Mo doan XML thanh text/plain de thay nguyen van <polyline label="lane">."""
    text = xml_path.read_text(encoding="utf-8")
    start = text.find('<image id="0"')
    end = text.find("</image>", start)
    block = text[start : end + len("</image>")]
    lines = block.splitlines()
    keep: list[str] = []
    for ln in lines:
        keep.append(ln)
        if 'label="lane"' in ln and len(keep) > 5:
            # giu them 6 dong thuoc tinh cua lane dau tien roi dung
            idx = lines.index(ln)
            keep = lines[: idx + 7]
            break
    snippet = Path(tempfile.gettempdir()) / "cvat_annotations_snippet.txt"
    snippet.write_text("\n".join(keep), encoding="utf-8")
    page.goto(snippet.as_uri())
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT / "cvat4-xml.png"))
    print("cvat4:", page.url)


def resolve_xml() -> Path:
    raw = os.environ.get("CVAT_XML", "")
    src = Path(raw) if raw else Path("")
    if src.exists() and src.suffix == ".xml":
        return src.resolve()
    if src.exists() and src.suffix == ".zip":
        tmp = Path(tempfile.gettempdir()) / "cvat_annotations.xml"
        tmp.write_bytes(zipfile.ZipFile(src).read("annotations.xml"))
        return tmp.resolve()
    raise SystemExit(f"khong tim thay CVAT_XML: {raw!r}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    xml = resolve_xml()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})
        login(page)
        for fn in (
            lambda: shot_task_labels(page),
            lambda: shot_job(page, 7, "cvat2-front.png"),
            lambda: shot_job(page, 22, "cvat3-fisheye.png", zoom_steps=4),
            lambda: shot_xml(page, xml),
        ):
            try:
                fn()
            except Exception:
                traceback.print_exc()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
