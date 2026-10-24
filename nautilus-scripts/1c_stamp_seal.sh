#!/usr/bin/env bash
# ==============================================================================
# 🪙 Підписати (Лише кутова Золота печатка Бінду) / Sign (Corner Golden Seal Only)
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
        CHOSEN=$(zenity --file-selection --multiple --separator="|" --title="Оберіть документи (.pdf, .docx) для кутової Золотої печатки" --file-filter="PDF / DOCX | *.pdf *.PDF *.docx *.DOCX" 2>/dev/null || true)
        [[ -n "$CHOSEN" ]] && IFS="|" read -ra VALID_FILES <<< "$CHOSEN" || exit 0
    else
        exit 0
    fi
fi

SEAL_POLICY="$(marma_resolve_seal_pages)" || exit 0
CMD_ARGS=(sign --mode seal --seal-pages "$SEAL_POLICY")
[[ -z "${MARMA_HEADLESS:-}" ]] && CMD_ARGS+=(--gui)
CMD_ARGS+=("${VALID_FILES[@]}")
if marma_run_or_warn "Помилка підписання" "Signing failed" marma-watermark "${CMD_ARGS[@]}"; then
    marma_notify "document-edit" \
        "🪙 Накладено Золоту печатку Бінду" \
        "🪙 Applied Golden Bindu Authorship Seal" \
        "Успішно підписано ${#VALID_FILES[@]} документ(ів) кутовою золотою печаткою Marma-Crypto." \
        "Successfully signed ${#VALID_FILES[@]} document(s) with corner Golden Bindu seal."
fi
