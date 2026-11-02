PYTHON ?= python3
SF ?= 1
.PHONY: all sources test serve benchmark performance incremental idempotence report
all:
	$(PYTHON) scripts/run_all.py --sf $(SF)
sources:
	$(PYTHON) scripts/fetch_sources.py
	$(PYTHON) scripts/prepare_population.py
test:
	$(PYTHON) -m unittest discover -s tests -v
serve:
	$(PYTHON) -m http.server 8000 --bind 127.0.0.1 --directory dashboard
benchmark:
	$(PYTHON) scripts/benchmark.py
performance:
	$(PYTHON) scripts/optimisations.py
incremental:
	$(PYTHON) pipeline/run.py --incoming "$(INPUT)"
	$(PYTHON) analytics/run.py
	$(PYTHON) serving/export.py
idempotence:
	$(PYTHON) pipeline/run.py
report:
	$(PYTHON) scripts/build_documents.py


hidden-test:
	$(PYTHON) scripts/test_hidden_drop.py
