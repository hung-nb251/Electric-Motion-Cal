"""Tinh toan bo sung cho ban sua bao cao x = 2 (phan cung, ham, phanh, bao ve).

Moi so lieu dau vao lay tu sheet Tinh_toan_x2 cua bang tinh va catalog hang da tra cuu.
"""
import math
import numpy as np

# ---- Dau vao theo bang tinh (x = 2) ----
Q, mh = 12222.0, 222.0
m1, m0 = Q + mh, mh
v, D, i, mu, eta, g, k = 0.12, 0.25, 100.0, 0.2, 0.96, 9.81, 1.2
r = D / 2
Jr = 0.039                        # rotor M3AA 132ME 6 (sheet x=1)
Pn, nn, Tn, In, cosphi = 5500.0, 973.0, 53.9, 12.0, 0.74
Tmax_ratio = 2.9
wm = 2 * v * i / D                # 96 rad/s
nm = wm * 60 / (2 * math.pi)      # 916.73 rpm
kF = D / (2 * i * eta)            # N -> N·m tai truc motor (truyen thuan)
kJ = Jr * 2 * i / D               # N·m cho moi m/s^2 (quan tinh rotor)
F_env = m1 * (mu * g + 0.5)
M_env = k * (F_env * kF + kJ * 0.5)          # 66.59 N·m
M_traj = 35.04103125                           # Chu_ky!B27
M_fric1 = m1 * mu * g * kF                     # 31.79 N·m
M_fric0 = m0 * mu * g * kF                     # 0.567 N·m
Tw_k = k * F_env * r                           # 4595.57 N·m dau ra hop so co du tru

# ---- Bien tan ABB ACS380-04xx-17A0-4 (catalog ACS380) ----
VFD = dict(PN=7.5, IN=17.0, ILd=16.2, IHd=12.6, PHd=5.5, Imax=22.7,
           Rmin=32.0, Rmax=54.0, PBRcont=5.5, PBRmax=8.25, fuse_gG=32)

sinphi = math.sqrt(1 - cosphi ** 2)
Id, Iq_n = In * sinphi, In * cosphi
def I_for(T):
    """Uoc tinh dong stator khi tu thong dinh muc: I = sqrt(Id^2 + (Iq_n T/Tn)^2)."""
    return math.hypot(Id, Iq_n * T / Tn)

T_lim = Tw_k / (i * eta)                       # = 47.87 N·m: bao ve hop so
a_max_Tlim = (T_lim - M_fric1) / (kJ + m1 * kF)

# ---- Hai tai sinh: mo phong so ----
def regen_stop(m, T, tj=None):
    tj = T / 2 if tj is None else tj
    ap = v / (T - tj); jp = ap / tj
    t = np.linspace(0, T, 200001)
    a = np.where(t < tj, jp * t, np.where(t < T - tj, ap, jp * (T - t)))
    vv = v - np.concatenate([[0], np.cumsum((a[1:] + a[:-1]) / 2 * np.diff(t))])
    M = m * (mu * g - a) * kF - kJ * a
    P = M * vv * i / r
    return ap, jp, float(P.min()), float(np.trapezoid(np.minimum(P, 0), t))

reg_cycle = regen_stop(m0, 5.0, 0.25)          # giam toc khong tai theo chu ky
T_fast = 2 * math.sqrt(v / 2.0)                 # nhanh nhat voi j = 2 -> 0.4899 s
reg_fast = regen_stop(m0, T_fast * 1.0001)
reg_fast_loaded = regen_stop(m1, T_fast * 1.0001)
P_bound = -(kJ * 0.5 - m0 * (mu * g - 0.5) * kF) * wm   # buoc a = 0,5 tai v_max
E_rotor = 0.5 * Jr * wm ** 2
E_k = 0.5 * m1 * v ** 2 + E_rotor
R_h = 39.0

# ---- Phanh INTORQ BFK458-12E, 24 VDC ----
T_b, W_max_brake, t_d = 32.0, 24000.0, 0.10
def brake_decel(m, Tb):
    # J_r*alpha = -(Tb + F_w*kF), F_w = m(mu g + a) (dong cong suat qua hop so van thuan)
    return -(Tb + m * mu * g * kF) / (kJ + m * kF)
stop = {}
for lab, m in (("co_tai", m1), ("khong_tai", m0)):
    a_b = brake_decel(m, T_b); a_c = brake_decel(m, 0.0)
    stop[lab] = dict(a_brake=a_b, t_brake=v / -a_b, s_brake=v * v / (2 * -a_b) + v * t_d,
                     a_coast=a_c, t_coast=v / -a_c, s_coast=v * v / (2 * -a_c) + v * t_d,
                     F_w=m * (mu * g + a_b))
T_gear_brake = stop["co_tai"]["F_w"] * r

# ---- Vi tri cong tac ----
s_op = v * 0.10 + 0.5 * v * 10 + 0.05          # 0.662 m -> 0.70 m
s_final = 0.10                                  # cuc han sau diem dung
s_buffer_min = stop["khong_tai"]["s_coast"] + 0.05
s_buffer = 0.50

# ---- Encoder Autonics E50S8-1024-3-T-24 ----
ppr = 1024
f_enc = nm / 60 * ppr
res_um = math.pi * D / i / (4 * ppr) * 1e6
f_zero = 0.002 * i / (math.pi * D) * ppr

# ---- Nguong bao ve ----
v_os1, v_os2, v_dev = 1.1 * v, 1.2 * v, 0.2 * v
T_S5 = max(10.0, 5.0) + 2.0

# ---- Cap (IEC 60364-5-52, B.52.4, PVC, 3 day mang tai, pp C; he so 40 °C = 0,87) ----
Iz = {2.5: 24.0, 4.0: 32.0}
k40 = 0.87
dU_motor = math.sqrt(3) * In * 25 * (8.89e-3 * cosphi + 0.08e-3 * sinphi)

if __name__ == "__main__":
    print(f"nm={nm:.2f} rpm, wm={wm}, M_env={M_env:.3f}, T_lim={T_lim:.3f}, a_max(T_lim)={a_max_Tlim:.3f}")
    for T in (M_traj, k * M_traj, T_lim, M_env):
        print(f"I({T:.2f}) = {I_for(T):.2f} A")
    print("reg cycle", reg_cycle, "fast", reg_fast, "fast loaded", reg_fast_loaded)
    print(f"P_bound={P_bound:.1f} W, E_rotor={E_rotor:.1f} J, E_k={E_k:.1f} J, T_fast={T_fast:.4f}")
    for lab, d in stop.items():
        print(lab, {k_: round(v_, 4) for k_, v_ in d.items()})
    print(f"T_gear_brake={T_gear_brake:.1f} N·m ; s_op={s_op:.3f}; buffer_min={s_buffer_min:.3f}")
    print(f"enc f={f_enc:.1f} Hz res={res_um:.3f} um f_zero={f_zero:.1f} Hz")
    print(f"Iz 2.5: {Iz[2.5]*k40:.1f} A; 4: {Iz[4.0]*k40:.1f} A; dU motor 25 m = {dU_motor:.2f} V ({dU_motor/4:.2f} %)")
    print(f"overspeed {v_os1:.3f}/{v_os2:.3f} m/s; dev {v_dev:.3f}; T_S5={T_S5}")
    print(f"I_in est (rated motor, lambda 0.6) = {(Pn/0.895+230)/(math.sqrt(3)*400*0.6):.1f} A")
