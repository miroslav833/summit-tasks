# Survival function of the Weibull service time on log-log axes, 1-2-5 grid on the vertical axis.
import math, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
t1, S1, t2, S2 = 2.5, 0.5, 10.0, 0.002
beta = math.log(math.log(1/S2) / math.log(1/S1)) / math.log(t2/t1)
eta = t1 / math.log(1/S1)**(1/beta)
t = np.logspace(0, math.log10(15), 900); S = np.exp(-(t/eta)**beta)
fig, ax = plt.subplots(figsize=(6.0, 5.2), dpi=300)
ax.loglog(t, S, "-", color="0.1", lw=1.3)
ax.set_xlim(1, 15); ax.set_ylim(1e-4, 1)
xt = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 10, 12, 15]
ax.set_xticks(xt); ax.set_xticklabels([f"{v:g}" for v in xt])
ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10, subs=(2.0, 5.0), numticks=12))
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.grid(True, which="major", color="0.55", lw=0.7); ax.grid(True, which="minor", color="0.78", lw=0.5)
ax.set_xlabel("service time $t$"); ax.set_ylabel("$P(S > t)$")
fig.tight_layout(); fig.savefig("image.png"); fig.savefig("image.pdf")
print(f"saved; beta = {beta:.5f}, eta = {eta:.5f}")
