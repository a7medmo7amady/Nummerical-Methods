import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

def f(x):
    return np.sin(x) + np.cos(1 + x**2) - 1

def df(x):
    return np.cos(x) - 2*x * np.sin(1 + x**2)

ES = 1e-3 

def bisection(a, b, es=ES):
    history, xr_old = [], None
    for i in range(1, 1001):
        xr = (a + b) / 2.0
        ea = abs((xr - xr_old) / xr) * 100 if xr_old else 100.0
        history.append((i, xr, ea))
        if ea < es * 100 and i > 1: break
        a, b = (xr, b) if f(a)*f(xr) > 0 else (a, xr)
        xr_old = xr
    return xr, history

def false_position(a, b, es=ES):
    history, xr_old = [], None
    for i in range(1, 1001):
        xr = b - f(b)*(a - b) / (f(a) - f(b))
        ea = abs((xr - xr_old) / xr) * 100 if xr_old else 100.0
        history.append((i, xr, ea))
        if ea < es * 100 and i > 1: break
        a, b = (xr, b) if f(a)*f(xr) < 0 else (a, xr)
        xr_old = xr
    return xr, history

def newton_raphson(x0, es=ES):
    history, x = [], x0
    for i in range(1, 1001):
        x_new = x - f(x) / df(x)
        ea = abs((x_new - x) / x_new) * 100
        history.append((i, x_new, ea))
        x = x_new
        if ea < es * 100: break
    return x, history

def secant(x0, x1, es=ES):
    history = []
    for i in range(1, 1001):
        x2 = x1 - f(x1)*(x1 - x0) / (f(x1) - f(x0))
        ea = abs((x2 - x1) / x2) * 100
        history.append((i, x2, ea))
        x0, x1 = x1, x2
        if ea < es * 100: break
    return x2, history

a0, b0 = 1.8, 2.0
root_bis, hist_bis = bisection(a0, b0)
root_fp,  hist_fp  = false_position(a0, b0)
root_nr,  hist_nr  = newton_raphson(1.9)
root_sec, hist_sec = secant(1.8, 2.0)

root_scipy = brentq(f, a0, b0, xtol=1e-12)

print(f"{'Method':<20} {'Root':>12} {'Iters':>6}")
for name, r, h in [("Bisection",      root_bis, hist_bis),
                   ("False Position", root_fp,  hist_fp),
                   ("Newton-Raphson", root_nr,  hist_nr),
                   ("Secant",         root_sec, hist_sec),
                   ("SciPy brentq",   root_scipy, None)]:
    n = len(h) if h else "—"
    print(f"{name:<20} {r:>12.8f} {str(n):>6}")

fig, ax = plt.subplots(figsize=(10, 5))
COLORS = {"Bisection":"#4C72B0", "False Position":"#DD8452",
          "Newton-Raphson":"#55A868", "Secant":"#C44E52"}

for name, hist, mk in [("Bisection",      hist_bis, "o"),
                        ("False Position", hist_fp,  "s"),
                        ("Newton-Raphson", hist_nr,  "^"),
                        ("Secant",         hist_sec, "D")]:
    iters  = [h[0] for h in hist]
    errors = [h[2] for h in hist]
    ax.semilogy(iters, errors, marker=mk, label=f"{name} ({len(hist)} iters)",
                color=COLORS[name], lw=2, ms=7)

ax.axhline(ES * 100, color="gold", ls="--", label="εs = 0.1%")
ax.set_xlabel("Iterations"); ax.set_ylabel("Approximate Error εa (%)")
ax.set_title("Convergence Comparison – All Methods")
ax.legend(); ax.grid(True, ls="--", alpha=0.4)
plt.tight_layout()
plt.savefig("graph.png", dpi=150)
plt.show()