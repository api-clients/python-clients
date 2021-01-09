## Project structure

### [data/](data/)

This folder must consists the data of package. We think to a large data file must dumps to any storage (
databases, file storage, git LFS, docs and other). Most part of data here are test's data.

### data/test/

Files for tests

### data/docs/

Design and user documents

### [.secrets/](.secrets/)

Files for publishing package. Here you must save `.pypirc` and `pip_private.conf`. You can read more about this files
[here](https://github.com/U-Company/notes/blob/master/deployments/README.md).

### [python_clients/](python_clients/) 

Package for publishing in registry.

### [tests/](tests/)

This directory consists tests.

### [makefile](makefile)

Makefile is given interface for control of package: dependencies, test, deploying.
  
### [setup.py](setup.py)

This is template for configuration of package of setuptools package.
  
### [info.py](info.py)

This file consists version and package's name.
