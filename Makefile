PYTHON := python3

GENERATED_ASSETS := \
	tokyo-night-v2-bg.png \
	chrome-theme/images/theme_ntp_background.png \
	chrome-theme/images/theme_frame.png \
	chrome-theme/images/theme_toolbar.png \
	chrome-theme/images/theme_tab_background.png

.PHONY: check regen

## check — regenerate assets and verify they match what is committed.
##         Restores committed files afterwards (non-destructive).
check:
	@echo "Running generators..."
	@$(PYTHON) gen_bg2.py
	@$(PYTHON) gen_chrome_theme.py
	@echo ""
	@changed=$$(git diff --name-only -- $(GENERATED_ASSETS)); \
	git checkout -- $(GENERATED_ASSETS) 2>/dev/null; \
	if [ -n "$$changed" ]; then \
		echo "FAIL: the following assets are out of date with their generators:"; \
		echo "$$changed" | sed 's/^/  /'; \
		echo ""; \
		echo "Run 'make regen' and commit the result."; \
		exit 1; \
	else \
		echo "OK: all generated assets match their committed versions."; \
	fi

## regen — regenerate assets in-place and stage them for commit.
regen:
	@echo "Regenerating assets..."
	$(PYTHON) gen_bg2.py
	$(PYTHON) gen_chrome_theme.py
	git add $(GENERATED_ASSETS)
	@echo ""
	@echo "Assets staged. Review with 'git diff --cached' then commit."
