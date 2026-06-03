PYTHON  := python3
NODE    := node
SCRIPTS := scripts

.PHONY: help publish watch health jobs install-py install-node clean

help:
	@echo ""
	@echo "  WordPress Automation — Available commands"
	@echo "  ─────────────────────────────────────────"
	@echo "  make publish       Launch Tkinter GUI publisher"
	@echo "  make watch         Start Node.js folder watcher"
	@echo "  make health        Run WordPress health check"
	@echo "  make jobs          Fetch and email daily job digest"
	@echo "  make install-py    Install Python dependencies"
	@echo "  make install-node  Install Node.js dependencies"
	@echo "  make clean         Remove build artefacts"
	@echo ""

publish:
	$(PYTHON) $(SCRIPTS)/wp_publisher.py

watch:
	$(NODE) $(SCRIPTS)/folder_watcher.js

health:
	$(PYTHON) $(SCRIPTS)/wp_health_check.py

jobs:
	$(PYTHON) $(SCRIPTS)/job_hunter.py

install-py:
	pip install requests beautifulsoup4 lxml

install-node:
	cd $(SCRIPTS) && npm init -y && npm install chokidar node-fetch dotenv

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
