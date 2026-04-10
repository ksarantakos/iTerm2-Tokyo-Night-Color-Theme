"""
Generate a Tokyo Night Firefox theme extension.

Output: firefox-theme/
  manifest.json

Load in Firefox via about:debugging → "This Firefox" → "Load Temporary Add-on"
→ select firefox-theme/manifest.json

For permanent installation, zip the folder and rename to .xpi, or submit to
addons.mozilla.org.
"""
import os
import json

# ── Palette (Tokyo Night v2) ──────────────────────────────────────────────────
BG        = "#1A1B27"   # main background
BG_DARK   = "#13141E"   # darker background
BG_MID    = "#1E2036"   # mid-tone (toolbar)
BG_LIGHT  = "#24283B"   # lighter background (input fields)
FG        = "#BBC6F6"   # foreground / text
FG_DIM    = "#565F89"   # dimmed text
BLUE      = "#7AA2F7"
BLUE_BR   = "#A9B8FF"
CYAN      = "#2AB7E7"
CYAN_BR   = "#24D5F8"
GREEN     = "#00BCDB"
GREEN_BR  = "#4EF4DF"
PURPLE    = "#9B84EE"
RED       = "#F7768E"
ORANGE    = "#E69F51"

OUT_DIR = os.path.join(os.path.dirname(__file__), "firefox-theme")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Manifest ──────────────────────────────────────────────────────────────────
# Firefox theme manifest v2 format
# Reference: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/theme

MANIFEST = {
    "manifest_version": 2,
    "name": "Tokyo Night",
    "version": "1.0",
    "description": "Tokyo Night dark theme — inspired by tokyo-night-vscode and Catppuccin.",
    "browser_specific_settings": {
        "gecko": {
            "id": "tokyo-night-theme@iterm2-tokyo-night"
        }
    },
    "theme": {
        "colors": {
            # Frame (window chrome)
            "frame": BG,
            "frame_inactive": BG_DARK,

            # Tab bar
            "tab_background_text": FG,
            "tab_selected": BG_MID,
            "tab_text": FG,
            "tab_line": BLUE,
            "tab_loading": CYAN,

            # Toolbar (navigation bar)
            "toolbar": BG_MID,
            "toolbar_text": FG,
            "toolbar_field": BG_LIGHT,
            "toolbar_field_text": FG,
            "toolbar_field_border": BG_MID,
            "toolbar_field_focus": BG_LIGHT,
            "toolbar_field_text_focus": FG,
            "toolbar_field_border_focus": BLUE,
            "toolbar_field_highlight": BLUE,
            "toolbar_field_highlight_text": BG,
            "toolbar_top_separator": "transparent",
            "toolbar_bottom_separator": BG_DARK,
            "toolbar_vertical_separator": BG_DARK,

            # Bookmarks
            "bookmark_text": FG,

            # Icons
            "icons": FG,
            "icons_attention": ORANGE,

            # Buttons
            "button_background_hover": BG_LIGHT,
            "button_background_active": PURPLE,

            # Popups (menus, dropdowns)
            "popup": BG_MID,
            "popup_text": FG,
            "popup_border": BG_DARK,
            "popup_highlight": BLUE,
            "popup_highlight_text": BG,

            # Sidebar
            "sidebar": BG,
            "sidebar_text": FG,
            "sidebar_border": BG_DARK,
            "sidebar_highlight": BLUE,
            "sidebar_highlight_text": BG,

            # New Tab Page
            "ntp_background": BG,
            "ntp_card_background": BG_MID,
            "ntp_text": FG,
        }
    }
}

manifest_path = os.path.join(OUT_DIR, "manifest.json")
with open(manifest_path, "w") as f:
    json.dump(MANIFEST, f, indent=2)
print(f"Wrote {manifest_path}")

print()
print("Done! Load the theme in Firefox:")
print("  about:debugging → 'This Firefox' → 'Load Temporary Add-on'")
print("  → select firefox-theme/manifest.json")
print()
print("For permanent installation:")
print("  1. Zip the firefox-theme folder contents")
print("  2. Rename .zip to .xpi")
print("  3. Drag into Firefox or submit to addons.mozilla.org")
