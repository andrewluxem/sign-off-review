#!/usr/bin/env python3
"""Validate a finished sign-off review against the skill's verdict rules.

Usage:
    python3 scripts/check_report.py REVIEW.md [REVIEW.md ...]
    python3 scripts/check_report.py --selftest

Exit codes:
    0  every file is valid
    1  rule violations, each printed as PATH:LINE: message
    2  a file is unreadable, or its first non-blank line is not a review header

Standard library only. Python 3.9 or newer.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile

EM_DASH = "\u2014"

VERDICTS = ("Return", "Release with fixes", "Release")
SEVERITIES = ("Blocker", "Major", "Minor")
SEATS = ("Decision", "Logic", "Evidence", "Skeptic", "Outsider")
LEAD_SEAT = "Lead"
EARLY_STAGE_SEATS = ("Decision", "Logic")
PRIOR_STATUSES = ("fixed", "partly fixed", "open")

# The persona each profile names in parentheses after a seat, as in
# "Skeptic (CFO)". A seat missing from a profile's map takes no persona.
# Keep in step with the "## Seat N:" headings in references/profiles/.
PROFILES = {
    "strategy": {
        "Decision": "decision maker",
        "Skeptic": "CFO",
        "Outsider": "non-specialist",
    },
    "pitch": {
        "Decision": "economic buyer",
        "Skeptic": "procurement",
        "Outsider": "non-specialist",
    },
    "brief-post": {
        "Decision": "busy reader",
        "Skeptic": "dissenting practitioner",
        "Outsider": "non-specialist",
    },
    "job-search": {
        "Decision": "hiring manager",
        "Skeptic": "recruiter",
        "Outsider": "non-specialist",
    },
    "build-plan": {
        "Decision": "owner",
        "Skeptic": "operator",
        "Outsider": "fresh agent",
    },
}

REQUIRED_FIELDS = ("verdict", "in one line", "question", "answer the draft gives")

SECTION_FINDINGS = "findings"
SECTION_TIES = "numbers that do not tie"
SECTION_OUTSIDE = "missing outside view"
SECTION_PREMORTEM = "premortem"
SECTION_GOOD = "what is good and must survive"
SECTION_FIXED = "what fixed looks like"
SECTION_PRIOR = "prior findings"
REQUIRED_SECTIONS = (
    SECTION_FINDINGS,
    SECTION_TIES,
    SECTION_OUTSIDE,
    SECTION_PREMORTEM,
    SECTION_GOOD,
)

FINDING_COLUMNS = ("#", "severity", "seat", "where", "problem", "consequence", "fix")
TIE_COLUMNS = ("number", "location a", "location b", "difference")
PRIOR_COLUMNS = ("#", "status")

# Cell contents that mean "nothing here".
EMPTY_TOKENS = {"", "-", "--", "\u2013", "n/a", "na", "none", "tbd"}

HEADER_PREFIX = re.compile(r"^#\s+sign-off review\b", re.IGNORECASE)
HEADER = re.compile(
    r"^#\s+sign-off review:\s*(?P<document>.+?),\s*profile\s+(?P<profile>\S+),"
    r"\s*stage\s+(?P<stage>\S+)\s*$",
    re.IGNORECASE,
)
FIELD = re.compile(r"^\*\*(?P<name>[^*]+?):\*\*\s*(?P<value>.*)$")
SEAT_CELL = re.compile(r"^(?P<seat>[A-Za-z]+)\s*(?:\((?P<persona>[^()]*)\))?$")
HEDGED_FIX = re.compile(r"^(consider|you may|you might|perhaps)", re.IGNORECASE)
NUMBERED_ITEM = re.compile(r"^ {0,3}\d+[.)]\s+\S")
ANY_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
SEPARATOR_CELL = re.compile(r"^:?-+:?$")


class Section:
    def __init__(self, line: int, title: str):
        self.line = line
        self.title = title
        self.body = []  # (line number, raw text) pairs


def clean(cell: str) -> str:
    """Strip whitespace and Markdown emphasis or code marks from a cell."""
    return re.sub(r"^[\s*_`]+|[\s*_`]+$", "", cell)


def is_empty(cell: str) -> bool:
    return clean(cell).rstrip(".").lower() in EMPTY_TOKENS


def canonical(value: str, choices) -> str | None:
    for choice in choices:
        if value.lower() == choice.lower():
            return choice
    return None


def normalize_heading(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().rstrip(":")).lower()


def split_row(line: str) -> list:
    text = line.strip().replace("\\|", "\x00")
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip().replace("\x00", "|") for cell in text.split("|")]


def parse_table(body: list):
    """Return (header, rows) for the first table in a section body.

    header is (line, cells) or None. rows holds (line, cells) for data rows,
    leaving out separator rows and placeholder rows whose cells are all empty.
    """
    header = None
    rows = []
    for number, text in body:
        if text.lstrip().startswith("|"):
            cells = split_row(text)
            if header is None:
                header = (number, cells)
            elif all(SEPARATOR_CELL.match(c.strip()) for c in cells if c.strip()):
                continue
            elif not all(is_empty(c) for c in cells):
                rows.append((number, cells))
        elif header is not None:
            break
    return header, rows


def column_index(header_cells: list) -> dict:
    return {clean(cell).lower(): i for i, cell in enumerate(header_cells)}


def cell(cells: list, columns: dict, name: str) -> str:
    i = columns.get(name)
    if i is None or i >= len(cells):
        return ""
    return cells[i]


def has_content(section: Section | None) -> bool:
    if section is None:
        return False
    return any(not is_empty(text) for _, text in section.body)


def numbered_items(section: Section) -> list:
    """Top-level numbered list items, each joined with its continuation lines."""
    items = []
    for _, text in section.body:
        if NUMBERED_ITEM.match(text):
            items.append(text.strip())
        elif items and text.strip() and not ANY_ITEM.match(text):
            items[-1] += " " + text.strip()
    return items


def seat_problem(value: str, profile: str | None, stage: int | None) -> str | None:
    text = clean(value)
    match = SEAT_CELL.match(text)
    if not match:
        return "seat %r does not parse; write a seat name such as 'Skeptic' or 'Skeptic (CFO)'" % text
    seat = canonical(match.group("seat"), SEATS + (LEAD_SEAT,))
    if seat is None:
        return "unknown seat %r; use one of %s" % (
            match.group("seat"),
            ", ".join(SEATS + (LEAD_SEAT,)),
        )
    persona = match.group("persona")
    if persona is not None and profile is not None:
        expected = PROFILES[profile].get(seat)
        if expected is None or persona.strip().lower() != expected.lower():
            wanted = "no persona" if expected is None else "persona %r" % expected
            return "persona %r is not valid for the %s seat in profile %s (takes %s)" % (
                persona.strip(),
                seat,
                profile,
                wanted,
            )
    if stage in (1, 2) and seat not in EARLY_STAGE_SEATS + (LEAD_SEAT,):
        return "stage %d runs only the Decision and Logic seats, so %s findings are not valid" % (
            stage,
            seat,
        )
    return None


def check_text(text: str):
    """Check review text. Return (exit code, sorted list of (line, message))."""
    lines = text.lstrip("\ufeff").splitlines()
    first = next(((n, t) for n, t in enumerate(lines, 1) if t.strip()), None)
    if first is None or not HEADER_PREFIX.match(first[1].strip()):
        where = first[0] if first else 1
        return 2, [(where, "no review header; the first non-blank line must be "
                           "'# Sign-off review: <document>, profile <profile>, stage <1|2|3>'")]

    violations = []

    def flag(line: int, message: str) -> None:
        violations.append((line, message))

    # Rule 1: the header parses and names a known profile and stage.
    header_line = first[0]
    profile = None
    stage = None
    match = HEADER.match(first[1].strip())
    if not match:
        flag(header_line, "header does not parse; expected "
                          "'# Sign-off review: <document>, profile <profile>, stage <1|2|3>'")
    else:
        name = match.group("profile").lower()
        if name in PROFILES:
            profile = name
        else:
            flag(header_line, "unknown profile %r; use one of %s" % (name, ", ".join(PROFILES)))
        if match.group("stage") in ("1", "2", "3"):
            stage = int(match.group("stage"))
        else:
            flag(header_line, "stage %r is not 1, 2 or 3" % match.group("stage"))

    fields = {}
    sections = {}
    current = None
    for number, raw in enumerate(lines, 1):
        if number <= header_line:
            continue
        stripped = raw.strip()
        if stripped.startswith("## "):
            key = normalize_heading(stripped[3:])
            if key in sections:
                flag(number, "duplicate section %r" % stripped[3:].strip())
                current = Section(number, stripped[3:].strip())
            else:
                current = sections[key] = Section(number, stripped[3:].strip())
            continue
        if current is None:
            found = FIELD.match(stripped)
            if found:
                fields[found.group("name").strip().lower()] = (number, found.group("value"))
        else:
            current.body.append((number, raw))

    for name in REQUIRED_FIELDS:
        if name not in fields:
            flag(header_line, "missing the **%s:** line under the header" % name.capitalize())
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            flag(len(lines), "missing section '## %s'" % name.capitalize())

    # Rule 2: the verdict is one of the three values.
    verdict = None
    verdict_line = header_line
    if "verdict" in fields:
        verdict_line, value = fields["verdict"]
        verdict = canonical(clean(value).rstrip("."), VERDICTS)
        if verdict is None:
            flag(verdict_line, "verdict %r is not Return, Release with fixes or Release" % clean(value))

    # Rules 3, 4 and 9: severity, seat, consequence and fix on each finding.
    blocker_lines = []
    finding_numbers = set()
    findings = sections.get(SECTION_FINDINGS)
    if findings is not None:
        header, rows = parse_table(findings.body)
        if header is not None:
            columns = column_index(header[1])
            missing = [c for c in FINDING_COLUMNS if c not in columns]
            if missing:
                flag(header[0], "findings table is missing column(s): %s" % ", ".join(missing))
            for number, cells in rows:
                severity = canonical(clean(cell(cells, columns, "severity")), SEVERITIES)
                if severity is None:
                    flag(number, "severity %r is not Blocker, Major or Minor"
                         % clean(cell(cells, columns, "severity")))
                if "seat" in columns:
                    problem = seat_problem(cell(cells, columns, "seat"), profile, stage)
                    if problem:
                        flag(number, problem)
                if severity in ("Blocker", "Major") and is_empty(cell(cells, columns, "consequence")):
                    flag(number, "%s finding has no consequence; add one sentence or rate it Minor"
                         % severity)
                if severity == "Blocker":
                    blocker_lines.append(number)
                fix = clean(cell(cells, columns, "fix"))
                hedge = HEDGED_FIX.match(fix)
                if hedge:
                    flag(number, "fix starts with %r; write it as an instruction "
                                 "(Reconcile, Cut, Replace, Add)" % hedge.group(1))
                if not is_empty(cell(cells, columns, "#")):
                    finding_numbers.add(clean(cell(cells, columns, "#")))

    # Rule 5: an open Blocker or any tie-out row forces Return.
    tie_rows = []
    ties = sections.get(SECTION_TIES)
    if ties is not None:
        header, tie_rows = parse_table(ties.body)
        if header is not None:
            columns = column_index(header[1])
            missing = [c for c in TIE_COLUMNS if c not in columns]
            if missing:
                flag(header[0], "tie-out table is missing column(s): %s" % ", ".join(missing))
    if verdict is not None and verdict != "Return":
        for number in blocker_lines:
            flag(number, "a Blocker is open, so the verdict must be Return (line %d says %s)"
                 % (verdict_line, verdict))
        for number, _ in tie_rows:
            flag(number, "a number that does not tie forces verdict Return (line %d says %s)"
                 % (verdict_line, verdict))

    # Rule 6: Return needs a picture of what fixed looks like.
    if verdict == "Return" and not has_content(sections.get(SECTION_FIXED)):
        where = sections[SECTION_FIXED].line if SECTION_FIXED in sections else verdict_line
        flag(where, "verdict is Return, so '## What fixed looks like' must say what fixed looks like")

    # Rule 7: three premortem reasons, at least one internal.
    premortem = sections.get(SECTION_PREMORTEM)
    if premortem is not None:
        items = numbered_items(premortem)
        if len(items) != 3:
            flag(premortem.line, "premortem has %d numbered item(s); it needs exactly 3" % len(items))
        if not any("(internal)" in item.lower() for item in items):
            flag(premortem.line, "no premortem item is tagged (internal)")

    # Rule 8: at least one thing that is good and must survive.
    good = sections.get(SECTION_GOOD)
    if good is not None and not any(ANY_ITEM.match(text) for _, text in good.body):
        flag(good.line, "'What is good and must survive' needs at least one list item")

    # Re-review: prior statuses are valid and unfixed items stay in Findings.
    prior = sections.get(SECTION_PRIOR)
    if prior is not None:
        header, rows = parse_table(prior.body)
        if header is None:
            flag(prior.line, "'Prior findings' needs a table with # and Status columns")
        else:
            columns = column_index(header[1])
            missing = [c for c in PRIOR_COLUMNS if c not in columns]
            if missing:
                flag(header[0], "prior findings table is missing column(s): %s" % ", ".join(missing))
            for number, cells in rows:
                status = canonical(clean(cell(cells, columns, "status")), PRIOR_STATUSES)
                if status is None:
                    flag(number, "status %r is not fixed, partly fixed or open"
                         % clean(cell(cells, columns, "status")))
                elif status != "fixed":
                    prior_number = clean(cell(cells, columns, "#"))
                    if prior_number not in finding_numbers:
                        flag(number, "prior finding %s is %s but is not carried into Findings "
                                     "under the same number" % (prior_number, status))

    # Rule 10: no em dash anywhere.
    for number, raw in enumerate(lines, 1):
        if EM_DASH in raw:
            flag(number, "em dash (U+2014); use a comma, colon, period or parentheses")

    violations.sort()
    return (1 if violations else 0), violations


def check_file(path: str):
    """Check one review file. Return (exit code, list of (line, message))."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        return 2, [(0, "cannot read file: %s" % exc)]
    return check_text(text)


