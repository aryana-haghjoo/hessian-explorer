#!/usr/bin/env bash
# Wrap hessian_explorer.html in a full HTML document as index.html, for GitHub Pages or any static host.
set -euo pipefail
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  printf '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>\n'
  printf '</head>\n<body>\n'
  cat hessian_explorer.html
  printf '\n</body>\n</html>\n'
} > index.html
echo "wrote index.html"
