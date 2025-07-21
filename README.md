# Migration helper

This repository contains the downloaded static version of the site and a lightweight Shopify theme under `theme/`.

To generate Liquid templates for the downloaded HTML pages, run:

```bash
python scripts/convert_html_to_liquid.py
```

The script will create minimal templates that reference the dynamic sections in
the theme so the content is pulled from Shopify. It scans `pages/`, `policies/`,
`collections/`, `products/`, `blogs/` (and their articles), and now `apps/`.
The resulting Liquid templates are placed under `theme/templates/generated/`.

