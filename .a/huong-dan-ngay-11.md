# Hướng dẫn từng bước · Ngày 11 · Road Elements & SVM

Tài liệu này gom toàn bộ việc phải làm trong buổi lab thành một trình tự chạy được. Nguồn gốc từng bước ghi trong ngoặc: `[README]`, `[GL]` = `docs/guideline_road_v1.0.md`, `[HINH]` = `docs/huong_dan_cvat_bang_hinh.md`, `[DELIV]` = `docs/delivery_road_v1.0.md`, `[QC]` = `docs/qc_severity_road_v1.0.md`, `[RUB]` = `RUBRIC.md`, `[CP]` = `CHECKPOINTS.md`, `[SUB]` = `SUBMISSION.md`, `[AG]` = `lab/AGENTS.md`.

Quy tắc ưu tiên khi hai tài liệu khác nhau: về **quy tắc gán nhãn**, guideline Road v1.0 thắng; về **ngưỡng và CLI của script**, `lab/AGENTS.md` thắng `[AG]`.

## 0. Kết quả cuối cùng: 5 file

| File | Nội dung | Có chấm điểm? |
| --- | --- | --- |
| `<tên>-front.zip` | CVAT for images 1.1, không kèm ảnh; task front A01–A12 + front-extra nếu làm | có |
| `<tên>-fisheye.zip` | CVAT for images 1.1, không kèm ảnh; task fisheye B01–B08 + fisheye-extra nếu làm | có |
| `<tên>-manifest.json` | Do `road_check lint --manifest` sinh ra | không |
| `<tên>-qc1-for-<tên bạn>.md` | Phiếu QC 1 theo `templates/qc1_form.md` | có (15 điểm) |
| `<tên>-report.md` | Báo cáo theo `templates/report.md` | có (5 điểm) |

`<tên>` viết liền, không dấu, không khoảng trắng. Script chấm của coach tìm đúng hai tên `<tên>-front.zip` và `<tên>-fisheye.zip` nên không thêm hậu tố nào `[DELIV]`. Hạn nộp 16:35 `[SUB]`.

## 1. M0 — 13:00, kiểm môi trường

### 1.1 Repo và Python

Mở terminal tại gốc repo. Kiểm Python từ 3.11 trở lên; repo chỉ dùng thư viện chuẩn `[AG]`:

```bash
python3 --version
```

Trên Windows dùng `python` thay `python3` nếu lệnh `python3` không tồn tại.

### 1.2 Bộ ảnh

`README` yêu cầu `data/` có đúng 28 ảnh A01…A16, B01…B12 `[README]`. Trong bản repo hiện tại thư mục này rỗng hoặc chưa có: ảnh nằm trên CVAT của lớp, repo chỉ chứa script và tài liệu `[AG]`. Nếu thư mục `data/` chưa có thì hỏi trợ giảng ngay, đừng tự tải ảnh từ nguồn ngoài.

```bash
ls data/ | wc -l
```

### 1.3 Self-test checker

```bash
PYTHONPATH=src python3 -m road_lab.road_check selftest
```

Phải in `SELFTEST PASS` `[README]`. Lệnh này chạy trên GT tổng hợp 20 ảnh, không cần GT thật `[AG]`.

Nếu dùng PowerShell trên Windows, biến môi trường phải đặt riêng:

```powershell
$env:PYTHONPATH="src"
python -m road_lab.road_check selftest
```

Cách này áp dụng cho mọi lệnh `PYTHONPATH=src ...` trong tài liệu.

### 1.4 Đăng nhập CVAT và kiểm quyền

Đăng nhập CVAT của lớp bằng tài khoản được cấp `[HINH]`. **Không** đưa ảnh lên app.cvat.ai `[README]`, và không đưa GT, ảnh lên kênh chung của lớp `[AG]`.

Mở `Projects`, thấy project `d11-road-<tên>`. Nếu chưa có, báo coach.

## 2. Task 0 — 13:15, kiểm project và taxonomy

### 2.1 Sáu label vẽ và bốn label tag

Phải có đúng như bảng sau `[AG]` mục 2, `[GL]` mục 1:

