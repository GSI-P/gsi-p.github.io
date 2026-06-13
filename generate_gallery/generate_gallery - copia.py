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
    <a href="gallery.html">Gallery</a>
    <a href="index.html#contact">Contact</a>
</nav>

</header>


<section id="publications">

<h1>{title}</h1>

"""

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

/* ===========================
   Lightbox
   =========================== */

#lightbox {

    display: none;

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    background: rgba(0,0,0,0.9);

    z-index: 1000;

    justify-content: center;
    align-items: center;

    cursor: pointer;
}


#lightbox img {

    max-width: 90%;
    max-height: 90%;

    border-radius: 12px;

    box-shadow: 0 0 40px rgba(0,0,0,0.8);

    cursor: default;
}


</style>

</head>


<body>


<div class="gallery-header">

<h1>
GSIP photo Gallery
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


<!-- Lightbox -->
<div id="lightbox">
    <img id="lightbox-img" src="">
</div>


<script>

const images = document.querySelectorAll(
    ".photo-gallery img"
);


const lightbox =
    document.getElementById("lightbox");


const lightboxImg =
    document.getElementById("lightbox-img");


// Open image

images.forEach(img => {

    img.addEventListener("click", () => {

        lightboxImg.src = img.src;

        lightbox.style.display = "flex";

    });

});


// Close when clicking outside

lightbox.addEventListener("click", () => {

    lightbox.style.display = "none";

});


// Close with ESC key

document.addEventListener(
    "keydown",
    (event) => {

        if(event.key === "Escape") {

            lightbox.style.display = "none";

        }

    }
);

</script>


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