# Bộ file nộp bài — Ngày 11 · Road Elements & SVM

Sinh từ bản export `job_59_annotations_2026_11_22_21_39_46_cvat for images 1.1.zip` (28 ảnh, 112 tag), có sửa hai loại lỗi cơ học trước khi đóng gói:

1. `position = other` cho mọi `lane` ở ba ảnh camera hai bên B05, B07, B08 (QC1-03).
2. Xoá mọi cặp điểm lặp liền nhau trong `points=` của polyline và polygon (QC1-12, lỗi click hai lần một chỗ).

Không thêm vạch nào. Các cảnh báo QC1-02 (thiếu L1/R1) giữ nguyên và được khai báo là ca miễn trong báo cáo mục 3.

## File trong thư mục này

| File | Vai trò | Chấm điểm? |
| --- | --- | --- |
| `buicongdat-front.zip` | CVAT for images 1.1, 16 ảnh A01–A16, không kèm ảnh | có |
| `buicongdat-fisheye.zip` | CVAT for images 1.1, 12 ảnh B01–B12, không kèm ảnh | có |
| `buicongdat-manifest.json` | Manifest bàn giao, `revision` 1, `contains_images: false` | không |
| `buicongdat-qc1-for-chuviethung.md` | Phiếu QC 1 cho lô của chuviethung, đã kiểm 6 ảnh, quyết định Rework | có, 15 điểm |
| `buicongdat-report.md` | Báo cáo cá nhân, đã điền đủ 8 mục | có, 5 điểm |
| `figures/` | Bốn ảnh chụp CVAT thật (`cvat1`–`cvat4`) + bốn hình phụ lục dựng từ XML (`fig1`–`fig4`) | — |

## Kiểm lại trước khi nộp

```powershell
$env:PYTHONPATH="src"; $env:PYTHONIOENCODING="utf-8"
python -m road_lab.road_check lint submission\buicongdat-front.zip submission\buicongdat-fisheye.zip
```

Kết quả hiện tại: 28 ảnh, 18 cảnh báo — 7 nặng (đều là QC1-02 thiếu L1/R1, ca miễn), 11 chính (10 QC1-05 vạch đôi vẽ hai polyline, 1 QC1-11 gợi ý `edge_zone` của B04), 0 nhẹ.

## Việc còn lại

Không còn mục nào bắt buộc phải điền tay. Báo cáo đã đủ 8 mục:

- Mục 4 ghi rõ là **tự kiểm lô của mình** (chuviethung chưa gửi phiếu), kèm bảng mã lỗi, cột đồng ý và đã sửa.
- Mục 8 có đủ hai cột số row-anchor của A01 R1, lấy từ `road_lab.rowanchor` trên bài mình và bài chuviethung; hai bên lệch 0.0 px ở cả bốn hàng có số.
- Mục 6 là bốn ảnh chụp CVAT thật.

Nếu chuviethung gửi phiếu sau, chỉ cần sửa cột "Đồng ý?" ở mục 4 theo nhận xét của bạn ấy.


Phiếu QC 1 đã xong: [buicongdat-qc1-for-chuviethung.md](buicongdat-qc1-for-chuviethung.md), kiểm 6 ảnh A01, A04, A08, B01, B04, B05 trên 106 nhãn. Kết quả Rework vì 4 lỗi nặng: A04 và B04 thiếu tag `camera`, B05 có hai lane mang `position` L1/L2 trong khi camera `fisheye_left` buộc `other`. Còn hai ca mơ hồ ghi ở mục riêng (vạch đôi hay vạch đứt bị tách ở A01 và A04).

Sinh lại phiếu bằng script khi cần đổi mẫu ảnh:

```powershell
$env:PYTHONPATH="src"; $env:PYTHONIOENCODING="utf-8"
python tools\make_qc1.py chuviethung-front.zip chuviethung-fisheye.zip buicongdat chuviethung
```

Chụp lại ảnh nếu cần: `$env:CVAT_USER="..." ; $env:CVAT_PASS="..." ; python tools/cvat_shots.py` (thêm `CVAT_XML` trỏ tới file zip export để chụp mục 6.4).

Các mục khác đã điền xong: phiên bản CVAT 2.82.0, bảng số lượng nhãn, bảng ca khó, bảng kiểm file export, tự đánh giá.


## Nộp bằng link git

`.gitignore` đã được thêm `!submission/*.zip` để zip nộp bài không bị bỏ qua. Kiểm và đẩy lên:

```powershell
git status --short
git add submission .gitignore tools
git commit -m "Day 11: bo file nop bai road elements"
git push
```

Nếu repo chưa có remote hoặc remote riêng tư, dùng đúng link coach yêu cầu. Không đưa thư mục `data/` lên git: `.gitignore` đã bỏ `data/` vì ảnh thuộc bộ dữ liệu có giấy phép riêng.

## Dựng lại file từ bản export gốc

```powershell
$env:PYTHONPATH="src"
python tools\build_submission.py "job_59_annotations_2026_11_22_21_39_46_cvat for images 1.1.zip" submission buicongdat
python -m road_lab.road_check lint submission\buicongdat-front.zip submission\buicongdat-fisheye.zip --manifest submission\buicongdat-manifest.json --name buicongdat --revision 1
```

Script giữ nguyên header `<meta>`, thứ tự thuộc tính và khoảng trắng gốc; chỉ sửa `position` ở ba ảnh camera hai bên, xoá điểm lặp, đánh số lại `id` 0..n-1 và chỉnh `size`, `stop_frame`, `segment stop` cho khớp số ảnh từng phần.
