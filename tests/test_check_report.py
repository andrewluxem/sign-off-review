"""Unit tests for scripts/check_report.py. Run with: python -m unittest"""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "check_report.py")

_spec = importlib.util.spec_from_file_location("check_report", SCRIPT)
check_report = importlib.util.module_from_spec(_spec)
sys.modules["check_report"] = check_report
_spec.loader.exec_module(check_report)


def write(tmp, name, content):
    path = os.path.join(tmp, name)
    mode = "wb" if isinstance(content, bytes) else "w"
    kwargs = {} if isinstance(content, bytes) else {"encoding": "utf-8"}
    with open(path, mode, **kwargs) as handle:
        handle.write(content)
    return path


def run_cli(*args):
    return subprocess.run(
        [sys.executable, SCRIPT] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


class SelftestCasesTest(unittest.TestCase):
    """Every fixture the --selftest uses, checked one by one."""

    def test_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            for i, (name, content, want_code, want_text) in enumerate(check_report.selftest_cases()):
                with self.subTest(case=name):
                    path = os.path.join(tmp, "case-%02d.md" % i)
                    if content is None:
                        os.mkdir(path)
                    else:
                        write(tmp, os.path.basename(path), content)
                    code, messages = check_report.check_file(path)
                    joined = " | ".join(m for _, m in messages)
                    self.assertEqual(code, want_code, joined)
                    self.assertIn(want_text, joined)


class RuleDetailTest(unittest.TestCase):
    def check(self, text):
        return check_report.check_text(text)

    def test_valid_reports_have_no_messages(self):
        for text in (check_report.GOOD_RETURN, check_report.GOOD_RELEASE, check_report.GOOD_REREVIEW):
            self.assertEqual(self.check(text), (0, []))

    def test_violation_reports_its_line_number(self):
        text = check_report.GOOD_RETURN.replace(
            "**In one line:** The saving", "**In one line:** " + check_report.EM_DASH + " The saving")
        code, messages = self.check(text)
        self.assertEqual(code, 1)
        self.assertEqual(messages, [(3, "em dash (U+2014); use a comma, colon, period or parentheses")])

    def test_blocker_line_is_the_finding_row(self):
        text = check_report.GOOD_RETURN.replace("**Verdict:** Return", "**Verdict:** Release")
        code, messages = self.check(text)
        self.assertEqual(code, 1)
        lines = text.splitlines()
        flagged = [line for line, m in messages if "a Blocker is open" in m]
        self.assertEqual(len(flagged), 1)
        self.assertTrue(lines[flagged[0] - 1].startswith("| 1 | Blocker |"))

    def test_both_blocker_and_tie_row_flagged_when_released(self):
        text = check_report.GOOD_RETURN.replace("**Verdict:** Return", "**Verdict:** Release with fixes")
        _, messages = self.check(text)
        joined = " | ".join(m for _, m in messages)
        self.assertIn("a Blocker is open", joined)
        self.assertIn("a number that does not tie", joined)

    def test_majors_alone_do_not_force_return(self):
        text = check_report.GOOD_RELEASE.replace(
            "| 1 | Minor | Logic | Step 4 | Steps 4 and 5 could run in parallel but are listed in sequence. | |",
            "| 1 | Major | Logic | Step 4 | Step 5 needs step 4's output but runs first. | The run fails at step 5. |",
        ).replace("**Verdict:** Release", "**Verdict:** Release with fixes")
        self.assertEqual(self.check(text), (0, []))

    def test_minor_may_leave_consequence_empty(self):
        self.assertEqual(self.check(check_report.GOOD_RELEASE)[0], 0)

    def test_escaped_pipe_stays_inside_cell(self):
        text = check_report.GOOD_RELEASE.replace(
            "Move step 5 beside step 4", "Replace `a \\| b` with `a && b` and move step 5 beside step 4")
        self.assertEqual(self.check(text), (0, []))

    def test_bold_severity_and_verdict_are_accepted(self):
        text = check_report.GOOD_RETURN.replace("| 1 | Blocker |", "| 1 | **Blocker** |").replace(
            "**Verdict:** Return", "**Verdict:** Return.")
        self.assertEqual(self.check(text), (0, []))

    def test_hedge_only_at_start_of_fix(self):
        text = check_report.GOOD_RETURN.replace(
            "Add a downside case with", "Reconsider nothing; add a downside case with")
        self.assertEqual(self.check(text), (0, []))

    def test_hedge_check_ignores_case(self):
        text = check_report.GOOD_RETURN.replace("Add a downside case with", "YOU MAY add a downside case with")
        code, messages = self.check(text)
        self.assertEqual(code, 1)
        self.assertIn("fix starts with 'YOU MAY'", messages[0][1])

    def test_lead_seat_takes_no_persona(self):
        text = check_report.GOOD_RETURN.replace("| Lead |", "| Lead (CFO) |")
        code, messages = self.check(text)
        self.assertEqual(code, 1)
        self.assertIn("takes no persona", messages[0][1])

    def test_seat_without_persona_is_valid_in_every_profile(self):
        for profile in check_report.PROFILES:
            text = check_report.GOOD_RETURN.replace("profile strategy", "profile " + profile).replace(
                "Skeptic (CFO)", "Skeptic").replace("Outsider (non-specialist)", "Outsider")
            with self.subTest(profile=profile):
                self.assertEqual(self.check(text), (0, []))

    def test_each_profile_persona_is_valid_only_in_its_profile(self):
        for profile, personas in check_report.PROFILES.items():
            for seat, persona in personas.items():
                for other in check_report.PROFILES:
                    text = check_report.GOOD_RETURN.replace("profile strategy", "profile " + other).replace(
                        "Outsider (non-specialist)", "Outsider").replace(
                        "Skeptic (CFO)", "%s (%s)" % (seat, persona))
                    want = 0 if check_report.PROFILES[other].get(seat, "").lower() == persona.lower() else 1
                    with self.subTest(profile=profile, seat=seat, other=other):
                        self.assertEqual(self.check(text)[0], want)

    def test_stage_one_allows_decision_logic_and_lead(self):
        text = check_report.GOOD_RELEASE.replace("stage 2", "stage 1").replace(
            "| Minor | Logic |", "| Minor | Decision (owner) |")
        self.assertEqual(self.check(text), (0, []))

    def test_blank_lines_before_header_are_allowed(self):
        self.assertEqual(self.check("\n\n" + check_report.GOOD_RETURN)[0], 0)

    def test_byte_order_mark_is_allowed(self):
        self.assertEqual(self.check("\ufeff" + check_report.GOOD_RETURN)[0], 0)

    def test_premortem_internal_tag_on_continuation_line(self):
        text = check_report.GOOD_RETURN.replace(
            "so the timeline slips. (internal)", "so the timeline slips.\n   (internal)")
        self.assertEqual(self.check(text), (0, []))

    def test_empty_findings_section_is_allowed(self):
        text = check_report.GOOD_RELEASE.replace(
            "| # | Severity | Seat | Where | Problem | Consequence | Fix |\n|---|---|---|---|---|---|---|\n"
            "| 1 | Minor | Logic | Step 4 | Steps 4 and 5 could run in parallel but are listed in sequence. "
            "| | Move step 5 beside step 4 and mark both as independent. |",
            "None.")
        self.assertEqual(self.check(text), (0, []))

    def test_missing_findings_column_is_flagged(self):
        text = check_report.GOOD_RETURN.replace("| Consequence |", "| Impact |")
        code, messages = self.check(text)
        self.assertEqual(code, 1)
        self.assertIn("missing column(s): consequence", " | ".join(m for _, m in messages))


class CommandLineTest(unittest.TestCase):
    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = write(tmp, "good.review.md", check_report.GOOD_RETURN)
            bad = write(tmp, "bad.review.md", check_report.GOOD_RETURN.replace(
                "**Verdict:** Return", "**Verdict:** Release"))
            headless = write(tmp, "headless.md", "# Notes\nnothing here\n")

            result = run_cli(good)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("good.review.md: ok", result.stdout)

            result = run_cli(bad)
            self.assertEqual(result.returncode, 1)
            self.assertRegex(result.stdout, r"bad\.review\.md:\d+: a Blocker is open")

            result = run_cli(headless)
            self.assertEqual(result.returncode, 2)
            self.assertIn("no review header", result.stderr)

            result = run_cli(os.path.join(tmp, "missing.md"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("cannot read file", result.stderr)

            result = run_cli(good, bad, headless)
            self.assertEqual(result.returncode, 2)

    def test_no_arguments_is_a_usage_error(self):
        self.assertEqual(run_cli().returncode, 2)

    def test_selftest_flag(self):
        result = run_cli("--selftest")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("selftest: all", result.stdout)


class EvalRunsTest(unittest.TestCase):
    def test_stored_eval_reviews_pass(self):
        found = []
        for directory, _, filenames in os.walk(os.path.join(ROOT, "evals", "runs")):
            found.extend(os.path.join(directory, f) for f in filenames if ".review-" in f and f.endswith(".md"))
        for path in sorted(found):
            with self.subTest(review=os.path.relpath(path, ROOT)):
                code, messages = check_report.check_file(path)
                self.assertEqual(code, 0, messages)


class RepoHygieneTest(unittest.TestCase):
    def test_no_em_dash_in_repo(self):
        offenders = []
        for directory, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for filename in filenames:
                path = os.path.join(directory, filename)
                try:
                    with open(path, encoding="utf-8") as handle:
                        for number, line in enumerate(handle, 1):
                            if check_report.EM_DASH in line:
                                offenders.append("%s:%d" % (os.path.relpath(path, ROOT), number))
                except UnicodeDecodeError:
                    continue
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
