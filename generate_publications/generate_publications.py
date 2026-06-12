"""
GSIP Website Page Generator

Generate static HTML pages from a BibTeX database.

Input:
    gsip_library.bib

Generated pages:
    publications.html
    theses_projects.html

The BibTeX field 'gsip_type' determines where each entry appears.

Author: GSIP
"""

import bibtexparser
from collections import defaultdict


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

BIB_FILE = "gsip_library.bib"

PUBLICATION_TYPES = [
    "Journal Article"
]

THESIS_PROJECT_TYPES = [
    "PhD Thesis",
    "Master's Thesis",
    "Undergraduate Projects",
    "Posters",
    "Technical Reports"
]


# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------

def clean_text(text):
    """
    Remove simple LaTeX formatting from BibTeX strings.
    """

    if not text:
        return ""

    replacements = {
        "{\\'a}": "á",
        "{\\'e}": "é",
        "{\\'i}": "í",
        "{\\'o}": "ó",
        "{\\'u}": "ú",
        "{\\~n}": "ñ",
        "{\\~N}": "Ñ",
        "{\\'A}": "Á",
        "{\\'E}": "É",
        "{\\'I}": "Í",
        "{\\'O}": "Ó",
        "{\\'U}": "Ú",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("{", "")
    text = text.replace("}", "")

    return text


def format_authors(author_field, max_authors=6):
    """
    Convert BibTeX author list into a compact format.

    Example:
    Chierchie, Fernando and Doe, John

    becomes:
    F. Chierchie, J. Doe
    """

    if not author_field:
        return ""

    authors = author_field.split(" and ")
    formatted = []

    for author in authors[:max_authors]:

        parts = author.split(",")

        if len(parts) == 2:
            last = parts[0].strip()
            first = parts[1].strip()

            initials = " ".join(
                name[0] + "."
                for name in first.split()
            )

            formatted.append(
                f"{initials} {last}"
            )

        else:
            formatted.append(author)

    if len(authors) > max_authors:
        formatted.append("et al.")

    return ", ".join(formatted)


def sort_by_year(entries):
    """
    Sort entries by year in descending order.
    """

    return sorted(
        entries,
        key=lambda x: int(x.get("year", 0)),
        reverse=True
    )


# ------------------------------------------------------------------
# HTML structure
# ------------------------------------------------------------------

def html_header(title):
    """
    Generate common HTML page header.
    """

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>{title} - GSIP</title>

<link rel="preconnect"
      href="https://fonts.googleapis.com">

<link rel="preconnect"
      href="https://fonts.gstatic.com"
      crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap"
      rel="stylesheet">

<link rel="stylesheet" href="style.css">

</head>


<body>

<header>

<nav>
    <a href="index.html#research">Research</a>
    <a href="index.html#people">People</a>
    <a href="publications.html">Publications</a>
    <a href="theses_projects.html">Theses & Projects</a>
    <a href="index.html#projects">Projects</a>
    <a href="index.html#contact">Contact</a>
</nav>

</header>


<section id="publications">

<h1>{title}</h1>

"""


def html_footer():
    """
    Generate common HTML footer.
    """

    return """
</section>

<footer>

GSIP — Group of Sensors,
Instrumentation and Processing

</footer>

</body>
</html>
"""

# ------------------------------------------------------------------
# Entry formatting
# ------------------------------------------------------------------

def format_entry(entry):
    """
    Convert a single BibTeX entry into an HTML card.
    The displayed fields depend on the GSIP entry type.
    """

    html = '<div class="paper">\n'

    # Title
    title = clean_text(entry.get("title", ""))
    html += f'<div class="paper-title">{title}</div>\n'

    # Authors
    authors = format_authors(entry.get("author", ""))
    if authors:
        html += (
            f'<div class="paper-authors">'
            f'{authors}</div>\n'
        )

    entry_type = entry.get("gsip_type", "")
    year = entry.get("year", "")

    # Journal articles
    if entry_type in PUBLICATION_TYPES:

        journal = clean_text(
            entry.get("journal", "")
        )

        details = []

        if journal:
            details.append(f"<i>{journal}</i>")

        if year:
            details.append(year)

        if details:
            html += (
                '<div class="paper-journal">'
                + ", ".join(details)
                + '</div>\n'
            )
        
        doi = entry.get("doi", "")

        if doi:
            html += (
                f'<div class="paper-journal">'
                f'<a href="https://doi.org/{doi}" target="_blank">'
                f'DOI</a>'
                f'</div>\n'
            )
    # Theses, projects, posters, reports
    else:

        note = clean_text(
            entry.get("note", "")
        )

        institution = clean_text(
            entry.get("institution", "")
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

        advisor = clean_text(
            entry.get("gsip_advisor", "")
        )

        if advisor:
            html += (
                f'<div class="paper-authors">'
                f'Advisor: {advisor}'
                f'</div>\n'
            )

        coadvisor = clean_text(
            entry.get("gsip_coadvisor", "")
        )

        if coadvisor:
            html += (
                f'<div class="paper-authors">'
                f'Co-advisor: {coadvisor}'
                f'</div>\n'
            )

    # Optional link (PDF, repository, DOI, etc.)
    link = entry.get("gsip_link", "")

    if link:
        html += (
            f'<div class="paper-journal">'
            f'<a href="{link}" target="_blank">'
            f'PDF / Link</a>'
            f'</div>\n'
        )

    html += "</div>\n"

    return html


# ------------------------------------------------------------------
# Page generation
# ------------------------------------------------------------------

def generate_page(filename, title, groups):
    """
    Generate a complete HTML page from grouped entries.
    """

    html = html_header(title)

    for group_name, entries in groups.items():

        html += (
            '<div class="pub-area">\n'
            f'<h2>{group_name}</h2>\n'
        )

        for entry in sort_by_year(entries):
            html += format_entry(entry)

        html += "</div>\n"

    html += html_footer()

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Generated: {filename}")


# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

def main():

    print("Reading BibTeX library...")

    with open(BIB_FILE, encoding="utf-8") as bib_file:
        database = bibtexparser.load(bib_file)

    entries = database.entries


    # ------------------------------
    # Publications
    # Group by research area
    # ------------------------------

    publications = defaultdict(list)

    for entry in entries:

        if entry.get("gsip_type") in PUBLICATION_TYPES:

            area = entry.get(
                "gsip_area",
                "Other"
            )

            publications[area].append(entry)

    generate_page(
        "publications.html",
        "Publications",
        publications
    )


    # ------------------------------
    # Theses and projects
    # Group by output type
    # ------------------------------

    theses_projects = defaultdict(list)

    for entry in entries:

        entry_type = entry.get("gsip_type")

        if entry_type in THESIS_PROJECT_TYPES:
            theses_projects[entry_type].append(entry)

    ordered_groups = {}

    for group in THESIS_PROJECT_TYPES:

        if group in theses_projects:
            ordered_groups[group] = (
                theses_projects[group]
            )

    generate_page(
        "theses_projects.html",
        "Theses and Projects",
        ordered_groups
    )

    print("All GSIP pages generated successfully.")


if __name__ == "__main__":
    main()