| Label | Kiểu CVAT | Thuộc tính |
| --- | --- | --- |
| `lane` | polyline | `position` L1/R1/L2/R2/other · `style` solid/dashed · `color` white/yellow/other · `kind` single/double |
| `road_curb` | polyline | không có |
| `crosswalk` | polygon | không có |
| `drivable` | polygon | `area_type` direct/alternative |
| `traffic_light` | rectangle | `color` red/yellow/green/off/unknown · `type` vehicle/pedestrian/beacon · `facing` front/side/back · `edge_zone` checkbox |
| `traffic_sign` | rectangle | `group` prohibitory/mandatory/warning/information/supplementary/other · `facing` front/side/back · `edge_zone` checkbox |
| `camera` (tag) | tag | `value` front/fisheye_front/fisheye_rear/fisheye_left/fisheye_right |
| `timeofday` (tag) | tag | `value` day/dusk/night |
| `weather` (tag) | tag | `value` clear/overcast/rain/fog/other |
| `source` (tag) | tag | `value` real/simulated |

Bốn task phải có: `front`, `front-extra`, `fisheye`, `fisheye-extra` `[CP]`.

### 2.2 Cách kiểm bằng script

In JSON taxonomy rồi so với tab Labels → Raw của project `[README]`:

```bash
PYTHONPATH=src python3 -m road_lab.taxonomy
```

JSON chuẩn cũng nằm sẵn ở `configs/road_v1_labels.json`. Nếu project thiếu hoặc sai, dán JSON đó vào Project → Labels → Raw. `src/road_lab/taxonomy.py` là nguồn sự thật duy nhất; test kiểm hai bên luôn khớp `[AG]`.

### 2.3 Điểm dễ sai nhất ở bước này

Mỗi tag ảnh là **một** label kiểu Tag có **một** thuộc tính select tên `value`. Ví dụ label `camera`, `value = fisheye_left`. Không dùng phương án "mỗi giá trị một label riêng" `[AG]`. Lý do: export CVAT for images 1.1 ghi `<tag label="camera"><attribute name="value">…</attribute></tag>`, nên một ảnh không thể mang hai giá trị camera và checker chỉ đọc được một cách.

## 3. Sáu bẫy mặc định phải nhớ trước khi gán ảnh đầu

Cả sáu lỗi này đều do CVAT tự điền sẵn, không phải do bạn chọn sai `[HINH]`, `[CP]`:

1. Tag `weather` mới tạo tự mang `clear`. Lint không bắt được nếu giá trị đó vẫn hợp lệ, nên phải tự mở Details kiểm từng tag.
2. Tag `timeofday` tự mang giá trị đầu danh sách là `day`.
3. Tag `source` phải chọn đúng nguồn; ảnh lớp là ảnh thật nên `source = real` `[AG]`.
4. Polyline `lane` mới vẽ tự mang `L1 / solid / white / single`. Luôn mở Details sửa.
5. Polygon `drivable` mới vẽ tự mang `area_type = direct`. Polygon làn bên cạnh phải đổi thành `alternative`.
6. Box `traffic_light`, `traffic_sign` mới vẽ mang giá trị đầu của `color`, `facing`, `type`, `group`. Phải sửa hết.

Hệ quả nếu bỏ qua: sáu ảnh đầu đúng, mười bốn ảnh sau sai thuộc tính hàng loạt, mất điểm ở dòng "Thuộc tính làn" (10 điểm) và "Đèn và biển" (15 điểm) `[RUB]`.

## 4. Quy trình chuẩn cho một ảnh

Đây là thứ tự bắt buộc, làm sai thứ tự sẽ phải quay lại `[GL]` mục 2.

1. **Bốn tag ảnh**, `camera` trước tiên, rồi `timeofday`, `weather`, `source`. Mở Details kiểm từng giá trị.
2. **Làn**: `R1` và `L1` trước, rồi `L2` và `R2` nếu thấy. Mép đường không sơn thì vẽ `road_curb`.
3. **Thuộc tính từng vạch**, bật `occluded` ở chỗ nối qua vật che.
4. **`drivable`**: `direct` rồi `alternative` nếu có. **`crosswalk`** nếu có.
5. **Hộp đèn và biển**, đủ thuộc tính.
6. **Ctrl+S**.

Mỗi ảnh chỉ gán nhóm label mà bảng kế hoạch ảnh yêu cầu; không gán loại không được yêu cầu cho ảnh đó `[GL]`.

Cách kết thúc polyline trên bản CVAT này: bấm phím **N** sau điểm cuối `[HINH]`. Ghi câu trả lời này vào mục 1 của báo cáo.

## 5. Vẽ lane: mười quy tắc không được sai

