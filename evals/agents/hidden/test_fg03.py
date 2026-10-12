import re

from _phot import figure


def test_flux_axis_states_microjansky_and_no_bare_scale():
    fig, ax, _ = figure()
    label = ax.get_ylabel()
    assert re.search(r"\\mu\$?\s*\\?\s*\{?\s*\\?mathrm\{?Jy|\\mu\$\s*Jy|µJy|μJy|uJy|microjansky", label, re.I), label
    assert not re.search(r"10\^|10\$\^|cgs|1e-", label), label
    assert ax.yaxis.get_offset_text().get_text() == ""
