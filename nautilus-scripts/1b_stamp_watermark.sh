#!/usr/bin/env bash
# ==============================================================================
# 🌊 Підписати PDF (Лише фоновий водяний знак) / Sign PDF (Background Watermark Only)
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
    if [[ -f "$f" && "${f,,}" == *.pdf ]]; then
        VALID_FILES+=("$f")
    elif [[ -f "${f%.*}.pdf" ]]; then
        VALID_FILES+=("${f%.*}.pdf")
    fi
done

if [[ ${#VALID_FILES[@]} -eq 0 ]]; then
    if command -v zenity >/dev/null 2>&1; then
        CHOSEN=$(zenity --file-selection --multiple --separator="|" --title="Оберіть PDF для фонового водяного знака Шрі Янтри" --file-filter="PDF (*.pdf) | *.pdf *.PDF" 2>/dev/null || true)
        [[ -n "$CHOSEN" ]] && IFS="|" read -ra VALID_FILES <<< "$CHOSEN" || exit 0
    else
        exit 0
    fi
fi

CMD_ARGS=(sign --mode watermark)
[[ -z "${MARMA_HEADLESS:-}" ]] && CMD_ARGS+=(--gui)
CMD_ARGS+=("${VALID_FILES[@]}")
if marma_run_or_warn "Помилка підписання" "Signing failed" marma-watermark "${CMD_ARGS[@]}"; then
    marma_notify "document-edit" \
        "🌊 Накладено фоновий водяний знак Шрі Янтри" \
        "🌊 Applied Sri Yantra Background Watermark" \
        "Успішно захищено ${#VALID_FILES[@]} PDF-документ(ів) векторним фоновим водяним знаком." \
        "Successfully watermarked ${#VALID_FILES[@]} PDF document(s)."
fi
