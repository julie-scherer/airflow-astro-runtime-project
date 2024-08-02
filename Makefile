# Virtual environment setup
.PHONY: venv
venv: .venv
	@echo "Virtual environment is ready."

.venv: requirements.txt
	python3 -m venv .venv
	@echo "Virtual environment created in scripts folder."
	@. .venv/bin/activate && pip install --upgrade pip && pip install -r ./requirements.txt
	@touch .venv

# NEW VERSION
.PHONY: conn
conn:
	@echo "Setting up secrets..."
	@if [ -d .venv ]; then rm -rf .venv; fi
	@python3 -m venv .venv
	@. .venv/bin/activate && \
		pip install --upgrade pip && \
		pip install --no-cache-dir -r include/secrets-backend/requirements.txt && \
		python include/secrets-backend/aws_connection.py && \
		python include/secrets-backend/postgres_connection.py && \
		python include/secrets-backend/trino_connection.py
	

# OG VERSION
.PHONY: conn
conn:
	@echo "Setting up secrets..."
	@if [ -d .venv ]; then rm -rf .venv; fi
	@python3 -m venv .venv
	@. .venv/bin/activate && \
		pip install --upgrade pip && \
		pip install apache-airflow apache-airflow-providers-amazon apache-airflow-providers-postgres apache-airflow-providers-postgres[amazon] python-dotenv && \
		python3 include/aws_connection.py 
		# && \
		# python3 include/postgres_connection.py
