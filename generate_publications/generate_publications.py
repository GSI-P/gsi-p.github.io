import bibtexparser
from collections import defaultdict


# --------------------------
# Read BibTeX file
# --------------------------

with open("publications.bib", encoding="utf-8") as bibfile:
    bib = bibtexparser.load(bibfile)


# --------------------------
# Group papers by area
# --------------------------

areas = defaultdict(list)

for paper in bib.entries:

    area = paper.get("gsip_area", "Other")
    areas[area].append(paper)


# Sort papers by year (newest first)
for area in areas:
    areas[area].sort(
        key=lambda x: int(x.get("year", 0)),
        reverse=True
    )


# Sort areas alphabetically
sorted_areas = sorted(areas.keys())


# --------------------------
# Generate HTML
# --------------------------

html = []

html.append("""
<section id="publications">

<h2>Publications</h2>

<p>
Selected scientific publications organized by research area.
</p>

""")


for area in sorted_areas:

    html.append(f"""
    <div class="pub-area">
        <h3>{area}</h3>
    """)

    for paper in areas[area]:

        title = paper.get("title", "No title")
        authors = paper.get("author", "")
        journal = paper.get("journal", "")
        year = paper.get("year", "")

        # Make authors more readable
        authors = authors.replace(" and ", ", ")

        html.append(f"""
        <div class="paper">

            <div class="paper-title">
                {title}
            </div>

            <div class="paper-authors">
                {authors}
            </div>

            <div class="paper-journal">
                <i>{journal}</i> ({year})
            </div>

        </div>
        """)

    html.append("</div>")


html.append("""
</section>
""")


# --------------------------
# Save HTML
# --------------------------

with open("publications.html", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(html))


print("publications.html generated successfully")