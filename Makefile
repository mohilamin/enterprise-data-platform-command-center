PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt
generate-catalog:
	$(PYTHON) -m src.data_generation.generate_data_product_catalog
generate-signals:
	$(PYTHON) -m src.data_generation.generate_platform_signals
generate-incidents:
	$(PYTHON) -m src.data_generation.generate_incident_scenarios
run-pipeline:
	$(PYTHON) -m src.pipeline.run_all
test:
	$(PYTHON) -m pytest
lint:
	$(PYTHON) -m ruff check .
format:
	$(PYTHON) -m ruff format .
dashboard:
	streamlit run src/dashboard/app.py
api:
	uvicorn src.api.main:app --reload
docker-up:
	docker compose up --build
docker-down:
	docker compose down
