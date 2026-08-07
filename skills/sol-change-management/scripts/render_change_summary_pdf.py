#!/usr/bin/env python3
"""Render a Sol change-summary Markdown file to HTML and PDF.

This intentionally avoids third-party Python dependencies. It supports the
Markdown subset used by Sol change summaries: headings, paragraphs, inline
code, links, images, simple tables, and flat ordered/unordered lists.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

FOOTER_MARKING = "Quantinuum Internal Only"


def inline_markup(text: str) -> str:
    placeholders: list[str] = []

    def repl_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    text = re.sub(r"`([^`]+)`", repl_code, text)
    text = html.escape(text)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: f'<img alt="{html.escape(m.group(1))}" src="{html.escape(m.group(2))}">',
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2))}">{html.escape(m.group(1))}</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)

    for i, value in enumerate(placeholders):
        text = text.replace(f"\x00{i}\x00", value)
    return text


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def is_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def normalize_table_cells(cells: list[str], headers: list[str]) -> list[str]:
    """Keep malformed row pipes from creating phantom PDF columns.

    Markdown requires literal cell pipes to be escaped, but change summaries
    often quote interface rows like `A | B | C`. Recover the common impacted-doc
    table shape so one unescaped quoted row does not destroy the PDF layout.
    """
    expected = len(headers)
    if len(cells) == expected:
        return cells
    if len(cells) < expected:
        return cells + [""] * (expected - len(cells))

    normalized_headers = [header.strip().lower() for header in headers]
    if normalized_headers == ["document", "released file inspected", "impact driver", "assessment"]:
        return [cells[0], cells[1], " | ".join(cells[2:-1]), cells[-1]]
    return cells[: expected - 1] + [" | ".join(cells[expected - 1 :])]


def is_field_card_table(headers: list[str]) -> bool:
    normalized_headers = tuple(header.strip().lower() for header in headers)
    return normalized_headers in {
        ("document", "released file inspected", "impact driver", "assessment"),
        ("document", "evidence checked", "why it is not in the proposed field yet"),
        ("document", "evidence checked", "assessment"),
    }


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    if is_field_card_table(headers):
        blocks = ['<div class="field-table">']
        for row in rows:
            title = row[0] if row else ""
            blocks.append('<section class="field-card">')
            blocks.append(
                f'<h4 class="field-card-title">{inline_markup(headers[0])}: {inline_markup(title)}</h4>'
            )
            for header, value in zip(headers[1:], row[1:]):
                blocks.append('<div class="field-row">')
                blocks.append(f'<div class="field-label">{inline_markup(header)}</div>')
                blocks.append(f'<div class="field-value">{inline_markup(value)}</div>')
                blocks.append("</div>")
            blocks.append("</section>")
        blocks.append("</div>")
        return "\n".join(blocks)

    parts = ["<table>"]
    parts.append(
        "<thead><tr>"
        + "".join(f"<th>{inline_markup(header)}</th>" for header in headers)
        + "</tr></thead>"
    )
    parts.append("<tbody>")
    for row in rows:
        parts.append(
            "<tr>" + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row) + "</tr>"
        )
    parts.append("</tbody></table>")
    return "\n".join(parts)


def markdown_to_html(markdown: str, base_uri: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            level = min(level, 6)
            out.append(f"<h{level}>{inline_markup(text)}</h{level}>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            headers = split_table_row(line)
            rows: list[list[str]] = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = normalize_table_cells(split_table_row(lines[i]), headers)
                rows.append(cells)
                i += 1
            out.append(render_table(headers, rows))
            continue

        if stripped.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].strip().startswith("- "):
                out.append(f"<li>{inline_markup(lines[i].strip()[2:])}</li>")
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"\d+\.\s+", stripped):
            out.append("<ol>")
            while i < len(lines) and re.match(r"\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                out.append(f"<li>{inline_markup(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        if stripped.startswith("!["):
            out.append(f"<p>{inline_markup(stripped)}</p>")
            i += 1
            continue

        paragraph = [stripped]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if (
                not next_line
                or next_line.startswith("#")
                or next_line.startswith("|")
                or next_line.startswith("- ")
                or re.match(r"\d+\.\s+", next_line)
                or next_line.startswith("![")
            ):
                break
            paragraph.append(next_line)
            i += 1
        out.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")

    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "Change Summary")
    footer_date = datetime.now().strftime("%Y-%m-%d")
    footer_marking = html.escape(FOOTER_MARKING)
    css = """
