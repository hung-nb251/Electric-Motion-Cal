# Thiết kế hệ truyền động xe con cầu trục — x = 2

Dự án học phần **EE4332 – học kỳ 20261**, tính toán phần cứng và xây dựng logic trạng thái cho **chuyển động ngang của xe con cầu trục**. Bản hiện hành kế thừa mô hình bảng tính khóa trước, thay x = 2 và sửa các công thức chưa nhất quán.

## Hồ sơ hiện hành

| Tệp | Nội dung |
| --- | --- |
| [Bảng tính x2](outputs/bao_cao_xe_con/Tinh_toan_xe_con_x2_theo_mau.xlsx) | Công thức x2, chu kỳ S-curve, đồ thị và kiểm tra thiết bị. |
| [Báo cáo Word](outputs/bao_cao_xe_con/Bao_cao_xe_con_x2_theo_mau.docx) | Thuyết minh cơ khí, motor, thiết bị và logic an toàn. |
| [Báo cáo PDF](outputs/bao_cao_xe_con/Bao_cao_xe_con_x2_theo_mau.pdf) | Bản để đọc và in, 12 trang. |
| [Lưu đồ SVG](outputs/bao_cao_xe_con/Luu_do_trang_thai.svg) | Hình vector các trạng thái S0–S8. |

Bộ **x2_theo_mau** ở trên là bản hiện hành, thay thế bản tính 2,2 kW trước đây. Các bản xuất cũ và bản sao tạm đã được dọn khỏi thư mục làm việc.

## Đầu vào và giả thiết

| Thông số | Quy luật | x = 2 |
| --- | --- | ---: |
| Tải định mức Q | 10 000 + 1 111x | 12 222 kg |
| Khối lượng cơ cấu nâng hạ m_h | 200 + 11x | 222 kg |
| Chiều cao nâng h | 10 + x | 12 m |
| Tốc độ ngang tối đa | 0,1 + 0,01x | 0,12 m/s |
| Gia tốc giới hạn | Không đổi | 0,5 m/s² |
| Độ giật giới hạn | Không đổi | 2 m/s³ |

Chiều cao nâng **không phải hành trình ngang**. Khối lượng chuyển động theo dữ liệu đề: có tải 12 444 kg, không tải 222 kg. Khối lượng khung và phụ kiện chưa nằm trong m_h phải cộng thêm khi có dữ liệu.

Cấu hình kế thừa sheet x=1: bánh D = 250 mm; i = 100; hệ số cản μ = 0,2; hiệu suất cơ khí η = 0,96; dự trữ k = 1,2. Quán tính rotor motor tham khảo là 0,039 kg·m². Giữ μ theo mô hình bài tập; không tự coi hệ số cản là hệ số bám ray.

## Kết quả chính

| Đại lượng | Kết quả |
| --- | ---: |
| Lực kéo tại giới hạn a = 0,5 | 30 637,128 N |
| Mô-men quy đổi có dự trữ, chưa gồm rotor | 47,8705 N·m |
| Công suất theo mô hình giản lược của mẫu | 4,5956 kW |
| Motor tham khảo | 5,5 kW, 6 cực; 973 vòng/phút |
| Tốc độ motor làm việc | 916,73 vòng/phút |
| Công suất hiệu dụng toàn chu kỳ | 1,9247 kW |
| Mô-men RMS toàn chu kỳ | 20,9738 N·m |
| Mô-men đỉnh quỹ đạo có dự trữ | 42,0492 N·m |
| Bao mô-men có rotor tại a = 0,5, có dự trữ | 66,5905 N·m |
| VFD sơ bộ với hệ số 1,3 | Cấp 7,5 kW |
| Ngưỡng dòng bảo vệ theo đề | 18 A; mốc khảo sát 20 A |

Motor tham khảo có mô-men danh định 53,9 N·m, đáp ứng sơ bộ quỹ đạo tăng tốc 2 giây. Nếu khai thác gần a = 0,5, cần kiểm tra quá tải motor/VFD tối thiểu khoảng 1,235 lần. Số liệu motor được kế thừa mẫu, chưa xác minh catalog của mã đặt hàng.

## Các chỉnh sửa so với mẫu

1. Liên kết Q, m_h, h, v với ô x = 2; không nội suy i hoặc η giữa các sheet.
2. Sửa công suất thành `P = M × ω`: mô-men đã chia η thì không chia hiệu suất lần nữa.
3. Tính hiệu dụng bằng tích phân `P(t)²`; bổ sung mô-men RMS và mô-men tăng tốc rotor.
4. Thêm S-curve với thời gian jerk 0,25 s: gia tốc đỉnh 0,068571 m/s² và độ giật đỉnh 0,274286 m/s³.
5. Sửa chạy đều không tải thành 82,5 s để hai lượt cùng 10,32 m. Các thời gian còn lại giữ theo mẫu: tăng tốc 2 s; có tải chạy đều 80 s, giảm tốc 10 s; nghỉ 30 s; không tải giảm tốc 5 s. Tổng chu kỳ 211,5 s, chỉ có một khoảng nghỉ theo mẫu.

