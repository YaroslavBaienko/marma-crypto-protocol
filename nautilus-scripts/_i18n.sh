#!/usr/bin/env bash
# ==============================================================================
# _i18n.sh — Спільний модуль локалізації для Nautilus-скриптів Marma-Crypto
# ==============================================================================

get_marma_lang() {
    local cfg="$HOME/.config/marma-crypto/config.json"
    if [[ -f "$cfg" ]]; then
        local user_lang
        user_lang=$(grep -o '"lang"[[:space:]]*:[[:space:]]*"[^"]*"' "$cfg" 2>/dev/null | cut -d'"' -f4 || true)
        if [[ "$user_lang" == "en" ]]; then echo "en"; return; fi
        if [[ "$user_lang" == "uk" || "$user_lang" == "ua" ]]; then echo "uk"; return; fi
    fi

    local l="${LANGUAGE:-${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}}"
    if [[ -z "$l" && -f /etc/default/locale ]]; then
        l=$(grep -E '^(LANGUAGE|LANG|LC_MESSAGES)=' /etc/default/locale | head -n1 | cut -d= -f2 | tr -d '"' || true)
    fi
    if [[ "${l,,}" =~ ^uk ]]; then
        echo "uk"
    else
        echo "en"
    fi
}

MARMA_LANG="${MARMA_LANG:-$(get_marma_lang)}"
export MARMA_LANG

