# Phiếu QC 1 — Road v1.0

Lô được kiểm (học viên):  chuviethung        Người kiểm (học viên):  buicongdat
Ngày:  2026-11-23                        Phiên bản guideline: Road v1.0
File được kiểm (tên + `revision` trong manifest):  chuviethung-front.zip, chuviethung-fisheye.zip (chưa có manifest kèm, coi là lần nộp 1)
Số ảnh kiểm: 6 (+ 0 ảnh thêm, ghi riêng)   Số nhãn đã kiểm (shape + tag):  106

Mẫu 6 ảnh: A01, A04, A08 (front) và B01, B04, B05 (fisheye). Số nhãn từng ảnh: A01 16, A04 15, A08 47, B01 11, B04 8, B05 9. Cách chọn mẫu: xem cả ảnh sạch và ảnh có cảnh báo của `road_check lint` để không bỏ sót lỗi hệ thống.

## Tổng hợp theo mã

| Mã | Loại lỗi | Số mục kiểm | Số lỗi | Mức |
| --- | --- | ---: | ---: | --- |
| QC1-01 tag camera | sai thuộc tính / bỏ sót | 24 | 8 | nặng / nhẹ |
| QC1-02 đủ L1, R1 | bỏ sót | 18 | 0 | nặng |
| QC1-03 position | sai thuộc tính / thừa | 18 | 2 | nặng |
| QC1-04 tâm vạch, chiều, điểm dừng | sai phạm vi / bỏ sót | 18 | 0 | chính |
| QC1-05 vạch đứt, che | sai phạm vi / sai thuộc tính | 18 | 0 | chính |
| QC1-06 style, color, kind | sai thuộc tính | 18 | 0 | chính |
| QC1-07 vùng lái | sai phạm vi / bỏ sót / thừa | 34 | 0 | chính |
| QC1-08 đèn, màu | bỏ sót / sai phạm vi / sai thuộc tính | 38 | 0 | nặng / chính |
| QC1-09 facing, type, group, biển phụ | sai thuộc tính | 38 | 0 | chính |
| QC1-10 hình in, đủ biển | bỏ sót / sai phạm vi | 38 | 0 | chính |
| QC1-11 fisheye | sai phạm vi / sai thuộc tính | 20 | 0 | chính |
| QC1-12 file | lỗi file | 2 | 0 | nhẹ / nặng |

## Danh sách lỗi (mỗi lỗi một dòng)

| # | Mã | Ảnh | Nhãn (label, id) | Mức | Mô tả ngắn |
| --- | --- | --- | --- | --- | --- |
| 1 | QC1-01 | A04 | tag:camera | nặng | Không có tag camera. Ảnh thuộc camera trước nhưng thiếu hẳn tag, không suy được camera |
| 2 | QC1-01 | A04 | tag:timeofday | nhẹ | Thiếu tag timeofday |
| 3 | QC1-01 | A04 | tag:weather | nhẹ | Thiếu tag weather |
| 4 | QC1-01 | A04 | tag:source | nhẹ | Thiếu tag source |
| 5 | QC1-01 | B04 | tag:camera | nặng | Không có tag camera; file fisheye nên cần `fisheye_rear` |
| 6 | QC1-01 | B04 | tag:timeofday | nhẹ | Thiếu tag timeofday |
| 7 | QC1-01 | B04 | tag:weather | nhẹ | Thiếu tag weather |
| 8 | QC1-01 | B04 | tag:source | nhẹ | Thiếu tag source |
| 9 | QC1-03 | B05 | lane#0 | nặng | Camera `fisheye_left` nhưng `position = L2`; guideline mục 4 buộc `other` ở hai camera bên |
| 10 | QC1-03 | B05 | lane#2 | nặng | Camera `fisheye_left` nhưng `position = L1`; phải là `other` |

Hai lỗi QC1-01 còn lại nếu tính theo ảnh: A04 và B04 đều mất cả bốn tag, tức 8 dòng tag thiếu cho 2 ảnh. Trong 8 dòng đó có 2 dòng mức nặng (camera) và 6 dòng mức nhẹ (timeofday, weather, source).

## Ca mơ hồ

| Ảnh | Câu hỏi cho lead | Lời đáp (nếu có) |
| --- | --- | --- |
| A01 | `lane#3` và `lane#11` cùng `position = L2`: đây là vạch đôi (hai nét song song, hợp lệ) hay vạch đứt bị tách thành hai polyline (lỗi QC1-05)? | |
| A04 | `lane#6` và `lane#7` cùng `position = L1`, cách nhau vài chục pixel: vạch đôi hay một vạch đứt bị tách? | |

Hai ca này không đổi kết luận vì đã có lỗi nặng, nên ghi lại để lead xác nhận khi chấm.

## Quyết định

Lỗi nặng: 4   Lỗi chính: 0 / 106 nhãn = 0.0 %   Lỗi nhẹ: 6   Ca chờ lead: 2
Quyết định (Release / Hold / Rework): Rework
Lý do (theo luật của phiếu): có 4 lỗi nặng gồm thiếu tag camera ở A04 và B04, sai `position` ở B05; luật "có ít nhất một lỗi nặng thì Rework".

Loại lỗi: bỏ sót = thiếu nhãn phải có; thừa = gán cái không phải đối tượng; sai phạm vi = hình lệch, sai chiều, dừng sai chỗ, tràn vùng. Ba loại này theo cách chia lỗi gán nhãn của ISO/IEC 5259-4 (mục 8.4.2); "sai thuộc tính" và "lỗi file" là khóa học thêm. Cách xếp mức: `docs/qc_severity_road_v1.0.md`.