## Cách sử dụng bảng tính

1. Mở **Tinh_toan_xe_con_x2_theo_mau.xlsx**. Sheet **Tinh_toan_x2**, ô **E5 = 2** là chữ số đề. E51:E53 là khối lượng/quán tính chưa có số liệu, đang để 0 để tính theo đầu vào được giao.
2. Xem lực, tốc độ, công suất ở E18:E24. Cột M phần trên giữ ramp tuyến tính để đối chiếu; M34, M36, M37 lấy kết quả S-curve.
3. Sheet **Chu_ky** chứa pha chuyển động, tích phân và kiểm tra. Vùng A22:C32 là tổng hợp; A35:K95 là các điểm tích phân.
4. Sheet **Do_thi** có dữ liệu và đồ thị v(t), F(t), P(t), M(t) đủ hai lượt. P, M tại trục motor; F tại bánh; dấu âm chỉ chiều về.
5. Sheet **Thiet_bi** tổng hợp motor, VFD, bảo vệ và hãm; các mục ghi cần catalog chưa phải thiết bị đã chốt.
6. Thay dữ liệu Excel thì cập nhật lại số liệu Word/PDF; báo cáo và SVG không tự cập nhật theo Excel. Nếu thay thời gian ramp, kiểm tra thời gian pha không âm, a, j và quãng đường.

## Logic trạng thái

```text
S0 Khóa khởi động → S1 Sẵn sàng → S2 Tạo mô-men tại tốc độ 0
→ S3 Mở phanh, chờ xác nhận → S4 Chạy → S5 Giảm tốc
→ S6 Đóng phanh, xác nhận rồi bỏ mô-men → S1

S7 Lỗi đã chốt: xử lý nguyên nhân, Reset tay, yêu cầu lệnh chạy mới.
S8 Dừng khẩn: nhánh an toàn độc lập tác động STO và phanh.
```

Không tự chạy lại khi có điện hoặc khi nhả E-stop. Giới hạn vận hành chỉ cho phép rút theo hướng hợp lệ sau khi dừng; cực hạn an toàn khóa cả hai chiều. Liên khóa, timeout và quy trình nằm trong báo cáo.

## Phần cần bổ sung trước khi chốt phần cứng

- Khối lượng thực, quán tính phanh/bánh, phản lực bánh, mô hình cản và khả năng bám ray.
- Catalog motor và chế độ nhiệt; hộp số, khớp nối, phanh.
- Mã VFD, dòng HD và quá tải; điện trở hãm theo R_min, điện áp chopper, năng lượng và công suất xung. Chưa chốt Ω/W.
- Phối hợp MCCB/cầu chì với đầu vào VFD, khả năng cắt, cáp và điều kiện lắp đặt. Mốc 20 A chỉ theo tiêu chí bài tập.
- Kiểm chứng quãng đường dừng, mạch an toàn và logic trên thiết bị.

Đây là báo cáo tính chọn sơ bộ theo mẫu học phần, chưa phải hồ sơ chế tạo hoặc chứng nhận an toàn hoàn chỉnh.

## Nguồn và mã dựng

- [Bảng tính khóa trước](<Tính toán thông số động cơ.xlsx>): các trường hợp x = 1, 3, 6; sheet a=6 có E5 ghi nhầm 1.
- [Mẫu kiến trúc](<SYSTEM ARCHITECTURE – CRANE TROLLEY DRIVE SYSTEM.txt>).
- [SOW](SOW_HungNB.docx).
- `tmp/report_build/rebuild_x2.mjs`: dựng Excel có công thức.
- `tmp/report_build/build_report_x2.py`: dựng báo cáo và biểu đồ.
- `tmp/report_build/build_report.py`: chứa các hàm định dạng và nội dung logic được bản x2 sử dụng lại; giữ làm thành phần phụ thuộc, không chạy để xuất báo cáo cũ.
- `tmp/report_build/`: giữ mã dựng, dữ liệu nguồn, kết quả x2 và ảnh lưu đồ cần thiết; không thuộc hồ sơ nộp chính.

## Giữ thư mục gọn

Ảnh render, log, bản sao cũ và thư viện Python cài tạm đã được dọn. `.gitignore` loại trừ các file trung gian khi tạo lại. Tài liệu nguồn, bộ báo cáo hiện hành và lịch sử Git được giữ nguyên.

Đọc hoặc sửa trực tiếp Word/Excel không cần cài thư viện. Nếu chạy lại mã dựng, chuẩn bị Python với các gói trong `tmp/report_build/requirements-build.txt`; mã JavaScript cần `@oai/artifact-tool` từ môi trường dựng tài liệu. Liên kết `node_modules` tạm đã được gỡ, cần cấu hình lại khi dựng Excel. Xuất PDF bằng script PowerShell yêu cầu Microsoft Word.