# Resolve the files selected in Nautilus. Newer Nautilus versions/views may expose the
# selection as URIs (or only as URIs) instead of plain file paths; reading only
# NAUTILUS_SCRIPT_SELECTED_FILE_PATHS made the scripts open a fallback file chooser even
# though a file was selected. This helper accepts paths first, then decodes file:// URIs.
marma_selected_files() {
    local -a files=()
    local raw line uri decoded
    _marma_decode_item() {
        local item="$1"
        case "$item" in
            file://*)
                python3 -c 'import sys, urllib.parse; p=urllib.parse.urlparse(sys.argv[1]); print(urllib.parse.unquote(p.path))' "$item" 2>/dev/null || true
                ;;
            *) printf '%s\n' "$item" ;;
        esac
    }
    raw="${NAUTILUS_SCRIPT_SELECTED_FILE_PATHS:-}"
    if [[ -n "$raw" ]]; then
        while IFS= read -r line; do
            [[ -n "$line" ]] && files+=("$(_marma_decode_item "$line")")
        done <<< "$raw"
    fi
    if [[ ${#files[@]} -eq 0 ]]; then
        raw="${NAUTILUS_SCRIPT_SELECTED_URIS:-}"
        if [[ -n "$raw" ]]; then
            while IFS= read -r uri; do
                [[ -z "$uri" ]] && continue
                case "$uri" in
                    file://*)
                        decoded="$(python3 -c 'import sys, urllib.parse; p=urllib.parse.urlparse(sys.argv[1]); print(urllib.parse.unquote(p.path))' "$uri" 2>/dev/null || true)"
                        [[ -n "$decoded" ]] && files+=("$decoded")
                        ;;
                    *) files+=("$uri") ;;
                esac
            done <<< "$raw"
        fi
    fi
    if [[ ${#files[@]} -eq 0 ]]; then
        raw="${NAUTILUS_SCRIPT_NEXT_PANE_SELECTED_FILE_PATHS:-}"
        if [[ -n "$raw" ]]; then
            while IFS= read -r line; do
                [[ -n "$line" ]] && files+=("$line")
            done <<< "$raw"
        fi
    fi
    local _log_dir="${XDG_CACHE_HOME:-$HOME/.cache}/marma-crypto"
    mkdir -p "$_log_dir" 2>/dev/null || true
    printf '%s paths=%s uris=%s next=%s current=%s selected=%s\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        "$([[ -n "${NAUTILUS_SCRIPT_SELECTED_FILE_PATHS:-}" ]] && echo 1 || echo 0)" \
        "$([[ -n "${NAUTILUS_SCRIPT_SELECTED_URIS:-}" ]] && echo 1 || echo 0)" \
        "$([[ -n "${NAUTILUS_SCRIPT_NEXT_PANE_SELECTED_FILE_PATHS:-}" ]] && echo 1 || echo 0)" \
        "${NAUTILUS_SCRIPT_CURRENT_URI:-}" "${#files[@]}" \
        >> "$_log_dir/selection.log" 2>/dev/null || true
    printf '%s\n' "${files[@]}"
}

if [[ -f "$HOME/002_AI/PROJECTS/EDU-VEDI/marma-crypto-protocol/src/marma_watermark.py" ]]; then
    export PATH="$HOME/002_AI/PROJECTS/EDU-VEDI/marma-crypto-protocol/bin:$HOME/.local/bin:$PATH"
    marma-watermark() {
        python3 "$HOME/002_AI/PROJECTS/EDU-VEDI/marma-crypto-protocol/src/marma_watermark.py" "$@"
    }
    export -f marma-watermark 2>/dev/null || true
elif [[ -f "$HOME/ai-debian-admin/deb-packages/marma-crypto-watermark/src/marma_watermark.py" ]]; then
    export PATH="$HOME/ai-debian-admin/deb-packages/marma-crypto-watermark/bin:$HOME/.local/bin:$PATH"
    marma-watermark() {
        python3 "$HOME/ai-debian-admin/deb-packages/marma-crypto-watermark/src/marma_watermark.py" "$@"
    }
    export -f marma-watermark 2>/dev/null || true
fi

# ------------------------------------------------------------------------------
# Seal placement preference: last (default) | first | first-last | all | ask
# env MARMA_SEAL_PAGES overrides the saved ~/.config/marma-crypto/config.json value.
# ------------------------------------------------------------------------------
marma_config_path() {
    printf '%s\n' "${XDG_CONFIG_HOME:-$HOME/.config}/marma-crypto/config.json"
}

marma_get_seal_pages() {
    local spec="${MARMA_SEAL_PAGES:-}"
    local cfg
    cfg="$(marma_config_path)"
    if [[ -z "$spec" && -f "$cfg" ]]; then
        spec="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("seal_pages",""))' "$cfg" 2>/dev/null || true)"
    fi
    case "$spec" in
        first|first-last|all|ask) printf '%s\n' "$spec" ;;
        *) printf 'last\n' ;;
    esac
}

marma_set_seal_pages() {
    local spec="$1"
    local cfg
    cfg="$(marma_config_path)"
    mkdir -p "$(dirname "$cfg")" 2>/dev/null || true
    python3 - "$cfg" "$spec" <<'PYCFG'
import json, sys
path, spec = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(path, encoding="utf-8"))
except Exception:
    data = {}
data["seal_pages"] = spec
json.dump(data, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
PYCFG
}

# Resolve the placement for a signing action. If the user chose "ask", show a radio dialog
# (unless headless / no display); on cancel return 1 so the caller can abort.
marma_resolve_seal_pages() {
    local spec choice
    spec="$(marma_get_seal_pages)"
    if [[ "$spec" != "ask" ]]; then
        printf '%s\n' "$spec"
        return 0
    fi
    if [[ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" || -n "${MARMA_HEADLESS:-}" ]] || ! command -v zenity >/dev/null 2>&1; then
        printf 'last\n'
        return 0
    fi
    choice="$(zenity --list --radiolist \
        --title="$(marma_text "Розміщення печатки — Marma-Crypto" "Seal placement — Marma-Crypto")" \
        --text="$(marma_text "Оберіть, на яких сторінках ставити видиму печатку:" "Choose which pages carry the visible seal:")" \
        --column="" --column="ID" --column="$(marma_text "Сторінки" "Pages")" \
        TRUE "last" "$(marma_text "Остання (сторінка підпису) — рекомендовано" "Last (signature page) — recommended")" \
        FALSE "all" "$(marma_text "Кожна сторінка" "Every page")" \
        FALSE "first-last" "$(marma_text "Перша + остання" "First + last")" \
        FALSE "first" "$(marma_text "Лише перша" "First only")" \
        --hide-column=2 --print-column=2 --width=620 --height=390 2>/dev/null || true)"
    [[ -z "$choice" ]] && return 1
    printf '%s\n' "$choice"
}

marma_text() {
    if [[ "$MARMA_LANG" == "en" ]]; then
        echo "$2"
    else
        echo "$1"
    fi
}

marma_get_window_icon() {
    local candidate
    for candidate in \
        "/usr/share/icons/hicolor/scalable/apps/marma-crypto-watermark.svg" \
        "${XDG_DATA_HOME:-$HOME/.local/share}/icons/Papirus/48x48/mimetypes/application-certificate.svg" \
        "/usr/share/icons/Papirus/48x48/mimetypes/application-certificate.svg"; do
        if [[ -f "$candidate" ]]; then
            echo "$candidate"
            return 0
        fi
    done
    echo "security-high"
}

marma_run_or_warn() {
    local title_uk="$1"
    local title_en="$2"
    shift 2
    local out
    if out=$("$@" 2>&1); then
        return 0
    fi
    marma_warn_dialog "$title_uk" "$title_en" "${out:-Невідома помилка / unknown error}" "${out:-Unknown error}"
    return 1
}

marma_notify() {
    local icon="$1"
    local title_uk="$2"
    local title_en="$3"
    local body_uk="$4"
    local body_en="$5"

    if command -v notify-send >/dev/null 2>&1; then
        local w_icon
        w_icon="$(marma_get_window_icon)"
        local use_icon="$icon"
        [[ -z "$use_icon" ]] && use_icon="$w_icon"

        if [[ "$MARMA_LANG" == "en" ]]; then
            notify-send -a "Marma-Crypto Watermark" -h int:transient:1 -i "$use_icon" "$title_en" "$body_en"
        else
            notify-send -a "Marma-Crypto Watermark" -h int:transient:1 -i "$use_icon" "$title_uk" "$body_uk"
        fi
    fi
}

marma_warn_dialog() {
    local title_uk="$1"
    local title_en="$2"
    local text_uk="$3"
    local text_en="$4"
    local w_icon
    w_icon="$(marma_get_window_icon)"

    if command -v zenity >/dev/null 2>&1; then
        if [[ "$MARMA_LANG" == "en" ]]; then
            zenity --warning --title="$title_en" --text="<b>${title_en}</b>\n\n${text_en}" --width=480 --window-icon="$w_icon" 2>/dev/null || true
        else
            zenity --warning --title="$title_uk" --text="<b>${title_uk}</b>\n\n${text_uk}" --width=480 --window-icon="$w_icon" 2>/dev/null || true
        fi
    fi
}

marma_info_dialog() {
    local title_uk="$1"
    local title_en="$2"
    local text_uk="$3"
    local text_en="$4"
    local w_icon
    w_icon="$(marma_get_window_icon)"

    if command -v zenity >/dev/null 2>&1; then
        if [[ "$MARMA_LANG" == "en" ]]; then
            zenity --info --title="$title_en" --text="<b>${title_en}</b>\n\n${text_en}" --width=520 --window-icon="$w_icon" 2>/dev/null || true
        else
            zenity --info --title="$title_uk" --text="<b>${title_uk}</b>\n\n${text_uk}" --width=520 --window-icon="$w_icon" 2>/dev/null || true
        fi
    fi
}
