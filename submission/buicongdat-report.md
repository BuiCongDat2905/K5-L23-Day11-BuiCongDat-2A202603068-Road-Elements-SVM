# Báo cáo cá nhân — Ngày 11

Họ tên: Bùi Công Đạt      Mã học viên: 2A202603068
Phiên bản CVAT (Help → About): <điền khi mở CVAT>
Guideline: Road v1.0    Lần nộp (`revision` trong manifest): 1
Thời điểm export (ngày giờ trên CVAT): 2026-11-22 21:39:46    Số lần nộp lại sau Rework: 0

## 1. Kiểm project

| Mục | Đúng như guideline Road v1.0? | Ghi chú |
| --- | --- | --- |
| 6 label, đúng kiểu | Đúng | `lane`, `road_curb` là polyline; `crosswalk`, `drivable` là polygon; `traffic_light`, `traffic_sign` là rectangle |
| Thuộc tính và giá trị | Đúng | Dán tab Project → Labels → Raw bằng JSON sinh từ `python -m road_lab.taxonomy`, đối chiếu với `configs/road_v1_labels.json` |
| 4 tag ảnh | Đúng | Bốn label Tag: `camera`, `timeofday`, `weather`, `source`; mỗi label có một thuộc tính select tên `value` |

Cách kết thúc polyline trên bản CVAT này: bấm phím **N** sau điểm cuối.
Cách đặt tag ảnh trên bản CVAT này: công cụ **Tag** ở thanh bên trái, đặt `camera` trước rồi `timeofday`, `weather`, `source`; mở **Details** trong bảng Objects để kiểm giá trị.

## 2. Số lượng đã gán

| Task | Ảnh | lane | road_curb | crosswalk | drivable | traffic_light | traffic_sign |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| front | 12 | 40 | 17 | 10 | 29 | 42 | 40 |
| front-extra (đã làm 4 / 4) | 4 | 13 | 6 | 4 | 9 | 7 | 16 |
| fisheye | 8 | 7 | 11 | 10 | 12 | 9 | 7 |
| fisheye-extra (đã làm 4 / 4) | 4 | 0 | 5 | 5 | 7 | 0 | 0 |

Tổng: 28 ảnh, 297 shape và 112 tag. Số ảnh đủ bốn tag: 28/28 (manifest ghi `images_all_tags` 16 và 12).

## 3. Bảng ca khó

| Ảnh | Nhãn | Phân vân giữa | Đã chọn | Lý do |
| --- | --- | --- | --- | --- |
| A05 | lane | vẽ bổ sung L1/R1 / để trống | Để trống | Ảnh chỉ có lề và mép đường, không thấy vệt sơn ở hai bên làn đang đi; vẽ thêm sẽ là nhãn thừa. Lint báo QC1-02, đây là ca miễn theo guideline mục 5 và delivery mục 2 |
| A06 | lane | vẽ R1 / để trống | Để trống | Làn phải sát hàng xe đỗ, không có vạch sơn nhìn thấy được |
| A07 | lane | vẽ L1 / để trống | Để trống | Bên trái là dải phân cách, không có vạch kẻ |
| A09 | lane | vẽ R1 / để trống | Để trống | Mép phải là lề đất, không sơn |
| A14 | lane | vẽ R1 / để trống | Để trống | Ảnh thêm; bên phải là vỉa hè, không có vạch |
| A15 | lane | vẽ R1 / để trống | Để trống | Ảnh thêm; bên phải bị che gần hết, không đủ căn cứ vẽ |
| A01 | lane L2 | một polyline / hai polyline | Hai polyline | Ảnh có vạch đôi: mỗi nét song song là một vạch riêng, cùng `position = L2`. Lint báo QC1-05 "2 polyline cùng position", nhưng đây không phải vạch đứt bị tách |
| A04, A06, A09, A11, A12, A14, A15 | lane | một polyline / hai polyline | Hai polyline | Cùng lý do A01: vạch đôi hoặc hai vạch khác loại nằm cùng phía. Cần coach xác nhận nếu chấm là QC1-05 |
| B05, B07, B08 | lane | L1/R1 / other | `position = other` | Camera fisheye bên trái và bên phải: guideline mục 4 buộc dùng `other`, không dùng L1/R1/L2/R2 |
| B04 | traffic_light | bật / tắt `edge_zone` | Tắt | Tâm box nằm trong 80 % bán kính; lint chỉ gợi ý tự kiểm, không phải lỗi chấm |

