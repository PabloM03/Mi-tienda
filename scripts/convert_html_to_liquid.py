import os
from pathlib import Path

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
TEMPLATE_SNIPPETS = {
    'page': "{% section 'page-content' %}\n",
    'product': "{% section 'main-product' %}\n",
    'article': "{% section 'article-content' %}\n",
    'blog': "{% section 'blog-posts' %}\n",
    'collection': (
        "<h1>{{ collection.title }}</h1>\n"
        "{% for product in collection.products %}\n"
        "  <div><a href='{{ product.url }}'>{{ product.title }}</a></div>\n"
        "{% endfor %}\n"
    ),
}


def convert_file(html_path: Path, prefix: str):
    """Create a liquid template pointing to the relevant section."""
    slug = html_path.stem
    dest_file = DEST_DIR / f"{prefix}.{slug}.liquid"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    snippet = TEMPLATE_SNIPPETS.get(prefix, '')
    with dest_file.open('w', encoding='utf-8') as f:
        f.write(HEADER % html_path)
        f.write(snippet)
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
            snippet = TEMPLATE_SNIPPETS.get(prefix, '')
            with dest_path.open('w', encoding='utf-8') as f:
                f.write(HEADER % html_path)
                f.write(snippet)
            print(f"Created {dest_path}")


if __name__ == '__main__':
    main()
