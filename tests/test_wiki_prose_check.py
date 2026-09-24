"""Jev review preserves prose selection and fails visibly on service errors."""
import pytest

from scripts import wiki_prose_check as check


def reply_for(body, flagged=None):
    return {"model": check.JEV_MODEL, "answers": {
        key: {"noul": .95 if key == flagged else .05} for key in body["questions"]}}


def test_checks_each_passage_in_one_request(monkeypatch):
    calls = []

    def request(body):
        calls.append(body)
        return reply_for(body, "2_natural_phrasing")

    monkeypatch.setattr(check, "jev_request", request)
    found = [("a:1", "The fit uses thirty bands."), ("b:2", "A seamless and transformative journey.")]
    result = check.ask_jev(found)
    assert len(calls) == 1
    assert len(calls[0]["questions"]) == 6
    assert calls[0]["state"] == {"1": found[0][1], "2": found[1][1]}
    assert result["faults"] == [{"unit": 2, "problem": "natural_phrasing", "probability": .95}]


def test_no_prose_makes_no_request(monkeypatch):
    monkeypatch.delenv("SKIP_PROSE_CHECK", raising=False)
    monkeypatch.setattr(check, "collect", lambda _: [])
    monkeypatch.setattr(check, "jev_request", lambda _: pytest.fail("unexpected API request"))
    assert check.main([]) == 0


@pytest.mark.parametrize("flagged,expected", [(None, 0), ("1_conciseness", 1)])
def test_hook_reports_pass_or_fault(monkeypatch, capsys, flagged, expected):
    monkeypatch.delenv("SKIP_PROSE_CHECK", raising=False)
    monkeypatch.setattr(check, "collect", lambda _: [("wiki/notes/example.md:7", "This is the changed passage.")])
    monkeypatch.setattr(check, "jev_request", lambda body: reply_for(body, flagged))
    assert check.main([]) == expected
    output = capsys.readouterr().err
    if flagged:
        assert "wiki/notes/example.md:7: conciseness" in output
    assert "rewrite:" not in output


@pytest.mark.parametrize("response", [{}, {"answers": {}}, {"answers": {"1_conciseness": {"noul": float("nan")}}}])
def test_invalid_service_response_does_not_pass(monkeypatch, response):
    monkeypatch.delenv("SKIP_PROSE_CHECK", raising=False)
    monkeypatch.setattr(check, "collect", lambda _: [("a:1", "Some prose to check.")])
    monkeypatch.setattr(check, "jev_request", lambda _: response)
    assert check.main([]) == 1


def test_timeout_does_not_pass_or_expose_raw_exception(monkeypatch, capsys):
    def unavailable(_):
        raise TimeoutError("private service details")

    monkeypatch.delenv("SKIP_PROSE_CHECK", raising=False)
    monkeypatch.setattr(check, "collect", lambda _: [("a:1", "Some prose to check.")])
    monkeypatch.setattr(check, "jev_request", unavailable)
    assert check.main([]) == 1
    output = capsys.readouterr().err
    assert "TimeoutError" in output
    assert "private service details" not in output


def test_collect_uses_staged_text_not_worktree(monkeypatch):
    path = "wiki/notes/example.md"
    monkeypatch.setattr(check, "git", lambda *args: path)
    monkeypatch.setattr(check, "version", lambda spec:
                        "Old factual words remain here." if spec.startswith("HEAD:")
                        else "The fit uses thirty bands.")
    assert check.collect(None) == [(path + ":1", "The fit uses thirty bands.")]


def test_code_and_unchanged_prose_are_excluded():
    old = "The fit uses thirty bands.\n"
    new = old + "\n```python\nprint('Do not review this code block')\n```\n"
    assert check.units(old, new, "wiki/notes/example.md", False) == []
