
PYTHONPATH=.

REQ_PRIVATE=requirements.private
REQ_DEV=requirements/dev
REQ_PRIVATE=requirements.private
PIP_CONFIG_FILE=.deploy/.secrets/pip_private.conf



ifndef PYTHON
	PYTHON=python
endif

ifndef PYTEST
	PYTEST=pytest
endif
ifndef PIP
	PIP=pip
endif
ifndef TEST_SUBFOLDER
	TEST_SUBFOLDER=./
endif




.PHONY: config build publish clean deps run run-env run-full run-rebuild test-integration test-unit test


ENVS=PYTHONPATH=${PYTHONPATH}

deps-dev:
	$(info $(ENVS))
	$(ENVS) $(PIP) install -r $(REQ_DEV)
# 	PIP_CONFIG_FILE=${PIP_CONFIG_FILE} $(ENVS) $(PIP) install -r $(REQ_PRIVATE)


publish-package:
# 	$(ENVS) $(PYTHON) setup.py bdist_wheel upload -r private_pypi
	$(ENVS) $(PYTHON) setup.py bdist_wheel upload -r pypi_egor


clean:
	rm -rf build/
	rm -rf dist/
	rm -rf python-clients.egg-info
	rm -rf data/test/temp/