# Fixtures for --selftest and the unit tests.

GOOD_RETURN = """\
# Sign-off review: harbor-memo.md, profile strategy, stage 3
**Verdict:** Return
**In one line:** The saving is stated as two different figures, so the decision cannot rest on it yet.
**Question:** Should we close the Harbor site by June? (given)
**Answer the draft gives:** Yes, closing saves $2.0M a year.

## Findings
| # | Severity | Seat | Where | Problem | Consequence | Fix |
|---|---|---|---|---|---|---|
| 1 | Blocker | Lead | Summary vs cost table | The annual saving is $2.0M in the summary and $1.6M in the cost table. | The board would approve on a saving the memo's own table does not support. | Reconcile the saving to one figure and update the summary and payback to match. |
| 2 | Major | Skeptic (CFO) | Risks | No downside case for slower store delivery. | The committee cannot see what is lost if delivery slips at peak. | Add a downside case with the revenue at risk and the trigger for reversing. |
| 3 | Minor | Outsider (non-specialist) | Page 2 | "WMS" is not expanded. | | Replace "WMS" with "warehouse system" on first use. |

## Numbers that do not tie
| Number | Location A | Location B | Difference |
|---|---|---|---|
| Annual saving | $2.0M (Summary) | $1.6M (Cost table total) | $0.4M |

## Missing outside view
- The 25 percent cost cut is not compared with any closure the company has done before.

## Premortem
1. No one owns the move after the lease decision, so the timeline slips. (internal)
2. The receiving site cannot hire 20 people by May.
3. Store sales fall during peak because delivery moves to two days.

## What is good and must survive
- The lease deadline and its source are on page 1.

## What fixed looks like
One saving figure appears everywhere, the payback is recomputed from it, and a downside case shows the revenue at risk at peak.
"""

