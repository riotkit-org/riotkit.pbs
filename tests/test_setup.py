import unittest
import pytest
from unittest.mock import patch

from riotkit.pbs.setup import _calculate_version, \
    _render_template, \
    _calculate_requirements


class SetupTest(unittest.TestCase, object):
    def test_calculate_version(self):
        with patch('riotkit.pbs.setup.get_version') as get_version_mock:
            get_version_mock.return_value = '1.3.1.2'

            current_version, next_minor_version, next_major_version = _calculate_version('/something/mocked')

        self.assertEqual('1.3.1.2', current_version)
        self.assertEqual('1.4', next_minor_version)
        self.assertEqual('2.0', next_major_version)

    def test_calculate_requirements(self):
        req = _calculate_requirements(
            current_version='1.3.1.2',
            next_minor_version='1.4',
            next_major_version='2.0',
            root_dir='example'
        )

        self.assertEqual(
            ['somepackage<6,>=5.0', 'rkd.core >= 1.3.1.2, < 1.4'],
            req
        )


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
def test_render_template(template: str, variables: dict, expected: str):
    assert expected == _render_template(template, variables)

