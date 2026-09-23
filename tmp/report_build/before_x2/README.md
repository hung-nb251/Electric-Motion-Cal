# Thiết kế hệ truyền động xe con cầu trục

Dự án học phần **EE4332 – học kỳ 20261**, tập trung tính toán phần cứng và xây dựng logic an toàn cho **chuyển động ngang của xe con cầu trục** có tải nâng định mức 12 222 kg.

Hồ sơ gồm báo cáo tính toán cơ khí và công suất động cơ, bảng tính có công thức, kiến trúc phần cứng, lưu đồ trạng thái và quy trình vận hành. Phương án hiện tại là thiết kế sơ bộ có điều kiện; các giả thiết và dữ liệu cần bổ sung được nêu trong báo cáo.

## Thông số đầu vào

| Thông số | Ký hiệu | Giá trị |
| --- | --- | ---: |
| Tải nâng định mức | Q | 12 222 kg |
| Khối lượng cơ cấu nâng hạ | m_h | 222 kg |
| Chiều cao nâng | h | 12 m |
| Tốc độ di chuyển ngang tối đa | v_max | 0,12 m/s |
| Gia tốc cực đại | a_lim | 0,5 m/s² |
| Độ giật cực đại | j_lim | 2 m/s³ |

Tốc độ, gia tốc và độ giật trên áp dụng cho **di chuyển ngang của xe con**. Chiều cao nâng 12 m không phải hành trình ngang và không được dùng để tính công suất động cơ nâng trong dự án này.

Khối lượng di chuyển được xác định như sau:

- Có tải: `m = Q + m_h + m_x = 12 444 + m_x` kg.
- Không tải: `m_0 = m_h + m_x = 222 + m_x` kg.
- `m_x` là khối lượng bổ sung chưa có số liệu, gồm khung xe và các bộ phận chưa được tính trong `m_h`. Giá trị `m_x = 0` ở ca cơ sở là mốc tính tối thiểu, không có nghĩa xe con không có tự trọng.

## Phạm vi công việc

- Xác định lực cản, lực kéo và điều kiện bám bánh–ray.
- Tính chọn sơ bộ bánh xe, tỷ số truyền, mô-men hộp số và trục truyền động.
- Quy đổi tải và quán tính về trục động cơ; kiểm tra mô-men đỉnh, công suất và mô-men RMS theo chu kỳ.
- Xây dựng quỹ đạo S-curve đáp ứng giới hạn gia tốc và độ giật khi vận hành có điều khiển.
- Phân tích phanh, năng lượng hãm và khoảng cách dừng.
- Xác định yêu cầu đối với động cơ, biến tần, thiết bị bảo vệ và cảm biến.
- Xây dựng logic khởi động, chạy, dừng, liên khóa, xử lý lỗi và dừng khẩn.

Không bao gồm thiết kế cơ cấu nâng hạ, tang và cáp nâng, cơ cấu di chuyển cầu, kết cấu dầm cầu, bản vẽ chế tạo hoàn chỉnh hoặc chương trình PLC triển khai thực tế.

## Tài liệu trong dự án

### Tài liệu đầu vào

| Tệp | Vai trò |
| --- | --- |
| [SOW_HungNB.docx](SOW_HungNB.docx) | Phạm vi công việc, đầu vào bổ sung và tiêu chí nghiệm thu. |
| [SYSTEM ARCHITECTURE – CRANE TROLLEY DRIVE SYSTEM.txt](<SYSTEM ARCHITECTURE – CRANE TROLLEY DRIVE SYSTEM.txt>) | Mẫu kiến trúc hệ thống hai cấp của khóa trước. |
| [Tính toán thông số động cơ.xlsx](<Tính toán thông số động cơ.xlsx>) | Bảng tính mẫu để đối chiếu mô hình tải và cách chọn thiết bị. |

### Hồ sơ đã tạo

