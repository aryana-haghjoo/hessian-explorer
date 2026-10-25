"""Animate how the Hessian's eigenvalues set the local shape of a surface.

f(x, y) = 1/2 [x y] H [x y]^T with H = R(theta) diag(l1, l2) R(theta)^T.
The eigenvalues (l1, l2) move through bowl -> saddle -> dome -> saddle -> flat
valley -> bowl, holding on each so the numbers can be read.

Usage:  python3 hessian_movie.py [out.gif]
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

FPS = 20
HOLD = 40      # frames held on each keyframe
MOVE = 36      # frames spent morphing between keyframes

# (l1, l2, theta in degrees)
KEYS = [
    (2.0, 1.2, 0),
    (2.0, -1.6, 20),
    (-1.8, -1.2, 35),
    (-1.6, 2.0, 50),
    (1.8, 0.0, 30),
    (2.0, 1.2, 0),
]

POS, NEG = "#d1495b", "#2e86ab"   # curvature up / curvature down
FLAT = "#7a7a7a"


def classify(l1, l2, tol=0.08):
    if abs(l1) < tol or abs(l2) < tol:
        return "degenerate (flat direction)", "test inconclusive"
    if l1 > 0 and l2 > 0:
        return "BOWL  (both λ > 0)", "local minimum: a valley"
    if l1 < 0 and l2 < 0:
        return "DOME  (both λ < 0)", "local maximum: a peak"
    return "SADDLE  (mixed signs)", "neither: a mountain pass"


def smooth(t):
    return t * t * (3 - 2 * t)


def schedule():
    """Per-frame (l1, l2, theta) with holds and smooth transitions."""
    out = []
    for a, b in zip(KEYS[:-1], KEYS[1:]):
        out += [a] * HOLD
        for i in range(MOVE):
            s = smooth(i / MOVE)
            out.append(tuple(pa + s * (pb - pa) for pa, pb in zip(a, b)))
    out += [KEYS[-1]] * HOLD
    return out


FRAMES = schedule()
# circular domain so the surface edge doesn't depend on rotation
rr, tt = np.meshgrid(np.linspace(0, 1.5, 22), np.linspace(0, 2 * np.pi, 61))
X, Y = rr * np.cos(tt), rr * np.sin(tt)
probe = np.array([0.9, -0.6])      # point where we draw the gradient

fig = plt.figure(figsize=(12, 6.2), dpi=90, facecolor="white")
ax3 = fig.add_axes([0.0, 0.02, 0.56, 0.92], projection="3d",
                   computed_zorder=False)
axl = fig.add_axes([0.62, 0.10, 0.33, 0.42])
axt = fig.add_axes([0.58, 0.56, 0.40, 0.40])
axt.axis("off")
fig.suptitle("The Hessian  H = J(∇f)  —  its eigenvalues decide the shape",
             fontsize=15, fontweight="bold", y=0.985)


def color_of(lam):
    return FLAT if abs(lam) < 0.08 else (POS if lam > 0 else NEG)


def draw(k):
    l1, l2, th = FRAMES[k]
    t = np.radians(th)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    H = R @ np.diag([l1, l2]) @ R.T
    Z = 0.5 * (H[0, 0] * X**2 + 2 * H[0, 1] * X * Y + H[1, 1] * Y**2)

    # ---- 3D surface -------------------------------------------------------
    ax3.cla()
    ax3.plot_surface(X, Y, Z, cmap="coolwarm", vmin=-2.5, vmax=2.5,
                     rstride=1, cstride=1, linewidth=0.15,
                     edgecolor=(0, 0, 0, 0.15), alpha=0.75, antialiased=True,
                     zorder=1)
    ax3.contour(X, Y, Z, levels=12, zdir="z", offset=-3, cmap="coolwarm",
                vmin=-2.5, vmax=2.5, linewidths=0.8, zorder=0)
    # principal-curvature curves along each eigenvector
    s = np.linspace(-1.5, 1.5, 60)
    for vec, lam, name in ((R[:, 0], l1, "v₁"), (R[:, 1], l2, "v₂")):
        px, py = s * vec[0], s * vec[1]
        ax3.plot(px, py, 0.5 * lam * s**2, color=color_of(lam), lw=3.2,
                 zorder=10)
        ax3.plot([0, 1.4 * vec[0]], [0, 1.4 * vec[1]], [-3, -3],
                 color=color_of(lam), lw=2.5)
        ax3.text(1.6 * vec[0], 1.6 * vec[1], -3, name, color=color_of(lam),
                 fontsize=12, fontweight="bold")
    # gradient at a probe point, drawn in the floor plane: "which way is uphill"
    grad = H @ probe
    zp = 0.5 * probe @ H @ probe
    ax3.scatter(*probe, zp, color="k", s=25, zorder=11)
    gn = grad / (np.linalg.norm(grad) + 1e-9) * 0.6
    ax3.quiver(probe[0], probe[1], -3, gn[0], gn[1], 0, color="k",
               lw=2, arrow_length_ratio=0.3)
    ax3.text(probe[0] + gn[0], probe[1] + gn[1], -3, " ∇f (uphill)",
             fontsize=9)
    ax3.scatter(0, 0, 0, color="gold", edgecolor="k", s=70, zorder=12)
    ax3.set_xlim(-1.5, 1.5); ax3.set_ylim(-1.5, 1.5); ax3.set_zlim(-3, 3)
    ax3.text(0, 0, 0.35, "critical point", fontsize=9, ha="center", zorder=13)
    ax3.set_xlabel("x"); ax3.set_ylabel("y"); ax3.set_zlabel("f")
    ax3.view_init(elev=24, azim=-60 + 0.25 * k)
    ax3.set_box_aspect((1, 1, 0.8))

    # ---- text panel: H, eigenvalues, verdict -----------------------------
    axt.cla(); axt.axis("off")
    shape, verdict = classify(l1, l2)
    axt.text(0.0, 0.92, "Hessian at the critical point (gold):",
             fontsize=12, transform=axt.transAxes)
    axt.text(0.05, 0.62,
             f"H = ⎡ {H[0,0]:+5.2f}   {H[0,1]:+5.2f} ⎤\n"
             f"    ⎣ {H[1,0]:+5.2f}   {H[1,1]:+5.2f} ⎦",
             family="DejaVu Sans Mono", fontsize=13, transform=axt.transAxes,
             va="center")
    axt.text(0.0, 0.36, f"λ₁ = {l1:+.2f}", color=color_of(l1), fontsize=14,
             fontweight="bold", transform=axt.transAxes)
    axt.text(0.40, 0.36, f"λ₂ = {l2:+.2f}", color=color_of(l2), fontsize=14,
             fontweight="bold", transform=axt.transAxes)
    axt.text(0.0, 0.16, shape, fontsize=15, fontweight="bold",
             transform=axt.transAxes)
    axt.text(0.0, 0.02, verdict, fontsize=12, style="italic",
             transform=axt.transAxes)

    # ---- eigenvalue plane ------------------------------------------------
    axl.cla()
    lim = 2.5
    axl.fill_between([0, lim], 0, lim, color=POS, alpha=0.12)
    axl.fill_between([-lim, 0], -lim, 0, color=NEG, alpha=0.12)
    axl.fill_between([-lim, 0], 0, lim, color="#999", alpha=0.10)
    axl.fill_between([0, lim], -lim, 0, color="#999", alpha=0.10)
    for (x, y, lab) in ((1.25, 1.25, "bowl\n(min)"), (-1.25, -1.25, "dome\n(max)"),
                        (-1.25, 1.25, "saddle"), (1.25, -1.25, "saddle")):
        axl.text(x, y, lab, ha="center", va="center", fontsize=10, color="#444")
    axl.axhline(0, color="k", lw=0.8); axl.axvline(0, color="k", lw=0.8)
    trail = np.array([f[:2] for f in FRAMES[:k + 1]])
    axl.plot(trail[:, 0], trail[:, 1], color="#555", lw=1, alpha=0.5)
    axl.scatter([l1], [l2], s=90, color="gold", edgecolor="k", zorder=5)
    axl.set_xlim(-lim, lim); axl.set_ylim(-lim, lim); axl.set_aspect("equal")
    axl.set_xlabel("λ₁"); axl.set_ylabel("λ₂")
    axl.set_title("eigenvalue plane", fontsize=11)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "hessian_movie.gif"
    anim = FuncAnimation(fig, draw, frames=len(FRAMES))
    anim.save(out, writer=PillowWriter(fps=FPS))
    print(f"wrote {out}  ({len(FRAMES)} frames, {len(FRAMES)/FPS:.1f}s)")
