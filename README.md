# Migration helper

This repository contains the downloaded static version of the site and a lightweight Shopify theme under `theme/`.

To quickly convert remaining static HTML files into Liquid templates, run:

```bash
python scripts/convert_html_to_liquid.py [--dest DIR]
```

Generated templates will be placed in `theme/templates/generated/` by default.
Use `--dest` to specify a different output directory.

