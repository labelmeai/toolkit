all:
	@echo '## Make commands ##'
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

lint:
	mypy --package labelme_toolkit
	ruff format --check
	ruff check

format:
	ruff format
	ruff check --fix

test:
	python -m pytest -n auto -v labelme_toolkit

clean:
	rm -rf build dist *.egg-info

build: clean
	python -m build --sdist --wheel

publish: build
	python -m twine upload dist/labelme_toolkit-*
