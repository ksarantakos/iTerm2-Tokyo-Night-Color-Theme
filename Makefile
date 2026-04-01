PYTHON := python3

COLORS_V2 := \
	colors-v2/black.png        colors-v2/bright_black.png \
	colors-v2/red.png          colors-v2/bright_red.png \
	colors-v2/green.png        colors-v2/bright_green.png \
	colors-v2/yellow.png       colors-v2/bright_yellow.png \
	colors-v2/blue.png         colors-v2/bright_blue.png \
	colors-v2/magenta.png      colors-v2/bright_magenta.png \
	colors-v2/cyan.png         colors-v2/bright_cyan.png \
	colors-v2/white.png        colors-v2/bright_white.png

# All files produced by the generator scripts.
# Includes manifest.json, which gen_chrome_theme.py also rewrites.
ALL_ASSETS := \
	tokyo-night-bg.png \
	tokyo-night-v2-bg.png \
	$(COLORS_V2) \
	chrome-theme/manifest.json \
	chrome-theme/images/theme_ntp_background.png \
	chrome-theme/images/theme_frame.png \
	chrome-theme/images/theme_toolbar.png \
	chrome-theme/images/theme_tab_background.png

.PHONY: check regen

## check — regenerate assets and verify they match what is committed.
##
## Non-destructive: saves a copy of each asset before running the generators
## and restores that copy afterwards, preserving any unstaged local edits.
## Compares generated output against HEAD (committed), not the index.
check:
	@echo "Saving working-tree state..."
	@mkdir -p .check-saved/colors-v2 .check-saved/chrome-theme/images
	@for f in $(ALL_ASSETS); do cp "$$f" ".check-saved/$$f" 2>/dev/null || true; done
	@echo "Running generators..."
	@$(PYTHON) gen_bg.py
	@$(PYTHON) gen_bg2.py
	@$(PYTHON) gen_swatches.py
	@$(PYTHON) gen_chrome_theme.py
	@echo ""
	@fail=0; \
	for f in $(ALL_ASSETS); do \
		if git diff --quiet HEAD -- "$$f" 2>/dev/null; then \
			echo "OK    $$f"; \
		else \
			echo "FAIL  $$f"; fail=1; \
		fi; \
	done; \
	echo ""; \
	echo "Restoring working-tree state..."; \
	for f in $(ALL_ASSETS); do \
		[ -f ".check-saved/$$f" ] && cp ".check-saved/$$f" "$$f"; \
	done; \
	rm -rf .check-saved; \
	[ $$fail -eq 0 ] \
		&& echo "All assets match." \
		|| { echo "One or more assets are out of date — run 'make regen' and commit."; exit 1; }

## regen — regenerate assets in-place and stage them for commit.
regen:
	$(PYTHON) gen_bg.py
	$(PYTHON) gen_bg2.py
	$(PYTHON) gen_swatches.py
	$(PYTHON) gen_chrome_theme.py
	git add $(ALL_ASSETS)
	@echo ""
	@echo "Assets staged. Review with 'git diff --cached' then commit."