GOOD_RELEASE = """\
# Sign-off review: deploy-plan.md, profile build-plan, stage 2
**Verdict:** Release
**In one line:** The outline is complete enough to write the full plan.
**Question:** Can a fresh agent turn this outline into a full plan? (reconstructed, assumption)
**Answer the draft gives:** Yes, every step names its input and output.

## Findings
| # | Severity | Seat | Where | Problem | Consequence | Fix |
|---|---|---|---|---|---|---|
| 1 | Minor | Logic | Step 4 | Steps 4 and 5 could run in parallel but are listed in sequence. | | Move step 5 beside step 4 and mark both as independent. |

## Numbers that do not tie
None.

## Missing outside view
None.

## Premortem
1. The plan has no named owner after handover, so nobody runs step 6. (internal)
2. The staging database is smaller than production, so timings mislead.
3. A dependency upgrade lands mid-run.

## What is good and must survive
- Each step states its input, output and how to check it.
"""

GOOD_REREVIEW = GOOD_RETURN.replace(
    "## Findings\n",
    "## Prior findings\n"
    "| # | Status | Note |\n"
    "|---|---|---|\n"
    "| 1 | open | Summary still says $2.0M. |\n"
    "| 2 | partly fixed | Downside case added without a trigger. |\n"
    "| 3 | fixed | Expanded on page 2. |\n"
    "\n## Findings\n",
)


