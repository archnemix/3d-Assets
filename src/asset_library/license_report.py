"""Render the license audit as a page a human can actually read."""


def verdict(passed: bool) -> str:
    return "Yes" if passed else "NO"


def credit_verdict(attribution_free: bool) -> str:
    return "Not required" if attribution_free else "REQUIRED"


def asset_rows(report: dict) -> list[str]:
    lines = [
        "| Asset | Category | Creator / source | License | Free | Credit | Sell with it | Use as-is | Display |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for asset in sorted(report["assets"], key=lambda item: (item["category"], item["id"])):
        checks = asset["checks"]
        cells = [
            verdict(checks["free_of_charge"]),
            credit_verdict(checks["no_attribution_required"]),
            verdict(checks["commercial_use_allowed"]),
            verdict(checks["redistribution_allowed"] and checks["standalone_resale_permitted"]),
            verdict(checks["cc0_spdx"] and checks["no_trademark_warning"]),
        ]
        lines.append(
            f"| [{asset['title']}]({asset_link(asset)}) | `{asset['category']}` | "
            f"{asset['creator']} ({asset['provider']}) | {asset['spdx']} | "
            + " | ".join(cells)
            + " |"
        )
    return lines


def asset_link(asset: dict) -> str:
    return f"../{asset['directory']}/README.md"


def provider_sections(report: dict) -> list[str]:
    lines = []
    for name, provider in report["providers"].items():
        count = report["totals"]["by_provider"][name]
        lines += [
            f"### {provider['name']} — `{name}`",
            "",
            f"{count} approved assets. Status: **{provider['status']}**.",
            "",
            f"- Terms: <{provider['terms_url']}>",
            f"- Pinned evidence: <{provider['evidence_url']}>",
            f"- Reselling the files themselves: {provider['resale_as_is']['note']}",
            "",
        ]
        lines += [f"- {caveat}" for caveat in provider["caveats"]]
        lines.append("")
    return lines


def notes_section(report: dict) -> list[str]:
    lines = ["## Per-asset notes", ""]
    flagged = [asset for asset in report["assets"] if asset["notes"] or asset["ai_assisted"]]
    if not flagged:
        return lines + ["No asset carries an additional note.", ""]
    lines += ["| Asset | Note |", "| --- | --- |"]
    for asset in sorted(flagged, key=lambda item: item["id"]):
        notes = list(asset["notes"])
        if asset["ai_assisted"] and not any("AI" in note for note in notes):
            notes.append("AI-assisted origin disclosed by the source.")
        lines.append(f"| [{asset['title']}]({asset_link(asset)}) | {' '.join(notes)} |")
    return lines + [""]


def evidence_section(report: dict) -> list[str]:
    lines = [
        "## Evidence per asset",
        "",
        "Each row links to the license file stored beside the model and to the exact",
        " upstream page or pinned revision it came from.",
        "",
        "| Asset | License file | SHA-256 (first 12) | Source | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for asset in sorted(report["assets"], key=lambda item: item["id"]):
        lines.append(
            f"| {asset['id']} | [LICENSE.txt](../{asset['license_file']}) | "
            f"`{asset['license_file_sha256'][:12]}` | [source]({asset['source_url']}) | "
            f"[evidence]({asset['license_evidence']}) |"
        )
    return lines + [""]


def checks_section(report: dict) -> list[str]:
    names = sorted({name for asset in report["assets"] for name in asset["checks"]})
    total = report["totals"]["assets"]
    lines = [
        "## What was checked",
        "",
        "Every check below is machine-verified by `python -m asset_library license-audit`.",
        "",
        "| Check | Passing |",
        "| --- | --- |",
    ]
    for name in names:
        passing = sum(asset["checks"][name] for asset in report["assets"])
        lines.append(f"| `{name}` | {passing}/{total} |")
    return lines + [""]


def render(report: dict) -> str:
    totals = report["totals"]
    lines = [
        "# License audit",
        "",
        f"Checked on {report['checked_on']}. Scope: {report['scope']}.",
        "",
        f"**{totals['passed']} of {totals['assets']} approved assets pass every check.**",
        "",
        "Every approved asset is dedicated to the public domain under CC0 1.0. For each one",
        "that means: no cost, no attribution, commercial use allowed, use and redistribution",
        "of the files as they are (not only inside a compiled game), and public display in",
        "this gallery. The caveats below are real and are not hidden by that summary.",
        "",
        "Regenerate with `python -m asset_library license-audit`; verify with `--check`.",
        "Machine-readable results: [`reports/license-audit.json`](../reports/license-audit.json).",
        "",
        "## Per-asset verdict",
        "",
        '"Use as-is" means the model files may be shipped, mirrored, published or sold',
        'standalone. "Display" means showing the model and our own renders publicly.',
        "",
    ]
    lines += asset_rows(report)
    lines += ["", "## What CC0 does not cover", ""]
    lines += [f"- {caveat}" for caveat in report["universal_caveats"]]
    lines += ["", "## Source terms and caveats", ""]
    lines += provider_sections(report)
    lines += notes_section(report)
    lines += checks_section(report)
    lines += evidence_section(report)
    return "\n".join(lines)
