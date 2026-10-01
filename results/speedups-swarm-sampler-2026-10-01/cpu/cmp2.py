import json, sys, os, numpy as np
os.chdir(sys.argv[1]); ref = np.load("base/dead.npz")
for t in sorted(os.listdir(".")):
    if not os.path.exists(f"{t}/summary.json") or t.startswith("adapter") or "trace" in t: continue
    d = json.load(open(f"{t}/summary.json")); b = np.load(f"{t}/dead.npz")
    same = all(np.array_equal(ref[k], b[k], equal_nan=True) for k in ref.files)
    print(f"{t:10s} it {d['iterations']} logZ {d['logZ']!r} calls {d['n_likelihood_calls']} sampling {d['sampling_s']:.1f} first {d['first_iteration_s']:.1f} later {d['later_iterations_s']:.1f} bitwise {same}")
ref = np.load("adapter-base/samples.npz")
for t in sorted(os.listdir(".")):
    if not t.startswith("adapter") or t == "adapter-base": continue
    d, b = json.load(open(f"{t}/summary.json")), np.load(f"{t}/samples.npz")
    same = all(np.array_equal(ref[k], b[k]) for k in ref.files)
    print(f"{t:18s} run {d['run_s']:.1f} sampling wall {d['wall_time_s']:.1f} logZ {d['logZ']!r} calls {d['n_likelihood_calls']} samples bitwise {same}")