def selftest_cases():
    """Return (name, content, expected exit code, expected message fragment).

    content is a str written as UTF-8, bytes written as is, or None for a
    path that is a directory.
    """
    r = GOOD_RETURN
    g = GOOD_RELEASE
    tie_table = (
        "| Number | Location A | Location B | Difference |\n"
        "|---|---|---|---|\n"
        "| Run time | 40 min (Step 2) | 55 min (Summary) | 15 min |\n"
    )
    return [
        ("valid Return review", r, 0, ""),
        ("valid Release review at stage 2", g, 0, ""),
        ("valid re-review", GOOD_REREVIEW, 0, ""),
        ("placeholder tie row is not data", g.replace(
            "## Numbers that do not tie\nNone.",
            "## Numbers that do not tie\n| Number | Location A | Location B | Difference |\n"
            "|---|---|---|---|\n| - | - | - | - |"), 0, ""),
        ("header missing", r.replace(
            "# Sign-off review: harbor-memo.md, profile strategy, stage 3", "# Review of harbor-memo.md"),
         2, "no review header"),
        ("empty file", "", 2, "no review header"),
        ("path is a directory", None, 2, "cannot read file"),
        ("not UTF-8", b"\xff\xfe\x00 not text", 2, "cannot read file"),
        ("header does not parse", r.replace(
            "harbor-memo.md, profile strategy, stage 3", "harbor-memo.md"), 1, "header does not parse"),
        ("unknown profile", r.replace("profile strategy", "profile roadmap"), 1, "unknown profile"),
        ("stage out of range", r.replace("stage 3", "stage 4"), 1, "not 1, 2 or 3"),
        ("verdict not allowed", r.replace("**Verdict:** Return", "**Verdict:** Ship it"),
         1, "is not Return, Release with fixes or Release"),
        ("severity not allowed", r.replace("| 2 | Major |", "| 2 | Critical |"),
         1, "is not Blocker, Major or Minor"),
        ("persona from another profile", r.replace("Skeptic (CFO)", "Skeptic (recruiter)"),
         1, "not valid for the Skeptic seat"),
        ("unknown seat", r.replace("Outsider (non-specialist)", "Marketing"), 1, "unknown seat"),
        ("seat outside stage 2", g.replace("| Minor | Logic |", "| Minor | Skeptic (operator) |"),
         1, "stage 2 runs only the Decision and Logic seats"),
        ("Major without consequence", r.replace(
            "The committee cannot see what is lost if delivery slips at peak.", ""),
         1, "Major finding has no consequence"),
        ("Blocker without consequence", r.replace(
            "The board would approve on a saving the memo's own table does not support.", "-"),
         1, "Blocker finding has no consequence"),
        ("Blocker released", r.replace("**Verdict:** Return", "**Verdict:** Release with fixes"),
         1, "a Blocker is open, so the verdict must be Return"),
        ("tie row released", g.replace("## Numbers that do not tie\nNone.",
                                       "## Numbers that do not tie\n" + tie_table),
         1, "a number that does not tie forces verdict Return"),
        ("Return without fixed picture", r.split("## What fixed looks like")[0],
         1, "must say what fixed looks like"),
        ("Return with empty fixed picture", r.replace(
            "One saving figure appears everywhere, the payback is recomputed from it, and a "
            "downside case shows the revenue at risk at peak.", "None."),
         1, "must say what fixed looks like"),
        ("premortem with two reasons", r.replace(
            "3. Store sales fall during peak because delivery moves to two days.\n", ""),
         1, "needs exactly 3"),
        ("premortem with four reasons", r.replace(
            "3. Store sales fall during peak because delivery moves to two days.\n",
            "3. Store sales fall during peak because delivery moves to two days.\n"
            "4. Fuel costs rise.\n"),
         1, "needs exactly 3"),
        ("premortem with nothing internal", r.replace(" (internal)", ""),
         1, "no premortem item is tagged (internal)"),
        ("nothing good", r.replace("- The lease deadline and its source are on page 1.", "None."),
         1, "needs at least one list item"),
        ("fix starts with consider", r.replace(
            "Add a downside case with", "Consider adding a downside case with"),
         1, "fix starts with 'Consider'"),
        ("fix starts with perhaps", r.replace(
            "Replace \"WMS\" with", "Perhaps replace \"WMS\" with"), 1, "fix starts with 'Perhaps'"),
        ("fix starts with you might", r.replace(
            "Reconcile the saving", "you might reconcile the saving"), 1, "fix starts with 'you might'"),
        ("em dash", r.replace("two different figures,", "two different figures " + EM_DASH),
         1, "em dash"),
        ("missing section", r.replace(
            "## Missing outside view\n- The 25 percent cost cut is not compared with any closure "
            "the company has done before.\n", ""),
         1, "missing section '## Missing outside view'"),
        ("missing question line", r.replace(
            "**Question:** Should we close the Harbor site by June? (given)\n", ""),
         1, "missing the **Question:** line"),
        ("prior finding left open but dropped", GOOD_REREVIEW.replace(
            "| 2 | Major | Skeptic (CFO) |", "| 4 | Major | Skeptic (CFO) |"),
         1, "prior finding 2 is partly fixed but is not carried into Findings"),
        ("prior status not allowed", GOOD_REREVIEW.replace("| 3 | fixed |", "| 3 | done |"),
         1, "is not fixed, partly fixed or open"),
    ]