`[GL]` mục 3, mỗi lỗi dưới đây ánh xạ sang một mã QC 1.

1. Polyline đặt trên **tâm vệt sơn**, không đặt ở mép vạch.
2. Vẽ **từ gần xe ra xa**. Điểm đầu sát xe là điểm quan trọng nhất, phải thật chính xác.
3. Vạch đứt là **một** polyline, không phải mỗi vệt sáng một đường. Tách ra là lỗi QC1-05.
4. Đoạn bị che ngắn (xe, người): **nối liền** qua chỗ che và bật `occluded`. Không dừng trước vật che. Đứng trước vật che là lỗi QC1-05.
5. Dừng ở điểm xa nhất **còn thấy** vạch, không kéo tới chân trời. Dừng sớm hoặc kéo quá là lỗi QC1-04.
6. Lệch khỏi tâm vạch **tối đa 5 px**. Thêm điểm ở đoạn cong. Ngưỡng 5 px là ngưỡng chấm thật `[AG]` mục 4.
7. `position` tính theo làn đang đi: `L1` và `R1` là hai vạch sát xe, `L2` và `R2` là vạch kế tiếp bên ngoài.
8. Vạch vàng đôi: chọn `kind = double` khi ảnh có hai nét song song. Vạch đôi một liền một đứt (QCVN 1.4) không có giá trị style riêng: ghi vào bảng ca khó và nêu nửa nào bạn chọn.
9. Vạch trắng mép ngoài phần đường xe chạy (QCVN 3.1) vẫn là `lane`, không phải `road_curb` `[GL]` mục 6.
10. Ảnh không có vạch sơn ở một bên: **không vẽ** L1 hay R1 cho bên đó. Lint sẽ báo QC1-02; xem mục 8.3 dưới.

## 6. Task 1 — 13:50, gán A01–A12

### 6.1 Mở job và ảnh đầu tiên

Vào **Projects** → `d11-road-<tên>` → **Open** ở task `front` `[HINH]`. Job mở ra trống.

### 6.2 Thao tác trên ảnh A01

Làm đúng sáu bước ở mục 4. Trình tự thao tác cụ thể `[HINH]`:

1. Công cụ **Tag** ở thanh bên trái. Đặt `camera = front` trước, sau đó `timeofday`, `weather`, `source`.
2. Công cụ **Polyline** → label `lane` → bấm **Shape**.
3. Click lần lượt các điểm trên tâm vệt sơn, bắt đầu từ đáy ảnh (phía gần xe) đi ra xa. Bấm **N** để kết thúc.
4. Bảng Objects → **Details** của lane → sửa `position`, `style`, `color`, `kind` cho khớp ảnh.
5. Lặp cho các vạch còn lại.
6. Công cụ **Polygon** → label `drivable` → vẽ `direct` (cắt ở mép capô nếu capô lọt vào ảnh), rồi polygon thứ hai đổi `area_type` thành `alternative`.
7. Box đèn và biển nếu ảnh có.

### 6.3 A01 phải qua checkpoint của coach

Coach kiểm ảnh đầu tiên của mỗi học viên tại chỗ `[CP]`. Bốn điểm được kiểm:

- tag `camera = front`, đặt trước tiên;
- polyline vẽ từ gần ra xa;
- vạch đứt là một polyline;
- R1/L1 nằm trên tâm vạch;
- thuộc tính đã sửa (không còn giá trị mặc định).

Gặp lỗi ở đây thì sửa ngay, tuyệt đối không để lặp ra 11 ảnh sau.

### 6.4 Các ảnh A02–A12

Lặp quy trình mục 4. Ba mốc coach kiểm giữa giờ khoảng 14:20 `[CP]`:

- A03 phải có `occluded`;
- A04 phải có vạch vàng đôi (`kind = double`) và `drivable` chia `direct` / `alternative`;
- A07–A08 box đèn phải sát vỏ và `color` là màu **đang sáng** trong ảnh.

Trọng tâm từng ảnh front do coach công bố theo bảng kế hoạch ảnh của deck thực hành, không nằm trong repo. Bảng `manifests/manifest_front.csv` trong repo hiện chỉ có dòng tiêu đề, nên không dùng được để tra trọng tâm; hỏi coach nếu chưa có.

### 6.5 Lỗi hay gặp nhất ở Set A

