all:
	@echo '## Make commands ##'
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

PACKAGE_NAME:=labelme_toolkit

mypy:
	mypy --package $(PACKAGE_NAME)

lint:
	ruff format --check
	ruff check

format:
	ruff format
	ruff check --fix

test:
	python -m pytest -n auto -v $(PACKAGE_NAME)

clean:
	rm -rf build dist *.egg-info

build: clean
	python -m build --sdist --wheel

publish: build
	python -m twine upload dist/$(PACKAGE_NAME)-*
