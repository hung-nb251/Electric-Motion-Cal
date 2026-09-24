"""Ve hinh cho ban sua 24/09/2026: so do phan cung, cau truc FOC, luu do trang thai.

Chay: python rev_figures.py <thu_muc_xuat>
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.fonttype": "none"})
INK, SAFE, CTRL = "#2c3e50", "#a23b32", "#1f5f8b"
FILL, FILL_S, FILL_C = "#eef3f8", "#f7eceb", "#e8f1ea"


def box(ax, x, y, w, h, text, fill=FILL, edge=INK, size=9, lw=1.1):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor=fill, edgecolor=edge, lw=lw, zorder=2))
    lines = text.split("\n")
    step = 0.36 * size / 9
    top = y + step * (len(lines) - 1) / 2
    for j, ln in enumerate(lines):
        ax.text(x, top - j * step, ln, ha="center", va="center", zorder=3,
                fontsize=size if j == 0 else size - 0.8,
                fontweight="bold" if (j == 0 and len(lines) > 1) else "normal")


def arrow(ax, p, q, color=INK, lw=1.2, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, color=color,
                                 lw=lw, linestyle=ls, zorder=1, shrinkA=0, shrinkB=0))


def poly(ax, pts, color=INK, lw=1.2, ls="-", head=True):
    xs, ys = zip(*pts)
    n = len(pts) - 1 if head else len(pts)
    ax.plot(xs[:n], ys[:n], color=color, lw=lw, ls=ls, zorder=1)
    if head:
        arrow(ax, pts[-2], pts[-1], color=color, lw=lw, ls=ls)


def label(ax, x, y, text, color=INK, size=8, ha="center", va="center", rot=0, bg=True):
    ax.text(x, y, text, color=color, fontsize=size, ha=ha, va=va, rotation=rot, zorder=4,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6) if bg else None)


# ---------------------------------------------------------------- Hinh 2: phan cung
def hardware():
    fig, ax = plt.subplots(figsize=(10.2, 6.6))
    ax.set(xlim=(0, 20.6), ylim=(0, 13.2)); ax.axis("off")
    y1 = 10.6
    specs = [(1.8, 2.9, 1.4, "Lưới điện\n3~ 380/400 V, 50 Hz"),
             (5.3, 2.9, 1.4, "Q1 – MCCB 3P 20 A\nEZC100N3020, 15 kA"),
             (8.8, 2.9, 1.4, "K1 – contactor lực\nLC1D18BD, 24 VDC"),
             (12.4, 3.4, 1.7, "U1 – biến tần FOC\nACS380-042C-17A0-4\n7,5 kW · 17 A · STO"),
             (17.6, 4.2, 2.1, "M1 – motor 5,5 kW, 6 cực\nM3AA 132ME 6\n+ YB phanh BFK458-12E\n+ BG1 encoder 1024 xung")]
    for x, w, h, t in specs:
        box(ax, x, y1, w, h, t)
    for (xa, wa, *_), (xb, wb, *_) in zip(specs[:-1], specs[1:]):
        yy = y1 + 0.3 if xb > 15 else y1
        arrow(ax, (xa + wa / 2, yy), (xb - wb / 2, yy), lw=1.8)
    label(ax, 5.3, y1 - 1.0, "cáp vào 4×4 mm²", size=7.2, bg=False)
    label(ax, 14.8, y1 + 0.75, "3×2,5+PE\nmàn chắn", size=7.0, bg=False)
    arrow(ax, (15.5, y1 - 0.45), (14.1, y1 - 0.45), color=CTRL, lw=1.3)
    label(ax, 14.8, y1 - 0.85, "A/B/Z HTL", color=CTRL, size=7.0, bg=False)
    box(ax, 12.4, 7.7, 2.5, 1.1, "R1 – điện trở hãm\n39 Ω (32–54 Ω)", size=7.8)
    arrow(ax, (12.4, y1 - 0.85), (12.4, 8.25), lw=1.4)
    label(ax, 13.3, 8.95, "chopper\ntích hợp", size=7.2, bg=False)
    box(ax, 17.6, 7.7, 3.6, 1.1, "Hộp giảm tốc\ni = 100, η = 0,96")
    box(ax, 17.6, 5.7, 3.6, 1.1, "Bánh xe D = 250 mm\nxe con trên ray")
    arrow(ax, (17.6, y1 - 1.05), (17.6, 8.25), lw=1.8)
    arrow(ax, (17.6, 7.15), (17.6, 6.25), lw=1.8)
    box(ax, 8.0, 6.0, 4.4, 1.5, "PLC S7-1200 CPU 1214C\nS-curve · lưu đồ S0–S8\nliên khóa · mã lỗi", fill=FILL_C)
    box(ax, 3.0, 6.0, 3.6, 1.2, "HMI KTP700 Basic\ntrạng thái · tốc độ · lỗi", fill=FILL_C)
    arrow(ax, (4.8, 6.0), (5.8, 6.0), color=CTRL, style="<|-|>")
    box(ax, 3.0, 3.5, 4.0, 2.0, "Đầu vào PLC\nFWD, REV, STOP, RESET\nSQ1/SQ2 hành trình L/R\nphanh mở/đóng, LOAD_OK\nK1, SAFETY_OK", fill="white", size=8.4)
    poly(ax, [(5.0, 3.5), (7.0, 3.5), (7.0, 5.25)], color=CTRL, lw=1.3)
    poly(ax, [(10.2, 6.4), (10.85, 6.4), (10.85, y1 - 0.85)], color=CTRL, lw=1.3)
    arrow(ax, (10.85, 5.7), (10.2, 5.7), color=CTRL, lw=1.3)
    ax.plot([10.85, 10.85], [5.7, 6.4], color=CTRL, lw=1.3, zorder=1)
    label(ax, 10.5, 8.0, "PROFINET", color=CTRL, size=7.4, rot=90, bg=False)
    box(ax, 8.0, 1.2, 5.4, 1.5, "KS – rơ-le an toàn PNOZ s4\nE-stop 2NC (XB5AS8444)\ncực hạn SQ3/SQ4 (D4N)", fill=FILL_S, edge=SAFE)
    arrow(ax, (9.0, 1.95), (9.0, 5.25), color=SAFE, lw=1.2)
    label(ax, 9.75, 4.0, "SAFETY_OK", color=SAFE, size=7.2, bg=False)
    poly(ax, [(10.7, 1.4), (13.9, 1.4), (13.9, y1 - 0.85)], color=SAFE, lw=1.5)
    label(ax, 13.9, 4.2, "STO S1/S2\n(2 kênh)", color=SAFE, size=7.4)
    poly(ax, [(10.7, 0.8), (20.2, 0.8), (20.2, 9.9), (19.7, 9.9)], color=SAFE, lw=1.5)
    label(ax, 20.2, 3.6, "KB – cắt điện phanh", color=SAFE, size=7.4, rot=90)
    poly(ax, [(5.3, 1.2), (0.45, 1.2), (0.45, 8.9), (8.8, 8.9), (8.8, y1 - 0.7)], color=SAFE, lw=1.5)
    label(ax, 2.6, 8.9, "cuộn K1", color=SAFE, size=7.4)
    for j, (c, t) in enumerate(((INK, "Động lực / cơ khí"), (CTRL, "Điều khiển, đo lường"),
                                (SAFE, "Nhánh an toàn độc lập"))):
        x0 = 0.3 + j * 5.2
        ax.plot([x0, x0 + 0.8], [12.7, 12.7], color=c, lw=2.2)
        ax.text(x0 + 1.0, 12.7, t, va="center", fontsize=8.2)
    fig.tight_layout(); fig.savefig(OUT / "rev_hardware.png", dpi=190); plt.close(fig)


# ---------------------------------------------------------------- Hinh 3: FOC
def foc():
    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    ax.set(xlim=(0, 20.4), ylim=(0, 11.2)); ax.axis("off")

    def sumj(x, y):
        ax.add_patch(plt.Circle((x, y), 0.28, facecolor="white", edgecolor=INK, lw=1.1, zorder=3))
        ax.text(x, y, "Σ", ha="center", va="center", fontsize=9, zorder=4)
    yq, yd = 8.2, 5.2
    box(ax, 1.3, yq, 2.2, 1.4, "PLC\nS-curve v*(t)\na ≤ 0,5; j ≤ 2", fill=FILL_C, size=8.5)
    box(ax, 3.9, yq, 1.6, 1.0, "× 2i/D\n→ ω*", size=8.5)
    arrow(ax, (2.4, yq), (3.1, yq)); arrow(ax, (4.7, yq), (5.32, yq))
    sumj(5.6, yq)
    box(ax, 7.3, yq, 2.4, 1.4, "PI tốc độ\ngiới hạn\n|M*| ≤ 47,9 N·m", size=8.5)
    arrow(ax, (5.88, yq), (6.1, yq)); arrow(ax, (8.5, yq), (9.42, yq))
    label(ax, 8.95, yq + 0.5, "i_sq*", size=8, bg=False)
    sumj(9.7, yq)
    box(ax, 11.3, yq, 2.0, 1.1, "PI dòng q\n(mô-men)", size=8.5)
    arrow(ax, (9.98, yq), (10.3, yq))
    box(ax, 1.3, yd, 2.2, 1.1, "Từ thông\nđặt ψ_r*", size=8.5)
    box(ax, 3.9, yd, 1.6, 1.0, "÷ L_m\n→ i_sd*", size=8.5)
    arrow(ax, (2.4, yd), (3.1, yd)); arrow(ax, (4.7, yd), (9.42, yd))
    sumj(9.7, yd)
    box(ax, 11.3, yd, 2.0, 1.1, "PI dòng d\n(từ thông)", size=8.5)
    arrow(ax, (9.98, yd), (10.3, yd))
    box(ax, 14.0, 6.7, 1.8, 4.0, "dq → αβ\n(θ_s)", size=8.5)
    arrow(ax, (12.3, yq), (13.1, yq)); label(ax, 12.7, yq + 0.32, "u_sq*", size=7.6, bg=False)
    arrow(ax, (12.3, yd), (13.1, yd)); label(ax, 12.7, yd + 0.32, "u_sd*", size=7.6, bg=False)
    box(ax, 16.3, 6.7, 1.8, 1.2, "SVPWM", size=9)
    arrow(ax, (14.9, 6.7), (15.4, 6.7))
    box(ax, 18.8, 6.7, 2.6, 2.4, "Nghịch lưu\n3 pha IGBT\nDC bus + chopper\nSTO", size=8.5)
    arrow(ax, (17.2, 6.7), (17.5, 6.7))
    box(ax, 18.8, 2.9, 2.6, 1.6, "Motor KĐB\n5,5 kW\n+ hộp số + bánh", size=8.5)
    arrow(ax, (18.8, 5.5), (18.8, 3.7), lw=1.8)
    box(ax, 14.0, 2.9, 2.9, 1.3, "Đo dòng i_a, i_b\nabc → αβ → dq", size=8.5, fill=FILL_C)
    arrow(ax, (17.5, 2.9), (15.45, 2.9), color=CTRL)
    box(ax, 14.0, 0.9, 2.9, 1.1, "Encoder 1024 xung\nBTAC-02 → ω", size=8.5, fill=FILL_C)
    poly(ax, [(18.8, 2.1), (18.8, 0.9), (15.45, 0.9)], color=CTRL)
    poly(ax, [(12.55, 3.1), (9.7, 3.1), (9.7, yd - 0.28)], color=CTRL)
    label(ax, 11.4, 3.4, "i_sd", color=CTRL, size=8, bg=False)
    poly(ax, [(12.55, 2.7), (8.9, 2.7), (8.9, 7.0), (9.7, 7.0), (9.7, yq - 0.28)], color=CTRL)
    label(ax, 8.55, 4.0, "i_sq", color=CTRL, size=8, bg=False)
    poly(ax, [(12.55, 0.9), (5.6, 0.9), (5.6, yq - 0.28)], color=CTRL)
    label(ax, 5.25, 3.0, "ω", color=CTRL, size=9, bg=False)
    ax.add_patch(FancyBboxPatch((9.05, 4.35), 3.55, 4.75, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="none", edgecolor=CTRL, lw=1, ls="--", zorder=0))
    label(ax, 10.85, 9.35, "Mạch vòng dòng (trong)", color=CTRL, size=7.8, bg=False)
    ax.add_patch(FancyBboxPatch((5.1, 7.25), 3.65, 1.9, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="none", edgecolor=CTRL, lw=1, ls="--", zorder=0))
    label(ax, 6.9, 9.35, "Mạch vòng tốc độ (ngoài)", color=CTRL, size=7.8, bg=False)
    box(ax, 17.4, 10.0, 5.6, 1.3, "Mô hình từ thông rotor (trong VFD)\nω_sl = i_sq/(T_r·i_sd);  θ_s = ∫(p·ω + ω_sl)dt\ncấp θ_s cho các khối đổi tọa độ", fill="white", size=8)
    fig.tight_layout(); fig.savefig(OUT / "rev_foc.png", dpi=190); plt.close(fig)


# ---------------------------------------------------------------- Hinh 4: luu do trang thai
def states():
    fig, ax = plt.subplots(figsize=(9.6, 9.9))
    ax.set(xlim=(0, 19.2), ylim=(1.2, 21.0)); ax.axis("off")
    X, W, Hb = 5.6, 5.6, 1.45
    ys = [19.3, 16.6, 13.9, 11.2, 8.5, 5.8, 3.1]
    names = ["S0  KHÓA KHỞI ĐỘNG\nSTO, phanh đóng, chờ Reset",
             "S1  SẴN SÀNG\nPhanh đóng, mô-men = 0",
             "S2  TẠO MÔ-MEN\nBỏ STO, từ hóa, ω* = 0",
             "S3  MỞ PHANH\nGiữ 0 tốc độ, chờ BRAKE_OPEN",
             "S4  CHẠY TIẾN / LÙI\nBám S-curve, giám sát liên tục",
             "S5  GIẢM TỐC\nS-curve về 0 (≤ 10 s)",
             "S6  ĐÓNG PHANH\nGiữ 0 tốc độ, chờ BRAKE_CLOSED"]
    for y, t in zip(ys, names):
        box(ax, X, y, W, Hb, t, size=9.5)
    conds = ["Tự kiểm tra OK + SAFETY_OK\n+ RESET↑ + lệnh chạy đã nhả",
             "Lệnh mới FWD⊕REV↑\n+ PERMIT + DIR_OK",
             "TORQUE_READY\n(≤ 1,0 s)",
             "BRAKE_OPEN\n(≤ 0,5 s)",
             "STOP / nhả nút / giới hạn\nvận hành / lỗi còn điều khiển",
             "ZERO_SPEED ổn định 0,2 s\n(≤ 12 s)"]
    for (ya, yb), c in zip(zip(ys[:-1], ys[1:]), conds):
        arrow(ax, (X, ya - Hb / 2), (X, yb + Hb / 2), lw=1.4)
        ax.text(X + 0.25, (ya + yb) / 2, c, fontsize=8.2, va="center", ha="left")
    poly(ax, [(X - W / 2, ys[6]), (0.5, ys[6]), (0.5, ys[1]), (X - W / 2, ys[1])], lw=1.4)
    label(ax, 0.5, 10.4, "BRAKE_CLOSED (≤ 0,5 s), không có lỗi chờ", rot=90, size=8.0)
    poly(ax, [(X - W / 2, ys[2] + 0.3), (2.2, ys[2] + 0.3), (2.2, ys[1] - 0.3), (X - W / 2, ys[1] - 0.3)],
         lw=1.1, ls="--")
    label(ax, 2.2, 15.25, "nhả lệnh\n→ hủy", size=7.4)
    poly(ax, [(X - W / 2, ys[3] - 0.3), (2.35, ys[3] - 0.3), (2.35, ys[6] + 0.3), (X - W / 2, ys[6] + 0.3)],
         lw=1.1, ls="--")
    label(ax, 1.45, 7.15, "nhả lệnh /\nmất PERMIT /\ntimeout\nBRAKE_OPEN\n→ đóng phanh", size=7.2)
    XR = 15.0
    box(ax, XR, 13.9, 5.6, 2.2, "S7  LỖI ĐÃ CHỐT\nSTO, phanh đóng, cấm chạy\nLưu và hiển thị mã lỗi",
        fill=FILL_S, edge=SAFE, size=9.5)
    box(ax, XR, 8.5, 5.6, 2.3, "S8  DỪNG KHẨN / BẢO VỆ\nSTO 2 kênh + cắt điện phanh\n+ mở K1 (mạch PNOZ độc lập)",
        fill=FILL_S, edge=SAFE, size=9.5)
    box(ax, XR, 4.7, 5.8, 2.2, "TỪ MỌI TRẠNG THÁI S0–S7\nE-stop · cực hạn · mạch an toàn lỗi\n"
        "VFD trip · mất encoder · mất nguồn\nquá tốc > 120 % · timeout S5", fill="white", edge=SAFE, size=8.6)
    arrow(ax, (XR, 5.8), (XR, 7.35), color=SAFE, lw=1.7)
    arrow(ax, (XR, 9.65), (XR, 12.8), color=SAFE, lw=1.4)
    ax.text(XR + 0.25, 11.2, "đứng yên\n+ chốt lỗi", color=SAFE, fontsize=7.8, va="center")
    poly(ax, [(X + W / 2, ys[2] + 0.3), (XR - 2.8, ys[2] + 0.3)], color=SAFE, lw=1.3)
    label(ax, 10.3, ys[2] + 0.75, "timeout TORQUE_READY", color=SAFE, size=7.8, bg=False)
    poly(ax, [(X + W / 2, ys[6] - 0.3), (18.75, ys[6] - 0.3), (18.75, 13.9), (XR + 2.8, 13.9)],
         color=SAFE, lw=1.3)
    label(ax, 13.2, ys[6] - 0.7, "có lỗi chờ chốt hoặc timeout BRAKE_CLOSED", color=SAFE, size=7.8, bg=False)
    poly(ax, [(XR, 15.0), (XR, ys[0]), (X + W / 2, ys[0])], color=SAFE, lw=1.4)
    label(ax, 11.6, ys[0] + 0.55, "nguyên nhân đã hết + SAFETY_OK\n(tự động; Reset thực hiện ở S0)",
          color=SAFE, size=7.8, bg=False)
    ax.text(0.2, 20.6, "Mũi tên liền: chuyển trạng thái chính · nét đứt: hủy khởi động · màu đỏ: nhánh lỗi/an toàn",
            fontsize=8, color=INK)
    fig.tight_layout()
    fig.savefig(OUT / "rev_states.png", dpi=190)
    fig.savefig(OUT / "Luu_do_trang_thai.svg")
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hardware(); foc(); states()
    print("ok")