| Hiện tượng | Nguyên nhân | Cách tránh |
| --- | --- | --- |
| Nhầm L1 với L2 | Tính `position` theo tổng số làn nhìn thấy | Tính theo làn **đang đi**: hai vạch sát xe là L1, R1 |
| Vạch đứt bị tách thành 4–5 đường | Mỗi vệt sáng vẽ một polyline | Vẽ một polyline, nối qua khe hở |
| Polyline dừng trước xe đỗ | Ngại đoạn bị che | Nối liền, bật `occluded` |
| `drivable` tràn lề hoặc gồm dải đỗ | Chép theo mép ảnh | Chỉ vùng xe đi được; dải đỗ sát lề không thuộc `direct` |
| Box đèn gồm cả cần treo | Vẽ theo cả cụm | Hộp sát vỏ đèn `[GL]` |

## 7. Task 2 — 15:05, gán B01–B08 (fisheye)

### 7.1 Mở task fisheye

Cùng cách với task `front`, mở task `fisheye`.

### 7.2 Bốn quy tắc riêng của fisheye

`[GL]` mục 4:

1. Polyline đi theo **cung cong** trên ảnh; vạch thẳng ngoài đời thành cong trên ảnh. Không nối hai điểm đầu cuối, không nắn ảnh. Lệch tối đa 5 px, đặt điểm dày ở vòng ngoài nơi cung cong nhất.
2. Thân xe mình và vùng tối viền ảnh: **không gán**, và không tính vào vùng lái.
3. `position` L1/R1/L2/R2 **chỉ** dùng ở `fisheye_front` và `fisheye_rear`. Ở `fisheye_left` và `fisheye_right` luôn dùng `position = other`.
4. Đèn, biển có tâm hộp nằm ngoài 80 % bán kính vòng ảnh: bật `edge_zone`. Hộp vẫn thẳng, sát pixel, ôm cả phần nền ở các góc.

Thêm: vạch ngựa vạn gán `crosswalk` (polygon); vạch ô đỗ **không** gán `lane`.

### 7.3 Trọng tâm từng ảnh B

Lấy từ `manifests/manifest_fisheye.csv` (cột `focus`, trạng thái "ứng viên — coach xem lại và chốt"):

| Slot | File | Camera | Trọng tâm |
| --- | --- | --- | --- |
| B01 | `02688_FV.png` | `fisheye_front` | lane theo cung (R1/L1 nếu thấy) hoặc crosswalk |
| B02 | `03177_FV.png` | `fisheye_front` | traffic_light / traffic_sign sát mép + `edge_zone` |
| B03 | `04267_RV.png` | `fisheye_rear` | lane theo cung (đường nhiều làn) + thuộc tính |
| B04 | `05535_RV.png` | `fisheye_rear` | drivable đúng ở mép thân xe + crosswalk |
| B05 | `05780_MVL.png` | `fisheye_left` | crosswalk + road_curb |
| B06 | `04068_MVL.png` | `fisheye_left` | drivable + lane `position = other` |
| B07 | `01216_MVR.png` | `fisheye_right` | crosswalk + road_curb |
| B08 | `05783_MVR.png` | `fisheye_right` | drivable + lane `position = other` |

Ảnh thêm (không bắt buộc, +0,5 điểm mỗi ảnh đạt): B09 `02686_FV` đèn/biển sát mép + lane; B10 `01153_MVL` crosswalk; B11 `07282_RV` chỉ lane vạch dọc, **bỏ vạch ô đỗ** (bẫy QC1-03); B12 `05885_MVR` drivable + crosswalk.

### 7.4 Checkpoint fisheye

Coach kiểm B01 và B05–B08 `[CP]`:

- B01: polyline đi theo cung, nhiều điểm ở vòng ngoài; tag camera đúng (FV → `fisheye_front`, RV → `fisheye_rear`, MVL → `fisheye_left`, MVR → `fisheye_right`); thân xe mình không bị gán.
- B05–B08: mọi lane có `position = other`; vạch ngựa vạn gán `crosswalk` (polygon), không gán `lane`.

Dành 5 phút cuối của Task 2 để self-QC.

## 8. Self-QC trước khi export

### 8.1 Kiểm bằng mắt

`[GL]` mục 5:

- [ ] Mọi ảnh đủ bốn tag, `camera` đúng.
- [ ] Mọi polyline đi từ gần ra xa, vạch đứt là một đường, chỗ che có `occluded`.
- [ ] Không còn L1 hoặc R1 bị thiếu khi thấy được; không nhầm L1 với L2.
- [ ] Hộp đèn, biển sát và đủ thuộc tính.
- [ ] Ảnh fisheye: theo cung, không gán thân xe.

