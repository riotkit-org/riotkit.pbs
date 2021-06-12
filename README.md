Python Build Simplified
=======================

Lighter alternative to PBR. Created to support easily multiple namespace packages built from single repository.
Ultra simple, allows to have almost empty setup.py file, while keeping all information in setup.json

**Optionally integrates with Pipfile.lock which means you can stop using requirements.txt and use fully reproducible builds on production without doing pip freeze manually**


**Features:**
- External dependencies in `requirements-external.txt`
- Internal dependencies (packages from same repository) in `requirements-subpackages.txt`
- All arguments that goes to setup() are placed as dictionary in `setup.json` file, there is no magic there
- README.md and README.rst (in order) are loaded automatically as long description
- Uses SCM plugin (setuptools_scm) by default
- Optional Pipfile.lock from Pipenv support
- Command `./setup.py --quiet freeze_dependencies` to print dependencies in requirements.txt format
- Command `./setup.py install_dependencies` to install dependencies using pip


Getting started
---------------

**project.toml**

Needs to be configured, so the pip and pipenv would know the dependencies to run setup.py file

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.0", "riotkit.pbs>=1.0"]
```

**setup.py**

The usage of PBS is really simple, import and unpack a dictionary. 
Optionally override values as you wish - there is no magic, everything is passed explicitly, so you can print it or pass to setup()

```python
#!/usr/bin/env python3
from setuptools import setup
from riotkit.pbs import get_setup_attributes

# advanced usage: override any attribute
attributes = get_setup_attributes(git_root_dir='../../')
attributes['long_description'] += "\nBuilt using Riotkit Python Build Simplified"

setup(
    **attributes
)
```

**setup.json**

Again, there is no any magic. Every key there is an attribute that should go to setup() from setuptools.
Please look at setuptools documentation for list of available attributes, you can find it there: https://setuptools.readthedocs.io/en/latest/references/keywords.html

```json
{
    "name": "rkd.process",
    "author": "RiotKit non-profit organization",
    "author_email": "riotkit@riseup.net",
    "description": "rkd.process provides easy process interaction and output capturing/redirecting, wraps subprocess from Python's standard library.",
    "url": "https://github.com/riotkit-org",
    "license": "Apache-2",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only"
    ],
    "keywords": ["rkd", "riotkit", "anarchism", "output capturing", "output", "subprocess"]
}
```

**requirements-external.txt**

It's a regular `requirements.txt` replacement, with all versions there.

```
some-package>=1.0
```

**MANIFEST.in**

Points out which files should be included in a distribution package.

```bash
recursive-exclude tests *
recursive-exclude example *
include requirements-external.txt
include requirements-subpackages.txt
include setup.json
```

Additional work to do in multiple-package repository
----------------------------------------------------

Multiple-package repositories are used to keep versioning in synchronization for multiple packages.
Some of packages could be dependent on each other, but possible to install standalone.

**See real use case:** https://github.com/riotkit-org/riotkit-do/tree/master/src/core

**requirements-subpackages.txt**

A dynamic version of `requirements.txt`, where a simple templating mechanism is available to allow
creating dependencies to packages that are released together with current package from same repository.

```bash
rkd.process >= {{ current_version }}, < {{ next_minor_version }}
```

**Available variables:**
- current_version: Example 1.3.1.2
- next_minor_version: Example 1.4
- next_major_version: Example 2.0

Pipenv support
--------------

Pipenv support could be optionally enabled. In this case all standard dependencies from `Pipfile.lock` would be frozen
and added to `install_requires` automatically.

**setup.py**

```python
#!/usr/bin/env python3
from setuptools import setup
from riotkit.pbs import get_setup_attributes

setup(
    **get_setup_attributes(pipenv=True)
)
```

Debugging
---------

PBS is not performing any magic inside, so there is a possibility to just print the attributes that would be used in `setup()`

**setup.py**

```python
#!/usr/bin/env python3
from setuptools import setup
from riotkit.pbs import get_setup_attributes
import pprint

attributes = get_setup_attributes(git_root_dir='../../')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(attributes)

# setup(
#     **attributes
# )
```
