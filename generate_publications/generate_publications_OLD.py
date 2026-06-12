import bibtexparser
from collections import defaultdict
import re

#=====================================================
#Configuration
#=====================================================

BIB_FILE = "gsip_library.bib"

JOURNAL_TYPES = [
"Journal Article"
]

THESIS_TYPES = [
"PhD Thesis",
"Master's Thesis",
"Undergraduate Project",
"Poster",
"Technical Report"
]

#=====================================================
#Helper functions
#=====================================================

def clean_latex(text):

if not text:
    return ""

replacements = {
    r"{\'a}": "á",
    r"{\'e}": "é",
    r"{\'i}": "í",
    r"{\'o}": "ó",
    r"{\'u}": "ú",
    r"{\~n}": "ñ",
    r"{\~N}": "Ñ",
}

for old, new in replacements.items():
    text = text.replace(old, new)

text = text.replace("{", "")
text = text.replace("}", "")

return text

def short_authors(author_string, max_authors=6):

authors = author_string.split(" and ")

result = []

for a in authors[:max_authors]:

    parts = a.split(",")

    if len(parts) == 2:
        last = parts[0].strip()
        first = parts[1].strip()

        initials = " ".join(
            x[0] + "."
            for x in first.split()
        )

        result.append(f"{initials} {last}")

    else:
        result.append(a)

if len(authors) > max_authors:
    result.append("et al.")

return ", ".join(result)

def page_header(title):

return f"""

def page_footer():

return """
#=====================================================
#Paper formatting
#=====================================================

def format_entry(entry):

html = '<div class="paper">\n'

title = clean_latex(
    entry.get("title", "")
)

authors = clean_latex(
    short_authors(
        entry.get("author", "")
    )
)

year = entry.get("year", "")

html += (
    f'<div class="paper-title">{title}</div>\n'
)

if authors:
    html += (
        f'<div class="paper-authors">'
        f'{authors}</div>\n'
    )


# Journal article
if entry.get("gsip_type") in JOURNAL_TYPES:

    journal = clean_latex(
        entry.get("journal", "")
    )

    html += (
        f'<div class="paper-journal">'
        f'<i>{journal}</i> ({year})'
        f'</div>\n'
    )


# Thesis / project
else:

    institution = clean_latex(
        entry.get("institution", "")
    )

    note = clean_latex(
        entry.get("note", "")
    )

    if note:
        html += (
            f'<div class="paper-journal">'
            f'{note}</div>\n'
        )

    if institution:
        html += (
            f'<div class="paper-journal">'
            f'{institution}</div>\n'
        )

    if year:
        html += (
            f'<div class="paper-journal">'
            f'{year}</div>\n'
        )


    advisor = entry.get("gsip_advisor")
    if advisor:
        html += (
            f'<div class="paper-authors">'
            f'Advisor: {advisor}</div>'
        )


    coadvisor = entry.get("gsip_coadvisor")
    if coadvisor:
        html += (
            f'<div class="paper-authors">'
            f'Co-advisor: {coadvisor}</div>'
        )


link = entry.get("gsip_link")

if link:
    html += (
        f'<div class="paper-journal">'
        f'<a href="{link}" target="_blank">'
        f'PDF / Link</a></div>'
    )


html += "</div>\n"

return html
#=====================================================
#Generate pages
#=====================================================

with open(BIB_FILE, encoding="utf-8") as f:

database = bibtexparser.load(f)

entries = database.entries

#=====================================================
#Publications
#=====================================================

areas = defaultdict(list)

for e in entries:

if e.get("gsip_type") in JOURNAL_TYPES:

    areas[e.get(
        "gsip_area",
        "Other"
    )].append(e)

html = page_header(
"Publications"
)

for area in sorted(areas):

html += (
    f'<div class="pub-area">'
    f'<h2>{area}</h2>'
)

papers = sorted(
    areas[area],
    key=lambda x:
    int(x.get("year", 0)),
    reverse=True
)

for p in papers:
    html += format_entry(p)

html += "</div>"

html += page_footer()

with open(
"publications.html",
"w",
encoding="utf-8"
) as f:

f.write(html)
#=====================================================
#Theses and projects
#=====================================================

groups = defaultdict(list)

for e in entries:

if e.get("gsip_type") in THESIS_TYPES:

    groups[e["gsip_type"]].append(e)

html = page_header(
"Theses & Projects"
)

for group in THESIS_TYPES:

if group not in groups:
    continue

html += (
    f'<div class="pub-area">'
    f'<h2>{group}</h2>'
)

items = sorted(
    groups[group],
    key=lambda x:
    int(x.get("year", 0)),
    reverse=True
)

for item in items:
    html += format_entry(item)

html += "</div>"

html += page_footer()

with open(
"theses_projects.html",
"w",
encoding="utf-8"
) as f:

f.write(html)

print("GSIP pages generated successfully.")