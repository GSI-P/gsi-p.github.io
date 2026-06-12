import bibtexparser
from collections import defaultdict
import re


# --------------------------
# Helper functions
# --------------------------

def short_authors(author_string, max_authors=5):
    authors = author_string.split(" and ")

    short = []

    for a in authors[:max_authors]:
        names = a.split(",")

        if len(names) == 2:
            last = names[0].strip()
            first = names[1].strip()

            initials = " ".join([x[0]+"." for x in first.split()])
            short.append(f"{initials} {last}")

        else:
            short.append(a)

    if len(authors) > max_authors:
        short.append("et al.")

    return ", ".join(short)


def clean_latex(text):
    """
    Basic LaTeX accent cleaning
    """
    replacements = {
        r"{\'a}": "á",
        r"{\'e}": "é",
        r"{\'i}": "í",
        r"{\'o}": "ó",
        r"{\'u}": "ú",
        r"{\'A}": "Á",
        r"{\'E}": "É",
        r"{\'I}": "Í",
        r"{\'O}": "Ó",
        r"{\'U}": "Ú",
        r"{\~n}": "ñ",
        r"{\~N}": "Ñ"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


# --------------------------
# Read bib
# --------------------------

with open("publications.bib", encoding="utf-8") as f:
    bib = bibtexparser.load(f)


areas = defaultdict(list)


for paper in bib.entries:

    area = paper.get("gsip_area", "Other")
    areas[area].append(paper)


for area in areas:
    areas[area].sort(
        key=lambda x: int(x.get("year",0)),
        reverse=True
    )


# --------------------------
# Start HTML
# --------------------------

html = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>
GSIP Publications
</title>

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

<a href="index.html#research">
Research
</a>

<a href="index.html#people">
People
</a>

<a href="publications.html">
Publications
</a>

<a href="index.html#projects">
Projects
</a>

<a href="index.html#contact">
Contact
</a>

</nav>

</header>


<section id="publications">


<h1>
Publications
</h1>


<p>
Selected scientific publications organized by research area.
</p>

"""


# --------------------------
# Add papers
# --------------------------

for area in sorted(areas):

    html += f"""

<div class="pub-area">

<h2>
{area}
</h2>

"""

    for p in areas[area]:

        title = clean_latex(
            p.get("title","")
        )

        authors = clean_latex(
            short_authors(
                p.get("author","")
            )
        )

        journal = clean_latex(
            p.get("journal","")
        )

        year = p.get("year","")

        doi = p.get("doi","")


        html += """
<div class="paper">
"""


        html += f"""
<div class="paper-title">
{title}
</div>

<div class="paper-authors">
{authors}
</div>

<div class="paper-journal">
<i>{journal}</i> ({year})
</div>
"""


        if doi:

            html += f"""
<div class="paper-doi">
<a href="https://doi.org/{doi}" target="_blank">
DOI: {doi}
</a>
</div>
"""


        html += """
</div>
"""


    html += """
</div>
"""


html += """

</section>


</body>

</html>

"""


# --------------------------
# Save
# --------------------------

with open(
    "publications.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(html)


print(
"GSIP publications page generated successfully."
)