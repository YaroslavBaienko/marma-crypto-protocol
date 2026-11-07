#!/usr/bin/env bash
# ==============================================================================
# 🕵️ Підписати скрито (Stealth · 0% видимості + Canary) / Sign Stealth (0% Visible Marks + Canary)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for p in "${SCRIPT_DIR}/.i18n.sh" "${SCRIPT_DIR}/_i18n.sh" "${SCRIPT_DIR}/../.i18n.sh" "/usr/share/marma-crypto-watermark/nautilus-scripts/_i18n.sh"; do
    [[ -f "$p" ]] && { source "$p"; break; }
done

mapfile -t FILES < <(marma_selected_files)
if [[ ${#FILES[@]} -eq 0 ]]; then
    FILES=("$@")
fi

VALID_FILES=()
for f in "${FILES[@]}"; do
    if [[ -f "$f" ]]; then
        case "${f,,}" in
            *.pdf|*.docx) VALID_FILES+=("$f") ;;
            *)
                companion="${f%.*}.pdf"
                [[ -f "$companion" ]] && VALID_FILES+=("$companion")
                ;;
        esac
    fi
done

if [[ ${#VALID_FILES[@]} -eq 0 ]]; then
    if command -v zenity >/dev/null 2>&1; then
        CHOSEN=$(zenity --file-selection --multiple --separator="|" \
            --title="$(marma_text "Оберіть документи (.pdf, .docx) для скритого підпису (Stealth)" "Select documents (.pdf, .docx) for Stealth signing")" \
            --file-filter="PDF / DOCX | *.pdf *.PDF *.docx *.DOCX" 2>/dev/null || true)
        [[ -n "$CHOSEN" ]] && IFS="|" read -ra VALID_FILES <<< "$CHOSEN" || exit 0
    else
        exit 0
    fi
fi

RECIPIENT_ID="${MARMA_RECIPIENT_ID:-}"
if [[ -z "$RECIPIENT_ID" && -z "${MARMA_HEADLESS:-}" ]] && command -v zenity >/dev/null 2>&1 && [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]]; then
    RECIPIENT_ID=$(zenity --entry \
        --title="$(marma_text "Скрите штампування (Stealth · 0% видимості)" "Stealth Stamping (0% Visible Marks)")" \
        --text="$(marma_text "Введіть ідентифікатор отримувача для маркера Canary (або залиште порожнім):" "Enter recipient ID for Canary leak-tracing (or leave empty):")" \
        --entry-text="" \
        --width=500 2>/dev/null || true)
fi

CMD_ARGS=(sign --mode stealth --seal-pages none)
[[ -n "$RECIPIENT_ID" ]] && CMD_ARGS+=(--recipient-id "$RECIPIENT_ID")
[[ -z "${MARMA_HEADLESS:-}" ]] && CMD_ARGS+=(--gui)
CMD_ARGS+=("${VALID_FILES[@]}")
if marma_run_or_warn "Помилка скритого підписання" "Stealth signing failed" marma-watermark "${CMD_ARGS[@]}"; then
    marma_notify "security-high" \
        "🕵️ Накладено скритий штамп Marma-Crypto (Stealth)" \
        "🕵️ Applied Stealth Marma-Crypto Stamp (0% Visible)" \
        "Успішно захищено ${#VALID_FILES[@]} документ(ів) без жодних видимих слідів на сторінці (L/M/H 27-DOF + ДСТУ 4145-2002)." \
        "Successfully protected ${#VALID_FILES[@]} document(s) with zero visible marks on the page."
fi
