"""Utility for converting downloaded HTML files into Shopify Liquid templates.

The script traverses a set of known source directories (``pages``,
``products``, ``collections`` and ``blogs/news``) and for each ``.html`` file
creates a corresponding Liquid template inside ``theme/templates/generated`` by
default.  The generated template simply wraps the original HTML content and
annotates it with a comment describing its origin.

Files named ``POST.html`` are skipped as they represent HTTP method stubs rather
than real templates.  A custom output directory can be supplied via the
``--dest`` command-line argument.
"""

import os
from pathlib import Path
import argparse

# Directories containing the downloaded static HTML
SOURCE_DIRS = {
    'pages': 'page',
    'products': 'product',
    'collections': 'collection',
    os.path.join('blogs', 'news'): 'article'
}

# Default destination for generated liquid templates
DEFAULT_DEST = Path('theme/templates/generated')

HEADER = "{%% comment %%}Generated from %s{%% endcomment %%}\n"


def convert_file(html_path: Path, prefix: str, dest_dir: Path) -> Path:
    slug = html_path.stem
    dest_file = dest_dir / f"{prefix}.{slug}.liquid"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with html_path.open(encoding='utf-8') as f:
        content = f.read()
    with dest_file.open('w', encoding='utf-8') as f:
        f.write(HEADER % html_path)
        f.write(content)
    return dest_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-d",
        "--dest",
        default=str(DEFAULT_DEST),
        help="Destination directory for generated templates",
    )
    args = parser.parse_args()

    dest_dir = Path(args.dest)

    for src, prefix in SOURCE_DIRS.items():
        for html in Path(src).glob('*.html'):
            if html.name == 'POST.html':
                continue
            dest = convert_file(html, prefix, dest_dir)
            print(f"Created {dest}")


if __name__ == '__main__':
    main()
