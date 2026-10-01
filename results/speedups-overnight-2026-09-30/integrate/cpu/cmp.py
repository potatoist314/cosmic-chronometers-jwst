import sys, numpy as np
a, b = np.load(sys.argv[1]), np.load(sys.argv[2])
for k in ("loglikelihood", "logprior"):
    x, y = a[k], b[k]
    same = (x.view(np.int64) == y.view(np.int64))
    d = np.abs(x - y)
    print(k, "n", x.size, "bitwise equal", int(same.sum()), "max |d|", float(np.nanmax(d)) if d.size else 0, "median |d|", float(np.median(d)))
print("vs stored: max |d|", float(np.max(np.abs(a["loglikelihood"] - a["stored"]))))
