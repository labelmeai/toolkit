all:
	@echo '## Make commands ##'
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

PACKAGE_NAME:=labelme_toolkit

install:
	uv sync --dev

mypy:
	uv run mypy --package $(PACKAGE_NAME)

lint:
	uv run ruff format --check
	uv run ruff check

format:
	uv run ruff format
	uv run ruff check --fix

test:
	uv run pytest -n auto -v $(PACKAGE_NAME)

clean:
	rm -rf build dist *.egg-info

build: clean
	uv run python -m build --sdist --wheel

# upload: build
# 	python -m twine upload dist/$(PACKAGE_NAME)-*
#
# publish: build upload
