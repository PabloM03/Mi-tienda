#!/usr/bin/env bash
set -euo pipefail

echo "🔄  Preparando entorno…"

# ── 1. Dependencias Python ──────────────────────────────────────────────
python - <<'PY'
import importlib.util, subprocess, sys

pkgs = {"beautifulsoup4", "lxml"}
missing = [p for p in pkgs if importlib.util.find_spec(p) is None]

if missing:
    print("📦  Instalando dependencias Python:", ", ".join(missing))
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
PY

# ── 2. Comprobar Node 20+ ───────────────────────────────────────────────
NODE_MAJOR=$(node -p "process.versions.node.split('.')[0]")
if (( NODE_MAJOR < 20 )); then
  echo "❌  Shopify CLI requiere Node ≥ 20. Instálalo con nvm u otro gestor."
  exit 1
fi

# ── 3. Shopify CLI (local, vía npx) ─────────────────────────────────────
if ! npx --yes shopify -v >/dev/null 2>&1; then
  echo "⚙️  Instalando Shopify CLI (local)…"
  npm install -D @shopify/cli
fi
SHOPIFY="npx --yes shopify"

# ── 4. Ejecutar conversión ──────────────────────────────────────────────
echo "🚀  Convirtiendo HTML → Liquid…"
python scripts/html2shopify.py

# ── 5. Empaquetar theme ─────────────────────────────────────────────────
echo "📦  Creando theme.zip…"
cd theme
zip -qr ../theme.zip .
cd ..

# ── 6. Subida opcional a la tienda ──────────────────────────────────────
read -p $'¿Subir theme.zip a tu tienda ahora? [s/N] ' -r
if [[ $REPLY =~ ^[sS]$ ]]; then
  echo "🔑  Iniciando sesión (si hace falta)…"
  $SHOPIFY login --store="tu‑tienda.myshopify.com"

  echo "⬆️  Subiendo y publicando…"
  $SHOPIFY theme push \
    --path theme.zip \
    --theme "Migracion‑Auto" \
    --unpublished

  echo "✅  Tema “Migracion‑Auto” subido. Revísalo en tu admin."
else
  echo "✅  Listo. Archivo theme.zip generado en la raíz del proyecto."
fi
