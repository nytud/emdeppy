DIR := ${CURDIR}
all:
	@echo "See Makefile for possible targets!"

dist/*.whl dist/*.tar.gz:
	@echo "Building package..."
	python3 setup.py sdist bdist_wheel

build: dist/*.whl dist/*.tar.gz

install-user: build
	@echo "Installing package to user..."
	pip3 install dist/*.whl

test:
	@echo "Running tests..."
	cd /tmp && python3 -m emdeppy -i $(DIR)/tests/parse_kutya.in | diff - $(DIR)/tests/parse_kutya.out && cd ${CURDIR}

install-user-test: install-user test
	@echo "The test was completed successfully!"

ci-test: install-user-test

uninstall:
	@echo "Uninstalling..."
	pip3 uninstall -y emdeppy

install-user-test-uninstall: install-user-test uninstall

clean:
	rm -rf dist/ build/ emdeppy.egg-info/

clean-build: clean build
