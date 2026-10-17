#!/usr/bin/env bash
# Minify the hand-written sources in src/ into the assets/ paths the HTML
# already references, so there is a single source of truth and no drift.
set -euo pipefail
cd "$(dirname "$0")/.."

ESBUILD="./node_modules/.bin/esbuild"
[ -x "$ESBUILD" ] || ESBUILD="npx --no-install esbuild"

"$ESBUILD" --minify src/css/style.css --outfile=assets/css/style.css    --log-level=warning
"$ESBUILD" --minify src/js/main.js    --outfile=assets/js/main.js       --log-level=warning
"$ESBUILD" --minify src/js/scene.js   --outfile=assets/js/scene.js      --log-level=warning
# analytics.js is configuration plus the instructions for filling it in, so it
# is copied verbatim rather than minified — the comments are the point.
cp src/js/analytics.js assets/js/analytics.js

printf '%-26s %8s bytes\n' assets/css/style.css  "$(wc -c < assets/css/style.css)"
printf '%-26s %8s bytes\n' assets/js/main.js     "$(wc -c < assets/js/main.js)"
printf '%-26s %8s bytes\n' assets/js/scene.js    "$(wc -c < assets/js/scene.js)"
printf '%-26s %8s bytes\n' assets/js/analytics.js "$(wc -c < assets/js/analytics.js)"
