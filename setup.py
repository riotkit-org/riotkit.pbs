#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as readme:
    setup(
        name='riotkit.pbs',
        description='Python Build Simplified. A simple setuptools automation, '
                    'designed mainly for publishing multiple packages from single repository',
        long_description=readme.read(),
        license='Apache-2',
        url='https://github.com/riotkit-org',
        author_email='riotkit@riseup.net',
        long_description_content_type='text/markdown',
        keywords=['riotkit', 'pbs', 'pbr', 'build', 'simplified', 'reasonable',
                  'setuptools', 'anarchist', 'namespace', 'namespaced'],
        setup_requires=['setuptools_scm'],
        packages=find_namespace_packages(include='riotkit.*', exclude=('tests',)),
        use_scm_version={
            'root': './',
            'local_scheme': lambda txt: ''
        },
        install_requires=['setuptools_scm']
    )
