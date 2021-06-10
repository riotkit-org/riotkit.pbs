Python Build Simplified
=======================

Lighter alternative to PBR. Created to support easily multiple namespace packages built from single repository.
Ultra simple, allows to have almost empty setup.py file, while keeping all information in setup.json

**Features:**
- External dependencies in `requirements-external.txt`
- Internal dependencies (packages from same repository) in `requirements-subpackages.txt`
- All arguments that goes to setup() are placed as dictionary in `setup.json` file, there is no magic there
- README.md and README.rst (in order) are loaded automatically as long description
- Uses SCM plugin (setuptools_scm) by default

Multiple-package repository
---------------------------




Single-package repository
-------------------------

**project.toml**

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.0", "riotkit.pbs>=1.0"]
```

**setup.py**

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

```json
{
    "name": "rkd.process",
    "author": "RiotKit non-profit organization",
    "author_email": "riotkit@riseup.net",
    "description": "rkd.process provides easy process interaction and output capturing/redirecting, wraps subprocess from Python's standard library.",
    "home_page": "https://github.com/riotkit-org",
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

```
some-package>=1.0
```

**MANIFEST.in**

```bash
recursive-exclude tests *
recursive-exclude example *
include requirements-external.txt
include requirements-subpackages.txt
include setup.json
```
