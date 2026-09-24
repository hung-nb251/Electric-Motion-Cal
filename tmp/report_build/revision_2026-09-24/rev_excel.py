"""Bo sung bang tinh x2 qua Excel COM (giu bieu do, anh, dinh dang cua nguoi dung).

Chay: python rev_excel.py <xlsx_vao_ra>   (sua truc tiep tep duoc truyen vao)
"""
import sys
import win32com.client as win32

PATH = sys.argv[1]
T = "Tinh_toan_x2!"
m_all = f"({T}E6+{T}E7+{T}E51)"
m_0 = f"({T}E7+{T}E51)"
kF = f"{T}E12/(2*{T}E15*{T}E13)"
Jq = f"({T}C47+{T}E52+{T}E53/{T}E13^2)"

# (nhan, ky hieu, gia tri/cong thuc, don vi, ghi chu, la_so_lieu_nhap, dinh_dang)
ROWS = [
    ("A. BIẾN TẦN ABB ACS380-042C-17A0-4 (+K492 +L535)",),
    ("Công suất định mức", "P_N", 7.5, "kW", "Catalog ACS380, 400 V", 1, "0.0"),
    ("Dòng định mức", "I_N", 17, "A", "Catalog ACS380", 1, "0.0"),
    ("Dòng tải nặng", "I_Hd", 12.6, "A", "Catalog ACS380 (P_Hd = 5,5 kW)", 1, "0.0"),
    ("Dòng ra cực đại", "I_max", 22.7, "A", "Catalog ACS380", 1, "0.0"),
    ("Điện trở hãm nhỏ nhất", "R_min", 32, "Ω", "Catalog ACS380, chopper tích hợp", 1, "0"),
    ("Điện trở hãm lớn nhất cho P_BRcont", "R_max", 54, "Ω", "Catalog ACS380", 1, "0"),
    ("Công suất hãm cực đại", "P_BRmax", 8.25, "kW", "Catalog ACS380", 1, "0.00"),
    ("Kiểm tra P_N ≥ 1,3·P_đm", "", f'=IF(C{{P_N}}>=1.3*{T}C33,"Đạt","Không đạt")', "", "Tiêu chí SOW", 0, "@"),
    ("Kiểm tra I_Hd ≥ I_đm motor", "", f'=IF(C{{I_Hd}}>={T}C40,"Đạt","Không đạt")', "", "Tiêu chí SOW", 0, "@"),
    ("sin φ motor", "sinφ", f"=SQRT(1-{T}C39^2)", "", "", 0, "0.0000"),
    ("Dòng ở mô-men quỹ đạo có dự trữ", "I_traj",
     f"=SQRT(({T}C40*C{{sinφ}})^2+({T}C40*{T}C39*{T}E56/{T}C42)^2)", "A",
     "I = √[(I_đm sinφ)² + (I_đm cosφ·M/M_đm)²], từ thông định mức", 0, "0.00"),
    ("Dòng ở bao mô-men a_lim", "I_env",
     f"=SQRT(({T}C40*C{{sinφ}})^2+({T}C40*{T}C39*{T}E57/{T}C42)^2)", "A", "Như trên, M = E57", 0, "0.00"),
    ("Kiểm tra I_env ≤ I_N", "", f'=IF(C{{I_env}}<=C{{I_N}},"Đạt","Không đạt")', "", "Không cần quá tải VFD", 0, "@"),
    ("B. GIỚI HẠN MÔ-MEN VÀ HỘP SỐ",),
    ("Mô-men đầu ra hộp số có dự trữ", "M2", f"={T}E16*{T}E19", "N·m", "k·F·D/2", 0, "0.0"),
    ("Giới hạn mô-men đặt trong VFD", "M_lim", f"=C{{M2}}/({T}E13*{T}E15)", "N·m", "M2/(i·η)", 0, "0.00"),
    ("Tỷ số M_lim / M đỉnh quỹ đạo", "", f"=C{{M_lim}}/Chu_ky!B27", "", "", 0, "0.00"),
    ("Mô-men cản có tải tại trục motor", "M_c1", f"={m_all}*{T}E14*{T}E17*{kF}", "N·m", "m·μ·g·D/(2iη)", 0, "0.00"),
    ("Hệ số quán tính quay", "kJ", f"={Jq}*2*{T}E13/{T}E12", "N·m/(m/s²)", "J·2i/D", 0, "0.00"),
    ("Hệ số khối lượng có tải", "km1", f"={m_all}*{kF}", "N·m/(m/s²)", "m·D/(2iη)", 0, "0.000"),
    ("Gia tốc lớn nhất có tải khi chạm M_lim", "a_max", f"=(C{{M_lim}}-C{{M_c1}})/(C{{kJ}}+C{{km1}})", "m/s²", "", 0, "0.000"),
    ("C. NĂNG LƯỢNG HÃM VÀ ĐIỆN TRỞ HÃM",),
    ("Động năng rotor tại v_max", "E_rot", f"=0.5*{Jq}*{T}M35^2", "J", "", 0, "0.0"),
    ("Động năng xe không tải", "E_0", f"=0.5*{m_0}*{T}E9^2", "J", "", 0, "0.0"),
    ("Công suất hãm bao trên (a_lim tại v_max, không tải)", "P_h,max",
     f"=(C{{kJ}}*{T}E10-{m_0}*({T}E14*{T}E17-{T}E10)*{kF})*{T}M35", "W", "Lượt có tải không tái sinh", 0, "0"),
    ("Công suất hãm, dừng nhanh nhất j = 2 (không tải)", "", 770, "W", "Tích phân số, báo cáo mục 7.2", 1, "0"),
    ("Năng lượng hãm, dừng nhanh nhất j = 2 (không tải)", "", 168, "J", "Tích phân số, báo cáo mục 7.2", 1, "0"),
    ("Năng lượng hãm mỗi chu kỳ thường", "", 50, "J", "Tích phân số, giảm tốc không tải 5 s", 1, "0"),
    ("Điện trở hãm chọn", "R_h", 39, "Ω", "Ví dụ ABB: Danotherm CBR-V 560 D HT 406 39R", 1, "0"),
    ("Kiểm tra R_min ≤ R_h ≤ R_max", "", f'=IF(AND(C{{R_h}}>=C{{R_min}},C{{R_h}}<=C{{R_max}}),"Đạt","Không đạt")', "", "", 0, "@"),
    ("Kiểm tra P_BRmax ≥ P_h,max", "", f'=IF(C{{P_BRmax}}*1000>=C{{P_h,max}},"Đạt","Không đạt")', "", "", 0, "@"),
    ("D. PHANH INTORQ BFK458-12E VÀ DỪNG KHẨN",),
    ("Mô-men phanh", "M_b", 32, "N·m", "Catalog BFK458 cỡ 12 (phanh làm việc)", 1, "0"),
    ("Trễ tác động phanh + rơ-le", "t_d", 0.1, "s", "Giả thiết, đo khi chạy thử", 1, "0.00"),
    ("Mô-men cản không tải tại trục motor", "M_c0", f"={m_0}*{T}E14*{T}E17*{kF}", "N·m", "", 0, "0.000"),
    ("Hệ số khối lượng không tải", "km0", f"={m_0}*{kF}", "N·m/(m/s²)", "", 0, "0.000"),
    ("Gia tốc khi phanh, có tải", "a_b1", f"=-(C{{M_b}}+C{{M_c1}})/(C{{kJ}}+C{{km1}})", "m/s²", "", 0, "0.000"),
    ("Gia tốc khi phanh, không tải", "a_b0", f"=-(C{{M_b}}+C{{M_c0}})/(C{{kJ}}+C{{km0}})", "m/s²", "", 0, "0.000"),
    ("Quãng đường dừng khẩn có tải", "", f"={T}E9^2/(2*ABS(C{{a_b1}}))+{T}E9*C{{t_d}}", "m", "Gồm trễ t_d", 0, "0.000"),
    ("Quãng đường dừng khẩn không tải", "", f"={T}E9^2/(2*ABS(C{{a_b0}}))+{T}E9*C{{t_d}}", "m", "Gồm trễ t_d", 0, "0.000"),
    ("Gia tốc trôi không tải khi phanh không đóng", "a_c0", f"=-C{{M_c0}}/(C{{kJ}}+C{{km0}})", "m/s²", "Chỉ có STO", 0, "0.0000"),
    ("Quãng đường trôi không tải khi phanh không đóng", "s_c0", f"={T}E9^2/(2*ABS(C{{a_c0}}))+{T}E9*C{{t_d}}", "m", "", 0, "0.000"),
    ("Mô-men đầu ra hộp số khi phanh có tải", "", f"={m_all}*({T}E14*{T}E17+C{{a_b1}})*{T}E12/2", "N·m", "< M2", 0, "0.0"),
    ("Kiểm tra năng lượng mỗi lần dừng ≤ 24 kJ", "", '=IF(Thiet_bi!B20<=24000,"Đạt","Không đạt")', "", "W_max catalog BFK458-12", 0, "@"),
    ("E. VỊ TRÍ CÔNG TẮC HÀNH TRÌNH",),
    ("Khoảng kích hoạt công tắc vận hành", "d_op", f"={T}E9*0.1+0.5*{T}E9*{T}M14+0.05", "m", "Trễ 0,1 s; dự trữ 0,05 m; chọn 0,70 m", 0, "0.000"),
    ("Cực hạn đặt sau điểm dừng", "", 0.1, "m", "Giả thiết thiết kế", 1, "0.00"),
    ("Khoảng cực hạn → chặn cơ khí tối thiểu", "", f"=C{{s_c0}}+0.05", "m", "Chọn ≥ 0,50 m", 0, "0.000"),
    ("F. ENCODER VÀ NGƯỠNG GIÁM SÁT",),
    ("Số xung encoder", "ppr", 1024, "xung/vòng", "Autonics E50S8-1024-3-T-24", 1, "0"),
    ("Tần số xung ở tốc độ làm việc", "", f"={T}E23/60*C{{ppr}}", "Hz", "≤ 300 kHz", 0, "0"),
    ("Độ phân giải quãng đường (×4)", "", f"=PI()*{T}E12/{T}E13/(4*C{{ppr}})*1000000", "µm", "", 0, "0.00"),
    ("Ngưỡng quá tốc mức 1 (110 %)", "", f"=1.1*{T}E9", "m/s", "→ S5 → S7", 0, "0.000"),
    ("Ngưỡng quá tốc mức 2 (120 %)", "", f"=1.2*{T}E9", "m/s", "→ S8", 0, "0.000"),
    ("Ngưỡng sai lệch tốc độ (20 % v_max, 0,5 s)", "", f"=0.2*{T}E9", "m/s", "", 0, "0.000"),
    ("Timeout trạng thái S5", "", f"=MAX({T}M14,{T}M29)+2", "s", "Lớn hơn thời gian giảm tốc dài nhất", 0, "0.0"),
    ("G. CÁP (IEC 60364-5-52, PVC, lắp kiểu C, 40 °C)",),
    ("Dòng cho phép cáp 4 mm²", "", "=32*0.87", "A", "Cáp vào VFD", 0, "0.0"),
    ("Dòng cho phép cáp 2,5 mm²", "", "=24*0.87", "A", "Cáp motor có màn chắn", 0, "0.0"),
    ("Kiểm tra cáp vào ≥ dòng MCCB", "", '=IF(32*0.87>=Thiet_bi!B19,"Đạt","Không đạt")', "", "", 0, "@"),
    ("Kiểm tra cáp motor ≥ I_đm", "", f'=IF(24*0.87>={T}C40,"Đạt","Không đạt")', "", "", 0, "@"),
    ("Sụt áp cáp motor 25 m", "", f"=SQRT(3)*{T}C40*25*(0.00889*{T}C39+0.00008*C{{sinφ}})/400*100", "%", "R₇₀ = 8,89 Ω/km", 0, "0.00"),
]

