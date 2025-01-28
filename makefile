.PHONY: install docker-build-no-cache docker-build docker-run docker-build-and-run requirements tests run env-template help

# Variables
ENV_TEMPLATE := template.env

install:
	pip install --upgrade pip
	pip install uv
	uv install
	uv pip install -r requirements.txt
	make env-template

docker-build-no-cache:
	docker build --no-cache -t rs-interview:dev .

docker-build:
	docker build -t rs-interview:dev .

docker-run:
	docker run --env-file .env -p 8000:8000 rs-interview:dev

docker-build-and-run:
	make docker-build-no-cache && make docker-run

requirements:
	uv pip compile pyproject.toml -o requirements.txt

tests:
	python -m pytest --cov=src --cov-report=term-missing

run:
	uvicorn src.app:app --reload

env-template:
	echo "# Add your environment variables here" > "$(ENV_TEMPLATE)"
	echo "AWS_REGION=\"aws region\"" >> "$(ENV_TEMPLATE)"
	echo "AWS_BEDROCK_MODEL_ID=\"Claude model id\"" >> "$(ENV_TEMPLATE)"

help:
	@echo -e "\n"
	@echo -e "Available commands:"
	@echo -e "===================\n"
	@echo "install                  Install dependencies"
	@echo "docker-build-no-cache    Build docker image without cache"
	@echo "docker-build             Build docker image"
	@echo "docker-run               Run docker image"
	@echo "docker-build-and-run     Build and run docker image"
	@echo "requirements             Compile requirements"
	@echo "tests                    Run tests"
	@echo "run                      Run the application"
	@echo "env-template             Create a template for environment variables"
	@echo "help                     Show this help message"
	@echo -e "\n"
