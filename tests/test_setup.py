import unittest
import pytest
from unittest.mock import patch

from riotkit.pbs.setup import _calculate_version, \
    _render_template, \
    _calculate_requirements, \
    get_setup_attributes, \
    _bump_version_number


class SetupTest(unittest.TestCase, object):
    def test_calculate_version(self):
        with patch('riotkit.pbs.setup.get_version') as get_version_mock:
            get_version_mock.return_value = '1.3.1.2'

            current_version, next_minor_version, next_major_version = _calculate_version('/something/mocked')

        self.assertEqual('1.3.1.2', current_version)
        self.assertEqual('1.4', next_minor_version)
        self.assertEqual('2.0', next_major_version)

    def test_calculate_requirements_loads_requirements_from_external_and_packages(self):
        req = _calculate_requirements(
            current_version='1.3.1.2',
            next_minor_version='1.4',
            next_major_version='2.0',
            root_dir='example/working'
        )

        self.assertEqual(
            ['somepackage >= 5.0, < 6', 'rkd.core >= 1.3.1.2, < 1.4'],
            req
        )

    def test_calculate_requirements_from_requirements_txt_are_plain(self):
        """
        requirements from requirements.txt should be without filling up a template
        :return:
        """

        req = _calculate_requirements(
            current_version='1.3.1.2',
            next_minor_version='1.4',
            next_major_version='2.0',
            root_dir='example/not-working-bad-requirements-txt'
        )

        self.assertEqual(
            [
                # see example/not-working-bad-requirements-txt/requirements.txt - should not be parsed
                'flask >= {{ current_version }}, < {{ next_minor_version }}',

                # see example/not-working-bad-requirements-txt/requirements-subpackages.txt - it is parsed
                'rkd.core >= 1.3.1.2, < 1.4'
            ],
            req
        )

    def test_get_setup_attributes_contains_install_requires_name_and_author(self):
        attributes = get_setup_attributes(root_dir='example/working', git_root_dir='./')

        self.assertEqual(attributes.get('name'), 'rkd.process')
        self.assertEqual(attributes.get('author'), 'RiotKit non-profit organization')
        self.assertIn('rkd.core >= ', str(attributes.get('install_requires')))
        self.assertIn('somepackage >= 5.0, < 6', str(attributes.get('install_requires')))


@pytest.mark.parametrize("template,variables,expected", [
    # with spaces
    (
        'rkd.core >= {{ current_version   }}, < {{    next_minor_version }}',
        {'current_version': '1.3.1.2', 'next_minor_version': '1.4'},
        'rkd.core >= 1.3.1.2, < 1.4'
    ),
    # without spaces
    (
        'rkd.core >= {{current_version}}, < {{next_minor_version}}',
        {'current_version': '1.3.1.2', 'next_minor_version': '1.4'},
        'rkd.core >= 1.3.1.2, < 1.4'
    )
])
def test_render_template(template: str, variables: dict, expected: str) -> None:
    assert expected == _render_template(template, variables)


@pytest.mark.parametrize("version,expected", [
    (
        '1',  # version
        '2'   # expected after bump
    ),
    (
        '1-rc2',  # version
        '2-rc2'   # expected after bump
    ),
    (
        '1.rc1',  # version
        '2.rc1'   # expected after bump
    )
])
def test_bump_version_number(version: str, expected: str) -> None:
    """
    Bumps part of a version number
    The metadata part after non-numeric character (ex. -, .) cannot be incremented, as it is totally custom value
    that we do not understand purpose of

    :param version:
    :param expected:
    :return:
    """

    assert expected == _bump_version_number(version)
