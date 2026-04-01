<div align="center">

![Black](./colors/black.png) ![Bright Black](./colors/bright_black.png) ![Red](./colors/red.png) ![Bright Red](./colors/bright_red.png) ![Green](./colors/green.png) ![Bright Green](./colors/bright_green.png) ![Yellow](./colors/yellow.png) ![Bright Yellow](./colors/bright_yellow.png) ![Blue](./colors/blue.png) ![Bright Blue](./colors/bright_blue.png) ![Magenta](./colors/magenta.png) ![Bright Magenta](./colors/bright_magenta.png) ![Cyan](./colors/cyan.png) ![Bright Cyan](./colors/bright_cyan.png) ![White](./colors/white.png) ![Bright White](./colors/bright_white.png)

# iTerm2 – Tokyo Night Color Theme

A [iTerm2](https://iterm2.com/) color theme inspired by [Tokyo Night](https://github.com/tokyo-night/tokyo-night-vscode-theme) and [Catppuccin](https://github.com/catppuccin/catppuccin).

<br/>

## Themes

| File | Description |
|---|---|
| [`tokyo-night.itermcolors`](./tokyo-night.itermcolors) | Original theme |
| [`tokyo-night-v2.itermcolors`](./tokyo-night-v2.itermcolors) | v2 — improved contrast, distinct normal/bright pairs |

<br/>

## iTerm2 Installation

**`Preferences`** › **`Profiles`** › **`Colors`** › **`Color Presets`** › **`Import`** › select `.itermcolors` file

###### Alternatively, copy the color values from the [table](#colors) below into your iTerm2 color settings manually.

<br/>

<img height="100%" alt="example_1" src="./example_1.png">

<br/>

## Backgrounds

### iTerm2 background

An aurora-wave background is included for use with iTerm2's background image feature.

**`Preferences`** › **`Profiles`** › **`Window`** › **`Background Image`** › select `tokyo-night-v2-bg.png`

Set opacity to **20–35%** to keep text readable.

### Desktop background

A 3440×1440 ultrawide desktop wallpaper with a stylised city silhouette and aurora sky is included as [`tokyo-night-desktop-bg.png`](./tokyo-night-desktop-bg.png).

**System Settings → Wallpaper → Add Photo** → select `tokyo-night-desktop-bg.png`

<br/>

## Chrome Theme

A matching Chrome browser theme is included in [`chrome-theme/`](./chrome-theme/).

1. Open `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `chrome-theme/` folder

Colors the frame, tab strip, address bar, toolbar icons, and New Tab Page to match the Tokyo Night v2 palette.

<br/>

## Starship Prompt

A matching [Starship](https://starship.rs/) prompt config is included as [`starship.toml`](./starship.toml). Copy it to `~/.config/starship.toml`.

<br/>

## Slack

A matching sidebar theme is in [`slack-theme.txt`](./slack-theme.txt).

1. In Slack open **Preferences → Themes**
2. Scroll to the bottom and click **Open theme creator**
3. Paste the string from `slack-theme.txt` into the custom theme field

| Colour | Hex | Used for |
|---|---|---|
| Sidebar BG | `#24263E` | Sidebar background |
| Menu hover | `#2E3257` | Hovered channel/DM row |
| Active item | `#7AA2F7` | Active channel highlight |
| Active item text | `#1A1B27` | Text on active channel |
| Hover item | `#2A2D4A` | Hover row background |
| Sidebar text | `#BBC6F6` | Channel and DM names |
| Active presence | `#4EF4DF` | Online dot |
| Mention badge | `#F7768E` | Unread / mention counter |
| Top nav BG | `#1A1B27` | Top bar background |
| Top nav text | `#BBC6F6` | Top bar icons and text |

<br/>

## Colors

### Tokyo Night (original)

| Color Name    | Normal                                     | Bright                                                   |
| ------------- | ------------------------------------------ | -------------------------------------------------------- |
| Black         | `#2A2734` ![Black](./colors/black.png)     | `#454258` ![Bright Black](./colors/bright_black.png)     |
| Red           | `#E2514F` ![Red](./colors/red.png)         | `#E2514F` ![Bright Red](./colors/bright_red.png)         |
| Green         | `#00BCDB` ![Green](./colors/green.png)     | `#4EF4E0` ![Bright Green](./colors/bright_green.png)     |
| Yellow        | `#E1C381` ![Yellow](./colors/yellow.png)   | `#E1C281` ![Bright Yellow](./colors/bright_yellow.png)   |
| Blue          | `#5234B2` ![Blue](./colors/blue.png)       | `#7C65C3` ![Bright Blue](./colors/bright_blue.png)       |
| Magenta       | `#E59E50` ![Magenta](./colors/magenta.png) | `#E59E50` ![Bright Magenta](./colors/bright_magenta.png) |
| Cyan          | `#29B7E6` ![Cyan](./colors/cyan.png)       | `#24D5F7` ![Bright Cyan](./colors/bright_cyan.png)       |
| White         | `#9A84EE` ![White](./colors/white.png)     | `#EDEBFF` ![Bright White](./colors/bright_white.png)     |

### Tokyo Night v2 (improved contrast)

![Black](./colors-v2/black.png) ![Bright Black](./colors-v2/bright_black.png) ![Red](./colors-v2/red.png) ![Bright Red](./colors-v2/bright_red.png) ![Green](./colors-v2/green.png) ![Bright Green](./colors-v2/bright_green.png) ![Yellow](./colors-v2/yellow.png) ![Bright Yellow](./colors-v2/bright_yellow.png) ![Blue](./colors-v2/blue.png) ![Bright Blue](./colors-v2/bright_blue.png) ![Magenta](./colors-v2/magenta.png) ![Bright Magenta](./colors-v2/bright_magenta.png) ![Cyan](./colors-v2/cyan.png) ![Bright Cyan](./colors-v2/bright_cyan.png) ![White](./colors-v2/white.png) ![Bright White](./colors-v2/bright_white.png)

| Color Name | Normal | Bright |
|---|---|---|
| Black      | `#2A2734` ![Black](./colors-v2/black.png)           | `#454159` ![Bright Black](./colors-v2/bright_black.png)     |
| Red        | `#F7768E` ![Red](./colors-v2/red.png)               | `#FF9E9C` ![Bright Red](./colors-v2/bright_red.png)         |
| Green      | `#00BCDB` ![Green](./colors-v2/green.png)           | `#4EF4DF` ![Bright Green](./colors-v2/bright_green.png)     |
| Yellow     | `#E1C381` ![Yellow](./colors-v2/yellow.png)         | `#FFD580` ![Bright Yellow](./colors-v2/bright_yellow.png)   |
| Blue       | `#7AA2F7` ![Blue](./colors-v2/blue.png)             | `#A9B8FF` ![Bright Blue](./colors-v2/bright_blue.png)       |
| Magenta    | `#E69F51` ![Magenta](./colors-v2/magenta.png)       | `#FFB86C` ![Bright Magenta](./colors-v2/bright_magenta.png) |
| Cyan       | `#2AB7E7` ![Cyan](./colors-v2/cyan.png)             | `#24D5F8` ![Bright Cyan](./colors-v2/bright_cyan.png)       |
| White      | `#9B84EE` ![White](./colors-v2/white.png)           | `#EEEBFF` ![Bright White](./colors-v2/bright_white.png)     |

<br/>

## Contributing

The PNG assets in this repo are generated by Python scripts. After editing a generator, run:

```sh
make regen   # regenerate and stage the updated PNGs
make check   # verify committed PNGs match their generators (CI-safe)
```

Requires Python 3 with `Pillow` and `numpy` (`pip install pillow numpy`).

<br/>

## Roadmap

- [x] [Tokyo Night](./tokyo-night.itermcolors)
- [x] [Tokyo Night v2](./tokyo-night-v2.itermcolors)
- [ ] Tokyo Night Storm
- [ ] Tokyo Night Storm v2

</div>
