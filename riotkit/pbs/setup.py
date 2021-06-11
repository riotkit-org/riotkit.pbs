#!/usr/bin/env python3

# =================================================================
#  RiotKit's setuptools wrapper
#  ----------------------------
#  - Does not use PBR (because of requirements.txt enforcement)
#  - Uses setup.json as input dictionary to setup()
#  - Uses setuptools_scm to know self version
# =================================================================

import os
import re
from typing import List, Tuple
from setuptools_scm import get_version
from json import load as json_load
from .pipenv import collect_locked_dependencies


def _local_scheme(version):
    return ""


def _calculate_version(root_dir: str) -> Tuple[str, str, str]:
    current_version = get_version(root=root_dir)
    parts = current_version.split('.')
    next_minor_version = '.'.join([parts[0], str(int(parts[1]) + 1)])
    next_major_version = '.'.join([str(int(parts[0]) + 1), '0'])

    return current_version, next_minor_version, next_major_version


def _render_template(template: str, variables: dict) -> str:
    """
    Renders a pseudo-template

    :param template:
    :param variables:
    :return:
    """

    for name, value in variables.items():
        template = re.sub("{{(\\s*)" + re.escape(name) + "(\\s*)}}", value, template)

    return template


def _calculate_requirements(current_version: str,
                            next_minor_version: str,
                            next_major_version: str,
                            root_dir: str) -> List[str]:
    requirements = []

    filenames = [
        'requirements.txt',
        'requirements-external.txt',
        'requirements-subpackages.txt',
        'requirements-internal.txt'
    ]

    for filename in filenames:
        if os.path.isfile(root_dir + '/' + filename):
            with open(root_dir + '/' + filename) as f:
                for line in f.readlines():
                    if not line.strip():
                        continue

                    # do not allow dynamic requirements.txt
                    if filename == 'requirements.txt':
                        requirements.append(line.strip())
                        continue

                    requirements.append(
                        _render_template(line.strip(), {
                            'current_version': current_version,
                            'next_minor_version': next_minor_version,
                            'next_major_version': next_major_version
                        })
                    )

    return requirements


def get_setup_attributes(root_dir: str = None, git_root_dir: str = None, pipenv: bool = False):
    """
    Prepare attributes for setup() call

    :param root_dir:
    :param git_root_dir:
    :param pipenv: True to enable Pipfile.lock parsing
    :return:
    """

    # loads metadata from config.json
    with open(root_dir + '/setup.json') as f:
        setup_attributes = json_load(f)

    # sets long description
    if os.path.isfile(root_dir + '/README.md'):
        with open(root_dir + '/README.md', 'r') as f:
            setup_attributes['long_description'] = f.read()
            setup_attributes['long_description_content_type'] = 'text/markdown'

    elif os.path.isfile(root_dir + '/README.rst'):
        with open(root_dir + '/README.rst', 'r') as f:
            setup_attributes['long_description'] = f.read()
            setup_attributes['long_description_content_type'] = 'text/x-rst; charset=UTF-8'

    if root_dir is None:
        root_dir = os.path.dirname(os.path.realpath(__file__))

    if git_root_dir is None:
        git_root_dir = os.path.dirname(os.path.realpath(__file__))

    # calculate requirements - internal and external
    current_version, next_minor_version, next_major_version = _calculate_version(git_root_dir)
    setup_attributes['install_requires'] = _calculate_requirements(
        current_version,
        next_minor_version,
        next_major_version,
        root_dir
    )

    # turn on SCM integration
    setup_attributes['use_scm_version'] = {
        "root": git_root_dir,
        "local_scheme": _local_scheme
    },

    # add SCM integration to requirements for setuptools run
    if "setup_requires" not in setup_attributes:
        setup_attributes['setup_requires'] = []

    setup_attributes['setup_requires'].append('setuptools_scm')

    if pipenv:
        setup_attributes += collect_locked_dependencies(root_dir=root_dir)

    return setup_attributes
