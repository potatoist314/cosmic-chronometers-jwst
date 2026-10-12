from matplotlib.mathtext import MathTextParser

import plot_prior_kl as kl


def test_noll_parameters_have_latex_labels():
    parser = MathTextParser("agg")
    for name in ("diffuse_tau_noll", "diffuse_delta", "diffuse_Ebump"):
        label = kl.LABELS[name]
        assert label.count("$") >= 2, label
        parser.parse(label)
