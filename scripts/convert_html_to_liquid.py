import os
from pathlib import Path

# Directories containing the downloaded static HTML
SOURCE_DIRS = {
    'pages': 'page',
    'products': 'product',
    'collections': 'collection',
    os.path.join('blogs', 'news'): 'article'
}

# Destination for generated liquid templates
DEST_DIR = Path('theme/templates/generated')

HEADER = "{%% comment %%}Generated from %s{%% endcomment %%}\n"


def convert_file(html_path: Path, prefix: str):
    slug = html_path.stem
    dest_file = DEST_DIR / f"{prefix}.{slug}.liquid"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with html_path.open(encoding='utf-8') as f:
        content = f.read()
    with dest_file.open('w', encoding='utf-8') as f:
        f.write(HEADER % html_path)
        f.write(content)
    return dest_file


def main():
    for src, prefix in SOURCE_DIRS.items():
        for html in Path(src).glob('*.html'):
            dest = convert_file(html, prefix)
            print(f"Created {dest}")


if __name__ == '__main__':
    main()