## 4. Phiếu QC 1 nhận được

Bạn kiểm lô của tôi:  <điền tên bạn được ghép>    Quyết định nhận được:  <Release / Hold / Rework>

| Mã lỗi | Số lỗi | Đồng ý? | Đã sửa? |
| --- | ---: | --- | --- |
|  |  |  |  |

Nếu chưa nhận được phiếu: ghi rõ "chưa nhận phiếu" và để trống bảng. Mục này 2 điểm, cần phản hồi thật khi phiếu về.

## 5. Kiểm file export

| File | Mở lại được? | Số shape ảnh 1 (job / file) | Số shape ảnh 2 (job / file) | Tag camera có trong XML? |
| --- | --- | --- | --- | --- |
| `buicongdat-front.zip` | Có, `road_check lint` đọc được 16 ảnh | A01: 12 shape + 4 tag | A02: 8 shape + 4 tag | Có, `<tag label="camera">` với `<attribute name="value">front</attribute>` |
| `buicongdat-fisheye.zip` | Có, `road_check lint` đọc được 12 ảnh | B01: 5 shape + 4 tag | B02: 6 shape + 4 tag | Có, `value = fisheye_front` |

Kiểm tự động: `contains_images` là `false` ở cả hai file (manifest). Số ảnh 16 và 12, khớp số ảnh đã gán. Không có ảnh nào chưa gán (`images_unlabelled` 0).

## 6. Ảnh chụp màn hình

1. Tab Labels của project.
2. Một ảnh camera trước đã gán đủ (làn, vùng lái, đèn/biển).
3. Một ảnh fisheye đã gán, phóng to đoạn polyline cong.
4. Một đoạn XML có `<polyline label="lane">`.

<chèn ảnh chụp màn hình vào đây trước khi nộp; mục này có 2 điểm trong rubric>

## 7. Tự đánh giá

Lỗi bạn mắc nhiều nhất hôm nay (theo mã QC1-xx), và cách tránh ở Ngày 20: hai lỗi lặp lại nhiều nhất là QC1-02 (thiếu L1/R1 ở ảnh không có vạch sơn) và QC1-05 (vạch đôi vẽ thành hai polyline nên lint hiểu là vạch đứt bị tách). Cách tránh: trước khi vẽ, xác định làn đang đi bằng vạch sát xe chứ không đếm tổng số làn; với vạch đôi thì ghi rõ trong bảng ca khó rằng hai nét là hai vạch, và dùng `kind = double` thay vì vẽ hai polyline cùng `position`.

Nhãn của bạn đi vào model ở đâu? Chọn một lỗi đã sửa và nói nó làm model học sai thế nào: lỗi QC1-03 ở B05/B07/B08 là ví dụ rõ nhất. Camera hai bên phải luôn là `position = other`; nếu để L1/R1, model row-anchor học nhầm rằng vạch sát thân xe ở camera bên là làn đang đi của chính xe. Khi chạy LKA, model sẽ bám sang vạch của làn bên cạnh, tức lệch sang trái hoặc phải đúng một làn.

## 8. (Tùy chọn, buffer) Từ polyline đến đích row-anchor

| y | 720 | 680 | 640 | 600 | 560 |
| --- | ---: | ---: | ---: | ---: | ---: |
| x của chúng tôi |  |  |  |  |  |
| x của bạn kia |  |  |  |  |  |

Trả lời 3 câu:

1. Năm số x đó chính là đích mà một model row-anchor học cho vạch này. Nếu bạn dừng polyline sớm 40 px, hàng nào đổi thành "không có làn"?
2. So với bạn được kiểm (cùng ảnh): ở hàng 720 và hàng 560, hai bạn lệch nhau bao nhiêu pixel? Lệch ở hàng nào ảnh hưởng LKA nhiều hơn (slide 25)?
3. Nếu polyline vẽ từ xa về gần (ngược quy tắc 2), cách tính trên có đổi không? Script nào sẽ gặp khó?

<điền nếu làm hoạt động buffer; mục này không tính điểm>
