"""Dien Phieu QC 1 tu file export cua ban duoc ghep lo.

Chi lam phan may lam duoc: chon mau 6 anh, dem so nhan da kiem, lay canh bao
cua road_check lint lam ung vien loi, xep muc theo CODE_LEVEL, tinh ti le va
ra quyet dinh theo luat. Con lai phai nguoi kiem xac nhan: lint khong co GT nen
QC1-05 (vach dut bi tach) co the la canh bao sai.

Chay tu goc repo:
    python tools/make_qc1.py <peer-front.zip> <peer-fisheye.zip> <ten-nguoi-kiem> <ten-ban-kia>
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from road_lab import cvat_xml, road_check  # noqa: E402

CODES = [
    ("QC1-01", "tag camera", "sai thuộc tính / bỏ sót"),
    ("QC1-02", "đủ L1, R1", "bỏ sót"),
    ("QC1-03", "position", "sai thuộc tính / thừa"),
    ("QC1-04", "tâm vạch, chiều, điểm dừng", "sai phạm vi / bỏ sót"),
    ("QC1-05", "vạch đứt, che", "sai phạm vi / sai thuộc tính"),
    ("QC1-06", "style, color, kind", "sai thuộc tính"),
    ("QC1-07", "vùng lái", "sai phạm vi / bỏ sót / thừa"),
    ("QC1-08", "đèn, màu", "bỏ sót / sai phạm vi / sai thuộc tính"),
    ("QC1-09", "facing, type, group, biển phụ", "sai thuộc tính"),
    ("QC1-10", "hình in, đủ biển", "bỏ sót / sai phạm vi"),
    ("QC1-11", "fisheye", "sai phạm vi / sai thuộc tính"),
    ("QC1-12", "file", "lỗi file"),
]

LEVEL_VI = {"critical": "nặng", "major": "chính", "minor": "nhẹ"}


def slot_of(name: str) -> str:
    return Path(name).name.split("_")[0]


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__.strip())
        return 2
    front, fish, checker, peer = Path(argv[1]), Path(argv[2]), argv[3], argv[4]

    images: list[cvat_xml.Image] = []
    for p in (front, fish):
        images.extend(cvat_xml.load(p))

    wanted = {"A01", "A02", "A03", "B01", "B02", "B03"}
    sample = [im for im in images if slot_of(im.name) in wanted]
    sample.sort(key=lambda im: slot_of(im.name))
    if len(sample) < 6:
        raise SystemExit(f"chi tim thay {len(sample)} anh trong mau can 6")

    by_name = {slot_of(im.name): im for im in sample}
    counts = {im.name: len(im.shapes) + len(im.tags) for im in sample}
    total_labels = sum(counts.values())

    findings = [f for f in road_check.lint(images) if slot_of(f.image) in by_name]

    per_code: dict[str, int] = {code: 0 for code, _, _ in CODES}
    checked_per_code: dict[str, int] = {code: 0 for code, _, _ in CODES}
    rows: list[str] = []

    def ref_with_id(f) -> str:
        """Them #index cua shape khi canh bao chi ghi ten label."""
        if "#" in f.ref:
            return f.ref
        im = by_name.get(slot_of(f.image))
        if im:
            for i, s in enumerate(im.shapes):
                if s.label == f.ref:
                    return f"{f.ref}#{i}"
        return f.ref

    for f in findings:
        per_code[f.code] = per_code.get(f.code, 0) + 1
        rows.append(
            f"| {len(rows) + 1} | {f.code} | {slot_of(f.image)} | {ref_with_id(f)} | "
            f"{road_check.SEV_VI.get(f.severity, f.severity)} | {f.message} |"
        )

    # So muc kiem moi ma: dem so doi tuong da xem cho ma do.
    for im in sample:
        for code, _, _ in CODES:
            if code == "QC1-01":
                checked_per_code[code] += len(im.tags)
            elif code in ("QC1-02", "QC1-03", "QC1-04", "QC1-05", "QC1-06"):
                checked_per_code[code] += sum(1 for s in im.shapes if s.label == "lane")
            elif code == "QC1-07":
                checked_per_code[code] += sum(1 for s in im.shapes if s.label in ("drivable", "crosswalk", "road_curb"))
            elif code in ("QC1-08", "QC1-09", "QC1-10"):
                checked_per_code[code] += sum(1 for s in im.shapes if s.label in ("traffic_light", "traffic_sign"))
            elif code == "QC1-11":
                checked_per_code[code] += sum(1 for s in im.shapes if slot_of(im.name).startswith("B"))
            elif code == "QC1-12":
                checked_per_code[code] += 2  # hai file zip

    critical = sum(1 for f in findings if f.severity == "critical")
    major = sum(1 for f in findings if f.severity == "major")
    minor = sum(1 for f in findings if f.severity == "minor")
    rate = (major / total_labels * 100) if total_labels else 0.0

    if critical:
        decision = "Rework"
        reason = f"có {critical} lỗi nặng; luật: một lỗi nặng là đủ Rework"
    elif rate > 5:
        decision = "Rework"
        reason = f"lỗi chính {major}/{total_labels} = {rate:.1f} % > 5 %"
    else:
        decision = "Release"
        reason = f"0 lỗi nặng, lỗi chính {major}/{total_labels} = {rate:.1f} % ≤ 5 %"

    table = "\n".join(
        f"| {code} {name} | {kind} | {checked_per_code[code]} | {per_code[code]} | "
        f"{road_check.CODE_LEVEL.get(code, 'nhẹ')} |"
        for code, name, kind in CODES
    )
    error_rows = "\n".join(rows) if rows else "|  |  |  |  |  |  |"

    doc = f"""# Phiếu QC 1 — Road v1.0

Lô được kiểm (học viên):  {peer}        Người kiểm (học viên):  {checker}
Ngày:  {__import__('datetime').date.today().isoformat()}                        Phiên bản guideline: Road v1.0
File được kiểm (tên + `revision` trong manifest):  {front.name}, {fish.name}
Số ảnh kiểm: 6 (+ 0 ảnh thêm, ghi riêng)   Số nhãn đã kiểm (shape + tag):  {total_labels}

Mẫu 6 ảnh: {", ".join(slot_of(im.name) for im in sample)}. Số nhãn từng ảnh: {", ".join(f"{slot_of(k)} {v}" for k, v in counts.items())}.

## Tổng hợp theo mã

| Mã | Loại lỗi | Số mục kiểm | Số lỗi | Mức |
| --- | --- | ---: | ---: | --- |
{table}

## Danh sách lỗi (mỗi lỗi một dòng)

| # | Mã | Ảnh | Nhãn (label, id) | Mức | Mô tả ngắn |
| --- | --- | --- | --- | --- | --- |
{error_rows}

## Ca mơ hồ

| Ảnh | Câu hỏi cho lead | Lời đáp (nếu có) |
| --- | --- | --- |
|  |  |  |

## Quyết định

Lỗi nặng: {critical}   Lỗi chính: {major} / {total_labels} nhãn = {rate:.1f} %   Lỗi nhẹ: {minor}   Ca chờ lead: 0
Quyết định (Release / Hold / Rework): {decision}
Lý do (theo luật của phiếu): {reason}.

Loại lỗi: bỏ sót = thiếu nhãn phải có; thừa = gán cái không phải đối tượng; sai phạm vi = hình lệch, sai chiều, dừng sai chỗ, tràn vùng. Ba loại này theo cách chia lỗi gán nhãn của ISO/IEC 5259-4 (mục 8.4.2); "sai thuộc tính" và "lỗi file" là khóa học thêm. Cách xếp mức: `docs/qc_severity_road_v1.0.md`.

Ghi chú: phiếu này điền tự động từ cảnh báo `road_check lint`; lint không có GT nên mọi dòng cần người kiểm xác nhận trước khi gửi. Cảnh báo QC1-05 "2 polyline cùng position" thường là vạch đôi, không phải vạch đứt bị tách.
"""
    out = front.parent / f"{checker}-qc1-for-{peer}.md"
    out.write_text(doc, encoding="utf-8")
    print(f"ghi {out}")
    print(f"nhãn kiểm {total_labels}, nặng {critical}, chính {major} ({rate:.1f} %), nhẹ {minor} -> {decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
