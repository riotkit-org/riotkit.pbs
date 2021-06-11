"""
Support for Pipenv.lock file
"""

from typing import List
from json import loads


def collect_locked_dependencies(root_dir: str) -> List[str]:
    collected_dependencies: List[str] = []

    with open(f'{root_dir}/Pipfile.lock', 'r') as pipenv_file:
        pipenv = loads(pipenv_file.read())

        if "default" not in pipenv:
            raise Exception('Incorrectly formatted Pipfile.lock, missing "default" section')

        pipfile_dependencies: dict = pipenv['default']

        for name, data in pipfile_dependencies.items():
            dependency_string = '{name}{version}'.format(name=name, version=data['version'])

            if "markers" in data and data['markers']:
                dependency_string += '; {markers}'.format(markers=data['markers'])

            collected_dependencies.append(dependency_string)

    return collected_dependencies
