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
| `buicongdat-qc1-for-ban.md` | Phiếu QC 1 khung, chờ lô của bạn được ghép | có, 15 điểm |
| `buicongdat-report.md` | Báo cáo cá nhân | có, 5 điểm |

## Kiểm lại trước khi nộp

```powershell
$env:PYTHONPATH="src"; $env:PYTHONIOENCODING="utf-8"
python -m road_lab.road_check lint submission\buicongdat-front.zip submission\buicongdat-fisheye.zip
```

Kết quả hiện tại: 28 ảnh, 18 cảnh báo — 7 nặng (đều là QC1-02 thiếu L1/R1, ca miễn), 11 chính (10 QC1-05 vạch đôi vẽ hai polyline, 1 QC1-11 gợi ý `edge_zone` của B04), 0 nhẹ.

## Việc còn lại phải làm tay

1. **Phiếu QC 1 (15 điểm).** Phiếu đang là khung. Khi nhận `buicongdat`-style zip của bạn được ghép: mở 6 ảnh, đếm số nhãn đã kiểm, điền bảng 12 mã kèm cột "Số mục kiểm", ghi từng lỗi có mã ảnh và label id, tính tỉ lệ và ra quyết định. Đổi tên file thành `<tên bạn>-qc1-for-<tên bạn kia>.md`.
2. **Báo cáo mục 4.** Điền phản hồi phiếu QC 1 nhận được sau khi bạn kia trả phiếu.
3. **Báo cáo mục 6.** Chèn 4 ảnh chụp màn hình: tab Labels, một ảnh front đã gán đủ, một ảnh fisheye phóng to đoạn cong, một đoạn XML có `<polyline label="lane">`.
4. **Báo cáo mục 7.** Đọc lại phần tự đánh giá đã viết sẵn, sửa nếu không khớp thực tế.
5. **Phiên bản CVAT** ở đầu báo cáo: mở Help → About rồi ghi.

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