| Tệp | Nội dung |
| --- | --- |
| [Báo cáo Word](outputs/bao_cao_xe_con/Bao_cao_phan_cung_va_logic_xe_con.docx) | Bản thuyết minh có thể chỉnh sửa, gồm tính toán, sơ đồ và quy trình vận hành. |
| [Báo cáo PDF](outputs/bao_cao_xe_con/Bao_cao_phan_cung_va_logic_xe_con.pdf) | Bản 14 trang để đọc, trao đổi và in. |
| [Bảng tính của dự án](outputs/bao_cao_xe_con/Tinh_toan_xe_con_12222kg.xlsx) | Đầu vào có thể thay đổi, công thức tính và kiểm tra điều kiện mô hình. |
| [Lưu đồ trạng thái SVG](outputs/bao_cao_xe_con/Luu_do_trang_thai.svg) | Hình vector riêng để đưa vào báo cáo hoặc trình chiếu. |

Thư mục `tmp/report_build/` chứa mã dựng tài liệu, thư viện bổ sung và ảnh kiểm tra bố cục. Đây là tài nguyên hỗ trợ, không phải hồ sơ bàn giao chính; không cần chạy các mã này để đọc báo cáo hoặc sử dụng bảng tính.

## Phương án tính chọn sơ bộ

| Hạng mục | Giá trị đề xuất hoặc giả thiết |
| --- | --- |
| Động cơ | Không đồng bộ ba pha, 2,2 kW, 6 cực; tốc độ danh định giả định 960 vòng/phút |
| Tỷ số truyền | Khoảng 100:1 |
| Đường kính bánh xe | 250 mm |
| Bố trí bánh | 4 bánh, trong đó 2 bánh chủ động; giả thiết phân bố tải đều |
| Hiệu suất truyền động cơ khí | 0,96 |
| Hệ số dự trữ | 1,2 |
| Hệ số cản chạy quy đổi | 0,01, giả thiết cho mô hình cản lăn |
| Hệ số bám bánh–ray | 0,20, cần kiểm chứng với điều kiện ray thực |
| Quán tính phần quay quy về trục động cơ | 0,015 kg·m², ngân sách giả định cần xác minh |

Với ca cơ sở, mô-men yêu cầu có dự trữ khoảng **18,83 N·m**, công suất cơ bao trên khoảng **1,808 kW** và tốc độ motor làm việc khoảng **916,73 vòng/phút**. Việc chọn động cơ 2,2 kW vẫn phụ thuộc vào khối lượng thực, quán tính, đặc tính mô-men và khả năng phát nhiệt của thiết bị.

Báo cáo giữ phép tính đối chiếu theo hệ số 0,2 trong bảng mẫu: công suất có dự trữ khoảng **4,60 kW**, dẫn đến cấp motor 5,5 kW trong mô hình giản lược. Tuy nhiên, dùng 0,2 làm hệ số cản chạy gây vấn đề về lực bám theo các giả thiết đang xét. Vì vậy, 2,2 kW và 5,5 kW không phải hai cấu hình tương đương đã được xác nhận. Cần thống nhất mô hình cản chạy với giảng viên trước khi chốt phương án.

## Cách sử dụng bảng tính

1. Mở `outputs/bao_cao_xe_con/Tinh_toan_xe_con_12222kg.xlsx`.
2. Tại tab **Dau_vao**, đọc nguồn và ghi chú rồi sửa các ô màu vàng theo dữ liệu nhóm đã xác nhận. Không điền trùng khối lượng giữa `m_h` và `m_x`.
3. Tại tab **Ket_qua**, xem lực kéo, dự trữ bám, mô-men, công suất, quỹ đạo, RMS và năng lượng hãm.
4. Kiểm tra phần điều kiện mô hình cuối tab. Nếu xuất hiện thông báo thiếu dữ liệu, cần tính lại hoặc cần mô hình truyền ngược, xử lý điều kiện đó trước khi sử dụng kết quả.
5. Sau khi thay dữ liệu, cập nhật các số liệu tương ứng trong Word và xuất lại PDF. Báo cáo Word/PDF và hình SVG **không tự cập nhật theo Excel**.

