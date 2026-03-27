PYTHON := python3

# All files produced by the generator scripts.
# Includes manifest.json, which gen_chrome_theme.py also rewrites.
ALL_ASSETS := \
	tokyo-night-bg.png \
	tokyo-night-v2-bg.png \
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
	@mkdir -p .check-saved/chrome-theme/images .check-saved
	@for f in $(ALL_ASSETS); do cp "$$f" ".check-saved/$$f" 2>/dev/null || true; done
	@echo "Running generators..."
	@$(PYTHON) gen_bg.py
	@$(PYTHON) gen_bg2.py
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
	$(PYTHON) gen_chrome_theme.py
	git add $(ALL_ASSETS)
	@echo ""
	@echo "Assets staged. Review with 'git diff --cached' then commit."
