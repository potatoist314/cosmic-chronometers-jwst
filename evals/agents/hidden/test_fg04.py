import matplotlib

from _kl import run


def test_kl_png_resolution_matches_other_figures(monkeypatch, tmp_path):
    saved = run(monkeypatch, tmp_path)
    assert saved
    dpi = saved[0][1].get("dpi", matplotlib.rcParams["savefig.dpi"])
    if dpi == "figure":
        dpi = saved[0][0].dpi
    assert float(dpi) >= 110