### 8.2 Kiểm bằng lint

Sau khi export (mục 10), chạy `lint`. Trước khi export chưa có file để lint.

### 8.3 Xử lý cảnh báo QC1-02 "chưa có L1/R1"

Nếu một bên làn thật sự không có vạch sơn (chỉ có lề, hàng xe đỗ): **không vẽ thêm vạch**. Quy trình đúng `[HINH]`, `[SUB]`:

1. Gọi coach nhìn ảnh xác nhận.
2. Ghi mã ảnh và lý do vào Phiếu QC 1.
3. Đây là ngoại lệ **duy nhất** được miễn lỗi nặng `[DELIV]`. Manifest vẫn đếm cảnh báo này trong `lint.nặng`, nên đừng cố làm nó biến mất.

## 9. Task 3 — 15:40, Phiếu QC 1 cho bạn khác

### 9.1 Trước khi bắt đầu

Đổi lô với bạn được ghép. Nhận từ bạn: hai file zip (hoặc bản export) và `revision` trong manifest của bạn đó.

### 9.2 Nguyên tắc kiểm

Kiểm **theo mẫu**: 6 ảnh, không kiểm hết `[QC]` mục 5. Mỗi lỗi xếp ba mức theo đúng một câu hỏi: **nếu nhãn sai này đi vào dữ liệu huấn luyện, hậu quả là gì?** `[QC]` mục 1.

| Mức | Nghĩa | Ví dụ |
| --- | --- | --- |
| nặng | Sai ý nghĩa an toàn của cảnh, hoặc làm file không dùng được | Tag camera sai; thiếu L1/R1 khi thấy được; nhầm làn mình với làn bên; đèn đỏ gán xanh trên đèn hướng về xe; file không mở được |
| chính | Đúng đối tượng nhưng sai hình hoặc thuộc tính | Lệch tâm vạch quá 5 px, ngược chiều, dừng sớm; vạch đứt bị tách; sai style/color; vùng lái tràn lề; box không sát; sai facing hoặc group; thiếu biển; fisheye không theo cung |
| nhẹ | Không đổi ý nghĩa, sửa nhanh | Thiếu tag timeofday/weather/source; ảnh trùng; thuộc tính thiếu giá trị |

Phân vân giữa hai mức: chọn **mức cao hơn**, ghi vào mục "Ca mơ hồ" để lead quyết `[QC]`.

### 9.3 Điền phiếu

Mở `templates/qc1_form.md`, lưu thành `<tên người kiểm>-qc1-for-<tên người được kiểm>.md` (quy ước trong `[SUB]`). Điền đủ `[CP]`, `[RUB]`:

1. Phần đầu: lô được kiểm, người kiểm, ngày, phiên bản guideline `Road v1.0`, tên file kèm `revision`, số ảnh kiểm (6), **số nhãn đã kiểm** (shape cộng tag).
2. Bảng tổng hợp: đủ **12 mã**, mỗi mã có **số mục kiểm** và số lỗi. Đây là 3 điểm của rubric, dễ mất nếu để trống cột "Số mục kiểm".
3. Danh sách lỗi: mỗi lỗi một dòng, đủ mã, ảnh, nhãn (label + id), mức, mô tả ngắn.
4. Ca mơ hồ: ảnh, câu hỏi cho lead, lời đáp nếu có.
5. Quyết định, kèm phép tính tỉ lệ.

### 9.4 Luật quyết định và cách tính

`[QC]` mục 3, giữ nguyên theo bài:

- Có ít nhất một lỗi **nặng** → **Rework**.
- Không có lỗi nặng, lỗi **chính** trên **5 %** số nhãn đã kiểm → **Rework**.
- Còn câu hỏi chưa có lời đáp ảnh hưởng tới kết luận → **Hold** (chỉ người kiểm quyết; `road_check` không bao giờ ra Hold).
- Còn lại → **Release**.

Mẫu số là **số nhãn đã kiểm** (shape cộng tag), **không phải** số ảnh. Ví dụ: kiểm 6 ảnh, được 90 nhãn, có 4 lỗi chính, 0 lỗi nặng → 4/90 = 4,4 % → **Release**. Cùng 4 lỗi chính nhưng chỉ kiểm 70 nhãn → 5,7 % → **Rework**.

