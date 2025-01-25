.PHONY: install run-tests

install:
	pip install --upgrade pip
	pip install uv
	uv install
	uv pip install -r requirements.txt
	touch .env
	echo "# Add your environment variables here" > .env
	echo "AWS_REGION=your-region" >> .env
	echo "AWS_BEDROCK_MODEL_ID=your-model-id" >> .env

run-tests:
	python -m pytest --cov=src --cov-report=term-missing

docker-build-no-cache:
	docker build --no-cache -t rs-interview:dev .

docker-build:
	docker build -t rs-interview:dev .

docker-run:
	docker run --env-file .env -p 7000:8000 rs-interview:dev

docker-build-and-run:
	make docker-build-no-cache && make docker-run

requirements:
	uv pip compile pyproject.toml -o requirements.txt