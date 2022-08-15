isort:
	isort ./app ./tests

format: isort
	black .

type_check:
	mypy ./app ./tests

test:
	pytest --cov=app/
