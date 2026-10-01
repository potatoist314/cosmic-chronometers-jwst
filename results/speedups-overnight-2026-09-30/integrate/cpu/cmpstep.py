import sys, numpy as np
a, b = np.load(sys.argv[1]), np.load(sys.argv[2]); step = int(sys.argv[3])
x, y = a["loglikelihood"][::step], b["loglikelihood"]
print(sys.argv[2].split("/")[-1], "n", y.size, "bitwise equal", int((x.view(np.int64) == y.view(np.int64)).sum()), "max |d|", float(np.max(np.abs(x - y))))
