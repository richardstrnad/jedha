PY27DEVTESTS=cd tests;find ./* -name 'test_*.py' -exec /opt/virtual_env/py27_test/bin/py.test -s {} \;
PY34DEVTESTS=cd tests;find ./* -name 'test_*.py' -exec /opt/virtual_env/py34_test/bin/py.test -s {} \;
BITBUCKETPUSH = $(shell bash -c 'read -s -p "Bitbucket Password: " pwd; hg push "https://mpenning:$$pwd@bitbucket.org/mpenning/nety"')
DOCHOST ?= $(shell bash -c 'read -p "documentation host: " dochost; echo $$dochost')

.PHONY: package
package:
	make clean
	python setup.py sdist
.PHONY: pypi
pypi:
	make clean
	python setup.py sdist; python setup.py register; twine upload dist/* --skip-existing
.PHONY: test
test:
	# Run the doc tests and unit tests
	python tests/test_parser.py
.PHONY: clean
clean:
	find ./* -name '*.pyc' -exec rm {} \;
	find ./* -name '*.so' -exec rm {} \;
	find ./* -name '*.coverage' -exec rm {} \;
	@# A minus sign prefixing the line means it ignores the return value
	-find ./* -path '*__pycache__' -exec rm -rf {} \;
	@# remove all the MockSSH keys
	-find ./* -name '*.key' -exec rm {} \;
	-rm -rf .eggs/
	-rm -rf dist/ jedha.egg-info/ setuptools*
.PHONY: help
help:
	@# An @ sign prevents outputting the command itself to stdout
	@echo "help                 : You figured that out ;-)"
	@echo "pypi                 : Build the project and push to pypi"
	@echo "repo-push            : Build the project and push to bitbucket / github"
	@echo "test                 : Run all doctests and unit tests"
	@echo "devpkgs              : Get all dependencies for the dev environment"
	@echo "devtest              : Run tests - Specific to Mike Pennington's build env"
	@echo "coverage             : Run tests with coverage - Specific to this build env"
	@echo "flake                : Run PyFlake code audit w/ McCabe complexity"
	@echo "clean                : Housecleaning"
	@echo "parse-ios            : Parse configs/sample_01.ios with default args"
	@echo "parse-ios-factory    : Parse configs/sample_01.ios with factory=True"
	@echo "parse-iosxr-banner   : Parse an interesting IOSXR banner"
	@echo "perf-acl             : cProfile configs/sample_05.ios (100 acls)"
	@echo "perf-factory-intf    : cProfile configs/sample_06.ios (many intfs, factory=True)"
	@echo ""