def run_selftest() -> int:
    failures = []
    cases = selftest_cases()
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, content, want_code, want_text) in enumerate(cases):
            path = os.path.join(tmp, "case-%02d.review.md" % i)
            if content is None:
                os.mkdir(path)
            elif isinstance(content, bytes):
                with open(path, "wb") as handle:
                    handle.write(content)
            else:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(content)
            code, messages = check_file(path)
            joined = " | ".join(message for _, message in messages)
            if code != want_code or (want_text and want_text not in joined):
                failures.append("%s: expected exit %d with %r, got exit %d: %s"
                                % (name, want_code, want_text, code, joined or "no messages"))
    if failures:
        for failure in failures:
            print("selftest FAIL: " + failure)
        print("selftest: %d of %d cases failed" % (len(failures), len(cases)))
        return 1
    print("selftest: all %d cases passed" % len(cases))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a sign-off review file against the verdict rules.")
    parser.add_argument("reviews", nargs="*", metavar="REVIEW.md")
    parser.add_argument("--selftest", action="store_true",
                        help="build good and bad reviews in a temp dir and check the verdicts")
    args = parser.parse_args(argv)
    if args.selftest:
        return run_selftest()
    if not args.reviews:
        parser.error("give at least one review file, or --selftest")
    worst = 0
    for path in args.reviews:
        code, messages = check_file(path)
        stream = sys.stderr if code == 2 else sys.stdout
        for line, message in messages:
            print("%s:%d: %s" % (path, line, message), file=stream)
        if code == 0:
            print("%s: ok" % path)
        elif code == 1:
            print("%s: %d violation(s)" % (path, len(messages)))
        worst = max(worst, code)
    return worst


if __name__ == "__main__":
    sys.exit(main())
