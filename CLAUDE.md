# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an iTerm2 color theme inspired by [Tokyo Night](https://github.com/tokyo-night/tokyo-night-vscode-theme) and [Catppuccin](https://github.com/catppuccin/catppuccin). There is no build system, package manager, or test suite — it is a pure static asset repository.

## Repository Structure

- `tokyo-night.itermcolors` — The theme file (Apple plist/XML format). This is the primary deliverable.
- `colors/` — PNG swatches (16x16 px) for each of the 16 ANSI colors, used in README.md.
- `example_1.png` — Screenshot used in README.md.
- `README.md` — Contains the color palette table with hex values and the installation instructions.

## Color Format

`tokyo-night.itermcolors` uses Apple's plist XML format. Colors are stored as floating-point sRGB components (0.0–1.0) for Red, Green, Blue, and Alpha. To convert from hex: divide each 8-bit channel by 255.

The defined color keys are:
- `Ansi 0`–`Ansi 7`: Normal ANSI colors (Black, Red, Green, Yellow, Blue, Magenta, Cyan, White)
- `Ansi 8`–`Ansi 15`: Bright variants of the above
- `Background Color`, `Foreground Color`, `Bold Color`, `Cursor Color`, `Cursor Text Color`, `Cursor Guide Color`, `Selection Color`, `Selected Text Color`, `Link Color`, `Badge Color`, `Tab Color`

## Color Palette (Hex)

| Name          | Normal    | Bright    |
|---------------|-----------|-----------|
| Black         | `#2A2734` | `#454258` |
| Red           | `#E2514F` | `#E2514F` |
| Green         | `#00BCDB` | `#4EF4E0` |
| Yellow        | `#E1C381` | `#E1C281` |
| Blue          | `#5234B2` | `#7C65C3` |
| Magenta       | `#E59E50` | `#E59E50` |
| Cyan          | `#29B7E6` | `#24D5F7` |
| White         | `#9A84EE` | `#EDEBFF` |

## Roadmap

Planned variants (not yet created):
- Tokyo Night v2
- Tokyo Night Storm
- Tokyo Night Storm v2

Each variant should be a separate `.itermcolors` file following the same plist structure.

## Installation

Import `tokyo-night.itermcolors` via iTerm2: **Preferences → Profiles → Colors → Color Presets → Import**.
