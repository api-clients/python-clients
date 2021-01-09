PYTHONPATH=.
TESTS=tests/
MOCK_SERVER=${TESTS}server/mock_server.py
REQ=requirements/dev
PIP_CONFIG_FILE=.secrets/pip_private.conf
CONDA=conda

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


.PHONY: config publish-package clean deps deps-dev run run-mock test-integration test-unit test


ENVS=PYTHONPATH=${PYTHONPATH} PIP_CONFIG_FILE=${PIP_CONFIG_FILE}


config:
	$(ENVS) $(CONDA) create --name clients python=3.8

publish:
	$(ENVS) $(PYTHON) setup.py bdist_wheel upload -r python-clients

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf http_python_clients.egg-info
	rm -rf data/test/temp/

deps:
	PIP_CONFIG_FILE=${PIP_CONFIG_FILE}
	$(ENVS) $(PIP) install -r $(REQ) --use-feature=2020-resolver

run:
	$(ENVS) $(PYTHON) ${MOCK_SERVER}

test:
	$(ENVS_TEST) $(PYTEST) -v -l ${TESTS}