### 9.5 Coach kiểm lại phiếu của bạn

Coach kiểm lại **3 lỗi** bạn đã ghi và **1 ảnh** bạn ghi "không lỗi" `[RUB]`. Nghĩa là: ghi lỗi phải đúng và đủ cụ thể để người khác tìm lại được (mã ảnh, label, id). Ghi lỗi không tồn tại hoặc bỏ sót lỗi nặng làm mất điểm phần này (15 điểm).

## 10. Export — 16:15

### 10.1 Save và Finish job

Bấm **Save** ở thanh trên cùng. Mở **Menu** (góc trên bên trái) → **Finish the job** → **Continue** `[HINH]`. Việc này lưu nhãn và chuyển job sang `completed`.

Quay lại trang task kiểm cột **State** phải là `completed`. Làm cho **mọi** job: front, fisheye, và hai task extra nếu có làm `[DELIV]`.

### 10.2 Export

Menu → **Export job dataset** `[HINH]`:

- Format: **CVAT for images 1.1** (không phải COCO).
- **Save images**: tắt. Ảnh thuộc bộ dữ liệu có giấy phép riêng; người nhận đã có ảnh, chỉ cần nhãn `[DELIV]`.
- Custom name: `<tên>-front` (task fisheye thì `<tên>-fisheye`).

Bấm OK, tải file zip ở trang **Requests**. Làm tương tự cho task fisheye.

### 10.3 Lint và tạo manifest

```bash
PYTHONPATH=src python3 -m road_lab.road_check lint <tên>-front.zip <tên>-fisheye.zip --manifest <tên>-manifest.json --name <tên> --revision 1
```

`--revision` là lần nộp: `1` lần đầu, `2` sau Rework `[DELIV]`. Ba cờ có thật trong `road_check.py` là `--manifest`, `--name`, `--revision`; `--name` mặc định là `learner` nên phải truyền.

Điều kiện đạt ở bước này `[DELIV]`, `[CP]`:

- File mở lại được, không còn cảnh báo mức **nặng** (ngoại lệ QC1-02 đã xác nhận với coach).
- Mở `<tên>-manifest.json`, kiểm `contains_images` là `false`.
- Kiểm nhanh trong manifest: `format`, `guideline`, `name`, `revision`, `created_at` (UTC), `files[].sha256`, `files[].bytes`, `files[].images`, `images_all_tags`, `images_unlabelled`, `shapes_by_label`, `lint` theo ba mức.

`lint` **chỉ** kiểm định dạng, không so với GT và không cho điểm `[README]`. Nó kiểm: tag, thiếu L1/R1, polyline vẽ từ xa về gần, nhiều polyline cùng `position`, fisheye chỉ có 2 điểm, `edge_zone` so với 80 % bán kính, box thấp hơn 8 px `[AG]`.

## 11. Báo cáo cá nhân

Mở `templates/report.md`, lưu thành `<tên>-report.md`. Điền đủ tám mục. Ba mục được chấm tay `[RUB]`:

1. **Mục 3 — bảng ca khó** (2 điểm): mỗi dòng có ảnh, nhãn, phân vân giữa hai lựa chọn, đã chọn gì, **lý do**.
2. **Mục 4 — phiếu QC 1 nhận được** (2 điểm): bạn nào kiểm lô của bạn, quyết định nhận được, bảng mã lỗi kèm đồng ý/không và đã sửa chưa.
3. **Mục 7 — tự đánh giá** (1 điểm): lỗi bạn mắc nhiều nhất theo mã QC1-xx và cách tránh ở Ngày 20; nhãn của bạn đi vào model ở đâu và một lỗi đã sửa làm model học sai thế nào.

Mục 1, 2, 5 phải có **ảnh chụp màn hình** và bảng kiểm file, vì rubric dòng "Project, tag và file" có 2 điểm cho phần này `[RUB]`. Bốn ảnh chụp theo mẫu: tab Labels của project; một ảnh front đã gán đủ; một ảnh fisheye phóng to đoạn polyline cong; một đoạn XML có `<polyline label="lane">`.

Mục 8 là hoạt động buffer tùy chọn, không tính điểm `[RUB]`, `[SUB]`.

## 12. Buffer / Rework

Khi nhận phiếu QC 1 có quyết định Rework `[DELIV]` mục 4:

