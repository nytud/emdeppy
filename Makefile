all: test

test:
	python3 -m emdeppy -i parse_test.xtsv

build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist/ build/ emdeppy.egg-info/

clean-build: clean build
