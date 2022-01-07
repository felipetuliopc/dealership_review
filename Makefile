freeze:
	pip freeze > requirements.txt

install_requirements:
	pip install -r ./requirements.txt

lint:
	find . -type f -name "*.py" -not -path "./env/*" -not -path "./venv/*" | xargs pylint
