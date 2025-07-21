import os
from pathlib import Path
from bs4 import BeautifulSoup, Comment

# Directories containing the downloaded static HTML and the prefix
# used for the generated template name. Blog listings and articles
# are handled separately.
SOURCE_DIRS = {
    'pages': 'page',
    'products': 'product',
    'collections': 'collection',
    'policies': 'page',
    'blogs': 'blog',
    os.path.join('blogs', 'news'): 'article',
    'apps': 'page',
}

# Individual HTML files that map to specific Shopify templates. Each
# entry maps the path to the desired destination liquid file and the
# snippet prefix to use.
SPECIAL_FILES = {
    'index.html': ('theme/templates/index.liquid', 'page'),
    'search.html': ('theme/templates/search.liquid', 'page'),
    'cart.html': ('theme/templates/cart.liquid', 'page'),
    os.path.join('account', 'login.html'): (
        'theme/templates/customers/login.liquid',
        'page',
    ),
    os.path.join('account', 'register.html'): (
        'theme/templates/customers/register.liquid',
        'page',
    ),
}

# Destination for generated liquid templates
DEST_DIR = Path('theme/templates/generated')

HEADER = "{%% comment %%}Generated from %s{%% endcomment %%}\n"

# Minimal templates for each type. These reference the dynamic
# sections already present in the theme.


def extract_body(html_path: Path) -> str:
    """Return the body HTML from the given file, stripping HTTrack comments."""
    with html_path.open(encoding="utf-8") as f:
        html_text = f.read()

    html_text = html_text.replace("&lt;!-- Mirrored from", "<!-- Mirrored from")
    html_text = html_text.replace("&lt;\\!-- Mirrored from", "<!-- Mirrored from")
    html_text = html_text.replace("<\\!-- Mirrored from", "<!-- Mirrored from")
    soup = BeautifulSoup(html_text, "lxml")

    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "HTTrack" in comment or "Mirrored from" in comment:
            comment.extract()

    body = soup.body or soup
    if body.name == "body":
        return "".join(str(child) for child in body.children)
    return body.decode()


def convert_file(html_path: Path, prefix: str):
    """Create a liquid template containing the HTML body."""
    slug = html_path.stem
    dest_file = DEST_DIR / f"{prefix}.{slug}.liquid"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    html_content = extract_body(html_path)

    with dest_file.open("w", encoding="utf-8") as f:
        f.write(HEADER % html_path)
        f.write(html_content)

    return dest_file


def main():
    for src, prefix in SOURCE_DIRS.items():
        for html in Path(src).glob('*.html'):
            dest = convert_file(html, prefix)
            print(f"Created {dest}")

    # Handle files that map to specific Shopify templates
    for src, (dest, prefix) in SPECIAL_FILES.items():
        html_path = Path(src)
        if html_path.exists():
            dest_path = Path(dest)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            html_content = extract_body(html_path)
            with dest_path.open('w', encoding='utf-8') as f:
                f.write(HEADER % html_path)
                f.write(html_content)
            print(f"Created {dest_path}")


if __name__ == '__main__':
    main()