@page {
  size: Letter;
  margin: 0.55in 0.55in 0.72in;
  @bottom-center {
    content: "__FOOTER_MARKING__";
    font-family: Arial, Helvetica, sans-serif;
    font-size: 7pt;
    color: #6b7280;
  }
  @bottom-right {
    content: "__FOOTER_DATE__   " counter(page) " / " counter(pages);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 7pt;
    color: #6b7280;
  }
}
body { font-family: Arial, Helvetica, sans-serif; color: #111827; font-size: 10.5pt; line-height: 1.36; }
h1 { font-size: 22pt; margin: 0 0 12px; color: #0f172a; }
h2 { font-size: 16pt; margin: 24px 0 8px; color: #111827; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; }
h3 { font-size: 13pt; margin: 18px 0 6px; color: #1f2937; }
h4 { font-size: 11.5pt; margin: 14px 0 6px; color: #334155; }
h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
p { margin: 7px 0; }
ul, ol { margin: 6px 0 8px 22px; padding: 0; }
li { margin: 3px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 14px; font-size: 8.7pt; page-break-inside: auto; }
th, td { border: 1px solid #cbd5e1; padding: 4px 5px; vertical-align: top; overflow-wrap: anywhere; }
th { background: #e5e7eb; color: #111827; font-weight: 700; }
tr { page-break-inside: avoid; }
.field-table { margin: 8px 0 14px; }
.field-card { border: 1px solid #cbd5e1; border-radius: 3px; margin: 8px 0 12px; break-inside: avoid; page-break-inside: avoid; }
.field-card-title { margin: 0; padding: 6px 8px; background: #e5e7eb; color: #111827; font-size: 10.5pt; border-bottom: 1px solid #cbd5e1; }
.field-row { display: grid; grid-template-columns: 1.35in 1fr; border-top: 1px solid #e5e7eb; }
.field-row:first-of-type { border-top: 0; }
.field-label { padding: 5px 7px; font-weight: 700; color: #374151; background: #f8fafc; border-right: 1px solid #e5e7eb; }
.field-value { padding: 5px 7px; overflow-wrap: anywhere; }
code { font-family: Consolas, 'Courier New', monospace; background: #f1f5f9; padding: 0 2px; border-radius: 2px; }
img { display: block; max-width: 100%; height: auto; margin: 8px auto 14px; border: 1px solid #cbd5e1; }
a { color: #075985; }
""".replace("__FOOTER_MARKING__", footer_marking).replace("__FOOTER_DATE__", footer_date)
    return (
        "<!doctype html>\n"
        f'<html><head><meta charset="utf-8"><base href="{html.escape(base_uri)}">'
        f"<title>{html.escape(title)}</title><style>{css}</style></head>\n"
        f"<body>\n{chr(10).join(out)}\n</body></html>\n"
    )


def find_chrome(explicit: str | None) -> str:
    candidates = []
    if explicit:
        candidates.append(explicit)
    candidates.extend(
        [
            shutil.which("chrome"),
            shutil.which("chrome.exe"),
            shutil.which("msedge"),
            shutil.which("msedge.exe"),
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
    )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise FileNotFoundError("Chrome or Edge executable was not found.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Change summary Markdown path.")
    parser.add_argument("--pdf", type=Path, help="Output PDF path.")
    parser.add_argument("--html", type=Path, help="Output HTML path.")
    parser.add_argument("--chrome", help="Path to Chrome or Edge executable.")
    args = parser.parse_args()

    markdown_path = args.markdown.resolve()
    package_dir = markdown_path.parent
    dry_run_dir = package_dir / "smartsheet-dry-run"
    dry_run_dir.mkdir(exist_ok=True)

    html_path = (args.html or dry_run_dir / f"{markdown_path.stem}_print.html").resolve()
    pdf_path = (args.pdf or markdown_path.with_suffix(".pdf")).resolve()

    html_text = markdown_to_html(
        markdown_path.read_text(encoding="utf-8"),
        package_dir.as_uri() + "/",
    )
    html_path.write_text(html_text, encoding="utf-8")

    chrome = find_chrome(args.chrome)
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
    )

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF was not created: {pdf_path}")

    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
