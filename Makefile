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
	python -m unittest discover
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
	@echo "test                 : Run all doctests and unit tests"
	@echo "clean                : Housecleaning"
	@echo ""