1. **Trước khi export lại**, cất bản cũ: chép hai file zip và manifest hiện tại vào thư mục `r1/` trên máy; đổi tên manifest cũ thành `<tên>-manifest-r1.json`. Lệnh tạo manifest mới ghi đè file cùng tên, nên phải cất trước.
2. Sửa trên CVAT. Export lại, **giữ nguyên tên zip**.
3. Tạo manifest mới với `--revision 2`.
4. Ghi vào mục 4 của báo cáo: đã sửa lỗi nào, theo phiếu QC nào, và lần nộp mới.

Nhờ `sha256` và `revision`, người kiểm phân biệt bản gốc với bản sửa mà không cần đổi tên file chấm. `road_check` từ chối ghi manifest đè lên chính file nhãn và không tạo manifest khi còn file không mở được.

Hoạt động row-anchor là tùy chọn, không chấm điểm `[CP]`. Nếu làm, dùng để kiểm lại phép tính tay, không thay việc tự tính `[AG]`:

```bash
PYTHONPATH=src python3 -m road_lab.rowanchor <tên>-front.zip --image A01 --position R1 --rows 720,680,640,600,560
```

## 13. Nộp bài — hạn 16:35

Nộp đúng 5 file lên kênh nộp bài coach chỉ định. Không gửi file GT, không gửi ảnh, không đăng lên kênh chung của lớp `[SUB]`.

Checklist cuối `[SUB]`, `[CP]`:

- [ ] `<tên>-front.zip` — CVAT for images 1.1, không kèm ảnh.
- [ ] `<tên>-fisheye.zip` — CVAT for images 1.1, không kèm ảnh.
- [ ] `<tên>-manifest.json` — tạo bằng `lint --manifest`, `contains_images` là `false`.
- [ ] `<tên>-qc1-for-<tên bạn>.md` — đủ 12 mã, có cột số mục kiểm, quyết định đúng luật.
- [ ] `<tên>-report.md` — có ảnh chụp màn hình và bảng kiểm file ở mục 1.
- [ ] Mọi job ở trạng thái `completed` trước khi export.
- [ ] Đã chạy `lint` lại lần cuối và không còn dòng mức **nặng**.

## 14. Thang điểm để biết mình mất điểm ở đâu

`[RUB]`: tổng 100, trong đó `road_check.py` chấm tự động 78 điểm, coach chấm tay 22 điểm (ảnh chụp 2, Phiếu QC 1 15, báo cáo 5).

| Dòng rubric | Điểm | Mã QC 1 làm trừ điểm |
| --- | ---: | --- |
| Project, tag và file | 10 | QC1-01, QC1-12 |
| Polyline làn, Set A | 25 | QC1-02, QC1-04, QC1-05 |
| Thuộc tính làn | 10 | QC1-03, QC1-06 |
| Vùng lái được | 10 | QC1-07 |
| Đèn và biển | 15 | QC1-08, QC1-09, QC1-10 |
| Fisheye, Set B | 10 | QC1-11, QC1-03 (camera hai bên) |
| Phiếu QC 1 cho bạn khác | 15 | coach chấm tay |
| Báo cáo cá nhân | 5 | coach chấm tay |

Điều kiện **Đạt**: từ 60 điểm **và** lô của chính bạn không còn lỗi nặng sau buffer — tức tag camera đúng mọi ảnh, đủ L1/R1, không đổi nhầm `position`, không sai màu đèn quay về xe, file mở lại được `[RUB]`.

Ảnh bắt buộc chưa làm chỉ làm giảm số ảnh được chấm, vì các tiêu chí tính theo tỉ lệ trên số ảnh đã làm. Làm ít mà đúng tốt hơn làm nhiều mà ẩu. Ảnh thêm làm sai không bị trừ điểm, chỉ không được cộng.

