# Phiếu QC 1 — Road v1.0

Lô được kiểm (học viên):  <tên bạn được ghép>        Người kiểm (học viên):  buicongdat
Ngày:  <ngày kiểm>                        Phiên bản guideline: Road v1.0
File được kiểm (tên + `revision` trong manifest):  <tên bạn>-front.zip, <tên bạn>-fisheye.zip, revision <n>
Số ảnh kiểm: 6 (+ __ ảnh thêm, ghi riêng)   Số nhãn đã kiểm (shape + tag):  <đếm thật>

Cách đếm số nhãn đã kiểm: mỗi shape (polyline, polygon, rectangle) là 1 nhãn, mỗi tag ảnh là 1 nhãn. Đếm trên 6 ảnh đã mở, không đếm cả lô.

## Tổng hợp theo mã

| Mã | Loại lỗi | Số mục kiểm | Số lỗi | Mức |
| --- | --- | ---: | ---: | --- |
| QC1-01 tag camera | sai thuộc tính / bỏ sót |  |  | nặng |
| QC1-02 đủ L1, R1 | bỏ sót |  |  | nặng |
| QC1-03 position | sai thuộc tính / thừa |  |  | nặng |
| QC1-04 tâm vạch, chiều, điểm dừng | sai phạm vi / bỏ sót |  |  | chính |
| QC1-05 vạch đứt, che | sai phạm vi / sai thuộc tính |  |  | chính |
| QC1-06 style, color, kind | sai thuộc tính |  |  | chính |
| QC1-07 vùng lái | sai phạm vi / bỏ sót / thừa |  |  | chính |
| QC1-08 đèn, màu | bỏ sót / sai phạm vi / sai thuộc tính |  |  | nặng / chính |
| QC1-09 facing, type, group, biển phụ | sai thuộc tính |  |  | chính |
| QC1-10 hình in, đủ biển | bỏ sót / sai phạm vi |  |  | chính |
| QC1-11 fisheye | sai phạm vi / sai thuộc tính |  |  | chính |
| QC1-12 file | lỗi file |  |  | nhẹ / nặng |

Cột "Số mục kiểm" không được để trống: đó là số đối tượng đã xem cho mã đó, tính điểm riêng trong rubric.

## Danh sách lỗi (mỗi lỗi một dòng)

| # | Mã | Ảnh | Nhãn (label, id) | Mức | Mô tả ngắn |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Ghi đủ mã ảnh, label và id để coach tìm lại được: coach kiểm lại 3 lỗi bạn ghi và 1 ảnh bạn ghi "không lỗi".

## Ca mơ hồ

| Ảnh | Câu hỏi cho lead | Lời đáp (nếu có) |
| --- | --- | --- |
|  |  |  |

## Quyết định

Lỗi nặng: __   Lỗi chính: __ / __ nhãn = __ %   Lỗi nhẹ: __   Ca chờ lead: __
Quyết định (Release / Hold / Rework):
Lý do (theo luật của phiếu):

Luật quyết định: có ít nhất một lỗi nặng → Rework. Không có lỗi nặng và lỗi chính trên 5 % số nhãn đã kiểm → Rework. Còn câu hỏi chưa có lời đáp ảnh hưởng tới kết luận → Hold. Còn lại → Release. Mẫu số là số nhãn đã kiểm (shape cộng tag), không phải số ảnh.

Loại lỗi: bỏ sót = thiếu nhãn phải có; thừa = gán cái không phải đối tượng; sai phạm vi = hình lệch, sai chiều, dừng sai chỗ, tràn vùng. Ba loại này theo cách chia lỗi gán nhãn của ISO/IEC 5259-4 (mục 8.4.2); "sai thuộc tính" và "lỗi file" là khóa học thêm. Cách xếp mức: `docs/qc_severity_road_v1.0.md`.