Chu kỳ minh họa sử dụng hành trình ngang **9 m**, tăng/giảm tốc **2 s**, thời gian jerk **0,25 s** và nghỉ **30 s mỗi đầu**. Đây là giả thiết phân tích phụ tải, không phải toàn bộ yêu cầu đã được giao. Nếu hành trình quá ngắn hoặc quỹ đạo thay đổi khiến điều kiện mô hình không còn thỏa mãn, cần xây dựng lại phép tính chu kỳ.

## Logic trạng thái và an toàn

Luồng vận hành chính:

```text
S0 Khóa khởi động
  → S1 Sẵn sàng
  → S2 Tạo mô-men tại tốc độ đặt bằng 0
  → S3 Mở phanh và chờ xác nhận
  → S4 Chạy tiến hoặc lùi
  → S5 Giảm tốc có điều khiển
  → S6 Đóng phanh, xác nhận rồi bỏ mô-men
  → S1 Sẵn sàng
```

Các nhánh bảo vệ gồm **S7 Lỗi đã chốt** và **S8 Dừng khẩn**. Bảng chuyển trạng thái trong báo cáo quy định điều kiện chuyển tiếp và phản ứng theo từng loại lỗi.

- Không chạy khi lệnh tiến và lùi cùng tác động.
- Chỉ bắt đầu chuyển động sau khi drive sẵn sàng và phanh đã mở được xác nhận.
- Trong dừng thường, giảm tốc trước; đóng phanh và xác nhận rồi mới bỏ mô-men.
- Phân biệt giới hạn vận hành theo hướng với cực hạn an toàn độc lập.
- Nhả E-stop hoặc khôi phục nguồn không tự khởi động lại; cần reset và lệnh chạy mới.
- STO ngăn tạo mô-men, không thay cho phanh cơ hoặc dao cách ly nguồn. Dừng khẩn phải được kiểm chứng cùng khả năng hãm của phanh và quãng đường dừng thực.

## Dữ liệu cần bổ sung trước khi chốt thiết kế

- Khối lượng khung xe và phụ kiện, vị trí trọng tâm, phân bố tải trên từng bánh.
- Loại ray, vật liệu và kích thước bánh, ổ lăn, độ dốc, lực kéo cáp và điều kiện bám thực tế.
- Hành trình, chu kỳ và tần suất làm việc thực.
- Catalog motor: dòng điện, mô-men, quán tính, chế độ nhiệt và khả năng làm việc với biến tần.
- Hiệu suất thuận/ngược, mô-men cho phép và giới hạn tải của hộp số.
- Dữ liệu phanh: mô-men, thời gian đóng/mở, năng lượng hãm và số lần hãm cho phép.
- Catalog VFD, ngưỡng chopper và điều kiện chọn điện trở hãm.
- Dòng ngắn mạch, chiều dài và cách lắp cáp để chọn thiết bị bảo vệ.
- Đánh giá rủi ro, yêu cầu đối với mạch an toàn và kết quả thử nghiệm dừng.

## Tình trạng kiểm tra hồ sơ

- Bản báo cáo đã được xuất PDF từ Word và kiểm tra bố cục 14 trang.
- Công thức chính đã được đối chiếu với phép tính độc lập và kiểm tra lỗi trong tệp Excel xuất ra.
- Đã thử thay khối lượng bổ sung, đầu vào trống và thông số quỹ đạo không hợp lệ để kiểm tra cập nhật và cảnh báo của bảng tính.
- Chưa có thử nghiệm phần cứng, nghiệm thu an toàn hoặc xác nhận cấu hình chế tạo.

Danh mục tài liệu kỹ thuật và nguồn tham khảo chi tiết nằm tại mục 14 của báo cáo. Các giới hạn gia tốc và độ giật là yêu cầu đề bài; hồ sơ không tự gán chúng cho một điều khoản TCVN hoặc tuyên bố đạt chứng nhận an toàn.