## 15. Sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| Lint báo QC1-01 nhưng đã có tag camera | Tag `camera` đặt trùng hoặc tạo hai lần | Mỗi ảnh đúng một tag cho mỗi loại; xóa tag thừa trong bảng Objects |
| Lint báo "vẽ từ xa về gần" | Click điểm xa trước | Xóa polyline, vẽ lại từ đáy ảnh |
| Lint báo nhiều polyline cùng `position` | Hai vạch cùng bên nhưng gán cùng nhãn | Kiểm lại L1/R1/L2/R2 theo làn đang đi |
| Lint báo fisheye chỉ có 2 điểm | Vẽ thẳng hai đầu | Thêm điểm theo cung, dày ở vòng ngoài |
| Lint báo `edge_zone` | Tâm box ngoài 80 % bán kính | Bật `edge_zone` cho box đó |
| Lint báo box thấp hơn 8 px | Đèn, biển quá nhỏ | Đây là gợi ý tự kiểm, **không** phải lỗi chấm `[QC]`; không phải gán nếu không thấy rõ |
| Manifest ghi `contains_images: true` | Quên tắt *Save images* khi export | Export lại, tắt *Save images* |
| `lint` không tạo manifest | Còn file không mở được | Sửa file trước; script từ chối ghi manifest khi file hỏng |
| Manifest cũ bị ghi đè | Không cất bản `r1/` trước khi chạy lần 2 | Chép zip và manifest cũ vào `r1/` trước |
| Export ra COCO | Chọn sai format | Chọn lại **CVAT for images 1.1** |
| Không tìm thấy `python3` trên Windows | Windows dùng `python` | Dùng `python`, hoặc `py -3` |
| `ModuleNotFoundError: road_lab` | Thiếu `PYTHONPATH=src` | Chạy từ gốc repo, đặt `PYTHONPATH=src` (PowerShell: `$env:PYTHONPATH="src"`) |

## 16. Lệnh tham chiếu nhanh

Tất cả chạy từ gốc repo `[AG]`. Trên PowerShell, đặt `$env:PYTHONPATH="src"` một lần rồi bỏ tiền tố `PYTHONPATH=src`.

```bash
# M0: kiểm môi trường
PYTHONPATH=src python3 -m road_lab.road_check selftest

# Task 0: in taxonomy để so tab Labels → Raw
PYTHONPATH=src python3 -m road_lab.taxonomy

# Export: lint + tạo manifest bàn giao
PYTHONPATH=src python3 -m road_lab.road_check lint <tên>-front.zip <tên>-fisheye.zip \
    --manifest <tên>-manifest.json --name <tên> --revision 1

# Buffer tùy chọn: row-anchor
PYTHONPATH=src python3 -m road_lab.rowanchor <tên>-front.zip --image A01 --position R1 \
    --rows 720,680,640,600,560

# Chạy test (cần pytest)
uv run --with pytest==8.3.4 pytest -q
```

## 17. Bảng thời gian

`[README]`:

| Mốc | Giờ | Việc |
| --- | --- | --- |
| M0 | 13:00 | Điểm danh, kiểm repo, gói 28 ảnh, đăng nhập CVAT, selftest |
| Task 0 | 13:15 | Kiểm project: 6 label vẽ, 4 label tag, 4 task |
| Task 1 | 13:50 | Gán A01–A12; xong sớm thì A13–A16 |
| Task 2 | 15:05 | Gán B01–B08; xong sớm thì B09–B12; 5 phút cuối self-QC |
| Task 3 | 15:40 | Đổi lô, điền Phiếu QC 1 |
| Export | 16:15 | Export CVAT for images 1.1, lint, manifest |
| Buffer | 16:35 | Sửa theo phiếu nhận được; hạn nộp |

## 18. Ghi chú về tài liệu gốc

- Ảnh minh hoạ trong `docs/images/huong-dan-cvat/` là ảnh tổng hợp do script vẽ, có dòng `SYNTHETIC … - not a dataset image`; thao tác giống hệt ảnh thật `[HINH]`.
- `manifests/manifest_front.csv` trong repo hiện chỉ có dòng tiêu đề, nên trọng tâm từng ảnh A01–A12 phải lấy từ coach. `manifests/manifest_fisheye.csv` đã có đủ 12 dòng và đang ở trạng thái "ứng viên — coach xem lại và chốt".
- Ngưỡng `lane_match_px` 25, `lane_stop_px` 15, `curb_dev_px` 5, `drivable_iou` 0.85, `crosswalk_iou` 0.75, `box_match_iou` 0.5, `box_tight_iou` 0.75 là quyết định thiết kế của Lab Coach, chưa hiệu chỉnh trên bài thật `[AG]` mục 4. Ngưỡng 5 px, 8 px, 80 % bán kính và 5 % lỗi chính lấy từ guideline.
- Nếu `lab/AGENTS.md` khác guideline về **quy tắc gán** thì guideline thắng; khác về **ngưỡng hay CLI** thì `lab/AGENTS.md` thắng `[AG]`.
