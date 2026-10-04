"""Render the GitHub contribution graph (last 12 months) as an SVG that mirrors GitHub's own design.

Reads the public contributions page (no token required) and writes
``assets/contributions.svg``.

Usage:
    python scripts/contribution_quarters.py [--user USER] [--year YEAR] [--out PATH]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
import urllib.request
from pathlib import Path

PALETTE = {0: "#171722", 1: "#0e4a25", 2: "#12823a", 3: "#19b34a", 4: "#22e06b"}
BG, PANEL, BORDER = "#0d0d14", "#10101a", "#2a2a3a"
TEXT, MUTED = "#E2E8F0", "#8b8ba3"
ACCENTS = ["#05D9E8", "#B967FF", "#FF2A6D", "#F9F002"]
CELL, GAP = 15, 3
STEP = CELL + GAP
QUARTERS = [("Q1", 1, 3), ("Q2", 4, 6), ("Q3", 7, 9), ("Q4", 10, 12)]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch_days(user: str, year: int | None = None) -> dict[dt.date, tuple[int, int]]:
    """Return {date: (level, count)} parsed from the public contributions page."""
    url = f"https://github.com/users/{user}/contributions"
    if year:
        url += f"?from={year}-01-01&to={year}-12-31"
    req = urllib.request.Request(url, headers={"User-Agent": "contrib-quarters/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - fixed https host
        page = resp.read().decode("utf-8")
    cells = re.findall(
        r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"\s+data-level="(\d)"', page
    )
    tips = dict(
        re.findall(r'for="(contribution-day-component[^"]+)"[^>]*>\s*([^<]+)<', page)
    )
    days: dict[dt.date, tuple[int, int]] = {}
    for date, cid, level in cells:
        m = re.match(r"(\d+)\s+contribution", tips.get(cid, "").strip())
        days[dt.date.fromisoformat(date)] = (int(level), int(m.group(1)) if m else 0)
    if not days:
        raise RuntimeError("No contribution data found; page layout may have changed")
    return days


def week_start(d: dt.date) -> dt.date:
    """Sunday on or before ``d``."""
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def render(days, today):
    """Replica of GitHub's own contribution graph (last 12 months) with a year selector."""
    cell, gap = 11, 3
    step = cell + gap
    ordered = sorted(d for d in days if d <= today)
    first = week_start(ordered[0])
    weeks = (week_start(ordered[-1]) - first).days // 7 + 1
    total = sum(days[d][1] for d in ordered)
    left, top = 56, 64
    card_x, card_y = 24, 56
    grid_w = weeks * step - gap
    card_w = left + grid_w + 28
    card_h = top + 7 * step - gap + 62
    side_x = card_x + card_w + 28
    W, H = side_x + 130, card_y + card_h + 28
    cells, months, last_month = [], [], None
    for d in ordered:
        level, count = days[d]
        col, row = (d - first).days // 7, (d.weekday() + 1) % 7
        x, y = card_x + left + col * step, card_y + top + row * step
        cells.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{PALETTE[level]}">'
            f"<title>{count} contributions on {d:%b %d, %Y}</title></rect>"
        )
        if d.day <= 7 and d.month != last_month and row == 0 or (d == ordered[0] and False):
            last_month = d.month
            months.append(f'<text x="{x}" y="{card_y + top - 14}" class="m">{MONTHS[d.month - 1]}</text>')
    days_lbl = "".join(
        f'<text x="{card_x + 18}" y="{card_y + top + r * step + cell - 1}" class="d">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    ly = card_y + card_h - 18
    lx = card_x + card_w - 24 - 5 * (cell + 4) - 70
    legend = "".join(
        f'<rect x="{lx + 38 + i * (cell + 4)}" y="{ly - 10}" width="{cell}" height="{cell}" rx="2" fill="{PALETTE[i]}"/>' for i in range(5)
    )
    years = [today.year - i for i in range(5)]
    side = ""
    for i, yv in enumerate(years):
        yy = card_y + i * 35
        if i == 0:
            side += f'<rect x="{side_x}" y="{yy - 4}" width="116" height="30" rx="6" fill="#5200f5"/><text x="{side_x + 16}" y="{yy + 16}" class="y" fill="#fff">{yv}</text>'
        else:
            side += f'<text x="{side_x + 16}" y="{yy + 16}" class="y" fill="{MUTED}">{yv}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{total} contributions in the last year">
<style>
text{{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}}
.h{{font-size:16px;font-weight:600;fill:{TEXT}}}.s{{font-size:12px;fill:{MUTED}}}
.m{{font-size:12px;fill:{TEXT}}}.d{{font-size:12px;fill:{TEXT}}}.y{{font-size:13px;font-weight:600}}
</style>
<rect width="100%" height="100%" fill="{BG}"/>
<text x="{card_x}" y="36" class="h">{total} contributions in the last year</text>
<text x="{card_x + card_w - 18}" y="36" class="s" text-anchor="end">Contribution settings \u25be</text>
<rect x="{card_x + 0.5}" y="{card_y + 0.5}" width="{card_w}" height="{card_h}" rx="8" fill="none" stroke="{BORDER}"/>
{"".join(months)}{days_lbl}{"".join(cells)}
<text x="{card_x + left}" y="{ly}" class="s">Learn how we count contributions</text>
<text x="{lx}" y="{ly}" class="s">Less</text>{legend}<text x="{lx + 38 + 5 * (cell + 4) + 2}" y="{ly}" class="s">More</text>
{side}
</svg>
'''


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--user", default="amerelfalwo")
    ap.add_argument("--year", type=int, default=None, help="optional calendar year; default is the last 12 months")
    ap.add_argument("--out", default="assets/contributions.svg")
    a = ap.parse_args()
    days = fetch_days(a.user, a.year)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(days, dt.date.today()), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
