"""Cross-agent contracts: what one agent WRITES is what another READS.

Each agent's own tests use fixtures it wrote itself, which is how
`jarvis daily` spent weeks reading an `overall_status:` key that Wall-E
never writes. These tests feed each real writer's output to the real
reader, and check constants that two agents must agree on.

Needs the sibling agents installed (bootstrap does that); any agent that
isn't importable is skipped, not failed.
"""
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

NEIL = Path(__file__).resolve().parents[2]
ALFRED_API = NEIL / "alfred" / "apps" / "api"
if ALFRED_API.is_dir() and str(ALFRED_API) not in sys.path:
    sys.path.insert(0, str(ALFRED_API))


def _mod(name):
    return pytest.importorskip(name)


def _vault(tmp_path, monkeypatch):
    monkeypatch.setenv("VAULT_PATH", str(tmp_path))
    return tmp_path


# --- vault notes: writer -> reader ------------------------------------------

def test_wall_e_report_is_read_by_jarvis_daily(tmp_path):
    report_mod = _mod("walle.report")
    from walle.audit_review import summarize_audit
    from walle.contract_check import check_agent_yamls
    from walle.health_aggregation import summarize_health
    from walle.resource_check import check_sibling_repos
    briefing = _mod("jarvis.vault_briefing")

    health = summarize_health({"reachable": True, "agents": {"friday": {"healthy": True}}, "jarvis": {"healthy": True}})
    audit, contract, resources = summarize_audit([]), check_agent_yamls({}), check_sibling_repos({})
    setup = {"models": {"required": ["m"], "missing": ["m"], "error": None}, "sandbox_image": {}, "schedules": {}, "guard_hooks": {}}
    report = {
        "wall_e_version": "contract", "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_status": report_mod._overall_status(health, audit, contract, resources, setup),
        "status_reasons": report_mod.status_reasons(health, audit, contract, resources, setup),
        "agent_health": health, "privacy_audit": audit, "contract_compliance": contract,
        "resources": resources, "setup": None,
    }
    report_mod.write_report(report, tmp_path / "agents" / "Wall-E")

    got = briefing.vault_briefing(str(tmp_path))["wall_e"]
    assert got["overall_status"] == "degraded"
    assert got["reasons"] == report["status_reasons"] and got["reasons"]


def test_alfred_progress_note_is_read_by_jarvis_daily(tmp_path, monkeypatch):
    vault = _mod("alfred.vault")
    config = _mod("alfred.config")
    briefing = _mod("jarvis.vault_briefing")
    _vault(tmp_path, monkeypatch)
    today = datetime.date(2026, 11, 3)
    vault.write_progress_note(config.Settings(), user_handle="me", archetype="quiz redis",
                              streak_days=0, mastery=0.5, next_due=today + datetime.timedelta(days=1))
    due = briefing.vault_briefing(str(tmp_path), today=today)["alfred_reviews_due"]
    assert due == [{"topic": "quiz redis", "next_due": "2026-11-04"}]


def test_ultron_pending_finding_is_counted_by_jarvis_daily(tmp_path):
    uvault = _mod("ultron.vault")
    briefing = _mod("jarvis.vault_briefing")
    uvault.write_finding("Hard-coded key", "body", vault_root=str(tmp_path / "agents" / "Ultron"))
    assert briefing.vault_briefing(str(tmp_path))["ultron_pending_review"] == 1


def test_friday_draft_appears_in_friday_calendar(tmp_path):
    drafts = _mod("friday.drafts")
    cc = _mod("friday.content_calendar")
    drafts.write_draft(tmp_path, "blog", "Hash Rings", "body", "n.md")
    assert [p.platform for p in cc.load_posts(tmp_path)] == ["blog"]


# --- shared constants --------------------------------------------------------

def test_tars_guard_hook_is_recognised_by_wall_e(tmp_path, monkeypatch):
    guard = _mod("tars.guard")
    setup = _mod("walle.setup_check")
    assert guard.HOOK_MARKER == setup.GUARD_MARKER
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    monkeypatch.setenv("TARS_ALLOWED_ROOTS", str(tmp_path))
    guard.install_hook(repo)
    assert setup.check_guard_hooks({"repo": repo}) == {"repo": True}


def test_wall_e_checks_the_image_ultron_builds():
    sandbox = _mod("ultron.sandbox")
    setup = _mod("walle.setup_check")
    assert setup.SANDBOX_IMAGE == sandbox.IMAGE


def test_wall_e_requires_only_models_bootstrap_pulls():
    setup = _mod("walle.setup_check")
    manifest = yaml.safe_load((Path(__file__).resolve().parents[1] / "bootstrap" / "agents.yaml").read_text(encoding="utf-8"))
    assert set(setup.REQUIRED_MODELS) <= set(manifest["models"])


def test_scheduled_jobs_name_real_cli_commands():
    schedule = _mod("walle.schedule")
    clis = {"wall-e": "walle.cli", "friday": "friday.cli"}
    for job in schedule.JOBS.values():
        cli = _mod(clis[job.exe]).cli
        assert job.args.split()[0] in cli.commands, f"{job.exe} has no '{job.args}' command"
