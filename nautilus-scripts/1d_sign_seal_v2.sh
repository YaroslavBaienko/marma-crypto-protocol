#!/usr/bin/env bash
# ==============================================================================
# 🪙 Згенерувати круглу технічну печатку 42 мм (profile v2-round42)
# 🪙 Generate the 42 mm round technical seal (profile v2-round42)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for p in "${SCRIPT_DIR}/.i18n.sh" "${SCRIPT_DIR}/_i18n.sh" "${SCRIPT_DIR}/../.i18n.sh" "/usr/share/marma-crypto-watermark/nautilus-scripts/_i18n.sh"; do
    [[ -f "$p" ]] && { source "$p"; break; }
done

TARGET_DIR="$PWD"
if [[ -n "${NAUTILUS_SCRIPT_CURRENT_URI:-}" && "${NAUTILUS_SCRIPT_CURRENT_URI}" == file://* ]]; then
    TARGET_DIR="$(python3 -c "import urllib.parse, sys; print(urllib.parse.unquote(sys.argv[1][7:]))" "$NAUTILUS_SCRIPT_CURRENT_URI")"
fi

OUT_SVG="${TARGET_DIR}/marma_seal_42mm_v2.svg"
if marma-watermark --sign-svg "$OUT_SVG" --profile v2-round42 --gui >/dev/null 2>&1; then
    marma_notify "image-x-generic" \
        "🪙 Створено круглу технічну печатку 42 мм" \
        "🪙 Created 42 mm round technical seal" \
        "Профіль v2-round42: $(basename "$OUT_SVG")" \
        "Profile v2-round42: $(basename "$OUT_SVG")"
fi
