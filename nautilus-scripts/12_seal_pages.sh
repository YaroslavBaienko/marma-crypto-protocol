#!/usr/bin/env bash
# ==============================================================================
# ⚙️ Розміщення печатки — остання сторінка / усі / перша+остання / перша
# ⚙️ Seal placement — last page / all pages / first+last / first
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for p in "${SCRIPT_DIR}/.i18n.sh" "${SCRIPT_DIR}/_i18n.sh" "${SCRIPT_DIR}/../.i18n.sh" "/usr/share/marma-crypto-watermark/nautilus-scripts/_i18n.sh"; do
    [[ -f "$p" ]] && { source "$p"; break; }
done

CURRENT="$(marma_get_seal_pages)"
if [[ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" || -n "${MARMA_HEADLESS:-}" ]] || ! command -v zenity >/dev/null 2>&1; then
    printf '%s\n' "$CURRENT"
    exit 0
fi

CHOICE="$(zenity --list --radiolist \
    --title="$(marma_text "Розміщення печатки — Marma-Crypto" "Seal placement — Marma-Crypto")" \
    --text="$(marma_text "Поточна політика: ${CURRENT}\n\nОберіть, на яких сторінках ставити видиму печатку під час підписання PDF/DOCX:" "Current policy: ${CURRENT}\n\nChoose which pages carry the visible seal when signing PDF/DOCX:")" \
    --column="" --column="ID" --column="$(marma_text "Сторінки" "Pages")" \
    $([[ "$CURRENT" == "last" ]] && echo TRUE || echo FALSE) "last" "$(marma_text "Остання (сторінка підпису) — рекомендовано" "Last (signature page) — recommended")" \
    $([[ "$CURRENT" == "all" ]] && echo TRUE || echo FALSE) "all" "$(marma_text "Кожна сторінка" "Every page")" \
    $([[ "$CURRENT" == "first-last" ]] && echo TRUE || echo FALSE) "first-last" "$(marma_text "Перша + остання" "First + last")" \
    $([[ "$CURRENT" == "first" ]] && echo TRUE || echo FALSE) "first" "$(marma_text "Лише перша" "First only")" \
    $([[ "$CURRENT" == "ask" ]] && echo TRUE || echo FALSE) "ask" "$(marma_text "Питати під час підписання" "Ask on each signing")" \
    --hide-column=2 --print-column=2 --width=640 --height=430 2>/dev/null || true)"

[[ -z "$CHOICE" ]] && exit 0
marma_set_seal_pages "$CHOICE"
marma_notify "preferences-system" \
    "⚙️ Розміщення печатки збережено" \
    "⚙️ Seal placement saved" \
    "Поточна політика: $(marma_get_seal_pages)" \
    "Current policy: $(marma_get_seal_pages)"