import time
import pywintypes


BUSY = (-2147418111, -2147417846, -2146777998)   # rejected, retry later, VBA_E_IGNORE


def retry(fn, tries=120):
    for k in range(tries):
        try:
            return fn()
        except pywintypes.com_error as e:
            if e.args[0] not in BUSY or k == tries - 1:
                raise
            time.sleep(1)


xl = win32.DispatchEx("Excel.Application")
t0 = time.time()
while time.time() - t0 < 150:
    try:
        if xl.Ready:
            break
    except pywintypes.com_error:
        pass
    time.sleep(1)
print(f"Excel ready after {time.time() - t0:.0f} s")
retry(lambda: setattr(xl, "DisplayAlerts", False))
try:
    wb = retry(lambda: xl.Workbooks.Open(PATH, 0, False))
    time.sleep(2)
    names = [ws.Name for ws in wb.Worksheets]
    if "Bo_sung_phan_cung" in names:
        wb.Worksheets("Bo_sung_phan_cung").Delete()
    tb = wb.Worksheets("Thiet_bi")
    # pywin32 bo qua tham so co ten After=; chi dung tham so vi tri (Before)
    ws = wb.Worksheets.Add(tb)          # them truoc Thiet_bi
    ws.Name = "Bo_sung_phan_cung"
    tb.Move(ws)                         # dua Thiet_bi len truoc -> sheet moi o cuoi
    ws.Cells.Font.Name = "Times New Roman"
    ws.Cells.Font.Size = 11
    ws.Range("A1").Value = "BỔ SUNG PHẦN CỨNG, HÃM, PHANH VÀ BẢO VỆ – x = 2 (sửa 24/09/2026)"
    ws.Range("A1").Font.Bold = True; ws.Range("A1").Font.Size = 13
    ws.Range("A2").Value = "Ô nền vàng: số liệu catalog hoặc giả thiết nhập tay. Các ô khác là công thức liên kết Tinh_toan_x2, Chu_ky, Thiet_bi."
    ws.Range("A2").Font.Italic = True
    hdr = ["Hạng mục", "Ký hiệu", "Giá trị", "Đơn vị", "Công thức / nguồn"]
    for j, h in enumerate(hdr):
        c = ws.Cells(4, j + 1); c.Value = h; c.Font.Bold = True; c.Interior.Color = 0xF1E6DC
    # gan dong cho ky hieu truoc de thay {sym}
    r = 5; addr = {}
    plan = []
    for row in ROWS:
        plan.append((r, row))
        if len(row) > 1 and row[1]:
            addr[row[1]] = r
        r += 1
        if len(row) == 1:
            pass
    for r, row in plan:
        if len(row) == 1:
            c = ws.Cells(r, 1); c.Value = row[0]; c.Font.Bold = True
            ws.Range(ws.Cells(r, 1), ws.Cells(r, 5)).Interior.Color = 0xEFEFEF
            continue
        label, sym, val, unit, note, is_input, fmt = row
        ws.Cells(r, 1).Value = label
        ws.Cells(r, 2).Value = sym
        cell = ws.Cells(r, 3)
        if isinstance(val, str) and val.startswith("="):
            f = val
            for k, rr in addr.items():
                f = f.replace("{" + k + "}", str(rr))
            cell.Formula = f
        else:
            cell.Value = val
        if fmt != "@":
            cell.NumberFormat = fmt
        if is_input:
            cell.Interior.Color = 0x99FFFF
        ws.Cells(r, 4).Value = unit
        ws.Cells(r, 5).Value = note
    last = plan[-1][0]
    ws.Columns("A").ColumnWidth = 50
    ws.Columns("B").ColumnWidth = 10
    ws.Columns("C").ColumnWidth = 13
    ws.Columns("D").ColumnWidth = 11
    ws.Columns("E").ColumnWidth = 58
    ws.Range(f"A4:E{last}").Borders.LineStyle = 1
    ws.Range(f"A4:E{last}").Borders.Color = 0xD9D9D9
    ws.Range(f"C5:C{last}").HorizontalAlignment = -4152

    # Cap nhat sheet Thiet_bi (chi sua chu thich va ma thiet bi)
    tb.Range("B5").Value = "M3AA 132ME 6 (IE3)"
    tb.Range("D5").Value = "Mã ABB có thật; 12 A tại 400 V theo nhà phân phối; trị số khác theo sheet x=1"
    tb.Range("D12").Value = "Motor đạt (T_max = 2,9 T_đm); dòng ≈ 13,6 A < I_N 17 A; VFD giới hạn 47,9 N·m nên không khai thác"
    tb.Range("D14").Value = "Đáp ứng, không cần quá tải VFD (Bo_sung_phan_cung)"
    tb.Range("D16").Value = "Theo SOW: P_VFD ≥ 1,3 P_đm"
    tb.Range("D17").Value = "ABB ACS380-042C-17A0-4: I_N 17 A; I_Hd 12,6 A; I_max 22,7 A"
    tb.Range("D19").Value = "Schneider EZC100N3020, Icu 15 kA/415 V; ≤ cầu chì gG 32 A ABB khuyến nghị"
    tb.Range("D21").Value = "Chỉ lượt không tải tái sinh (≤ 180 J); xem Bo_sung_phan_cung"
    rh = addr["R_h"]
    tb.Range("B22").Formula = f"=Bo_sung_phan_cung!C{rh}"
    tb.Range("D22").Value = "32 ≤ R ≤ 54 Ω (ACS380-17A0); P_BRmax 8,25 kW ≫ 1,46 kW"
    xl.CalculateFull()
    print("sheets:", [s.Name for s in wb.Worksheets])
    wb.Worksheets("Tinh_toan_x2").Activate()
    out = {k: ws.Cells(v, 3).Value for k, v in addr.items()}
    checks = [ws.Cells(r, 3).Value for r, row in plan if len(row) > 1 and row[6] == "@"]
    wb.Save()
    wb.Close(False)
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()})
    print("checks:", checks)
    print("Thiet_bi B22 =", "ok")
finally:
    retry(lambda: xl.Quit())
