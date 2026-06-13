#!/usr/bin/env python3
"""
Generate gallery.html automatically from images in ../images/photos
"""

from pathlib import Path


# -------------------------------------------------
# Configuration
# -------------------------------------------------

IMAGE_DIR = Path("../images/photos")
OUTPUT_FILE = Path("gallery.html")

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}


# -------------------------------------------------
# HTML templates
# -------------------------------------------------

HTML_HEADER = """
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>GSIP - Gallery</title>

<link rel="stylesheet" href="style.css">

<style>

/* Gallery title */

.gallery-header {
    text-align: center;
    margin: 40px;
}


/* Masonry style gallery */

.photo-gallery {
    column-count: 4;
    column-gap: 15px;
    padding: 20px;
}


.photo-gallery img {
    width: 100%;
    margin-bottom: 15px;
    border-radius: 12px;
    display: block;

    transition: 
        transform 0.3s ease,
        box-shadow 0.3s ease;
}


.photo-gallery img:hover {

    transform: scale(1.03);

    box-shadow:
        0 10px 25px rgba(0,0,0,0.35);
}


/* Responsive */

@media (max-width: 1100px) {

    .photo-gallery {
        column-count: 3;
    }
}


@media (max-width: 700px) {

    .photo-gallery {
        column-count: 2;
    }
}


@media (max-width: 450px) {

    .photo-gallery {
        column-count: 1;
    }
}

</style>

</head>


<body>


<div class="gallery-header">

<h1>
GSIP Lab Gallery
</h1>


<p>
Research activities, experiments, conferences,
students, collaborations and everyday moments.
</p>

</div>


<div class="photo-gallery">

"""


HTML_FOOTER = """
</div>

</body>

</html>
"""


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    if not IMAGE_DIR.exists():
        print(
            f"ERROR: Directory not found: {IMAGE_DIR}"
        )
        return


    images = sorted(
        [
            f
            for f in IMAGE_DIR.iterdir()
            if (
                f.is_file()
                and f.suffix.lower()
                in VALID_EXTENSIONS
            )
        ]
    )


    print(
        f"Found {len(images)} images."
    )


    html = HTML_HEADER


    for img in images:

        relative_path = (
            "images/photos/" + img.name
        )

        html += (
            f'    <img src="{relative_path}" '
            f'alt="{img.stem}">\n'
        )


    html += HTML_FOOTER


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)


    print(
        f"Generated: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()