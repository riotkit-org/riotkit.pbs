
import unittest
from riotkit.pbs.pipenv import collect_locked_dependencies


class PipenvTest(unittest.TestCase):
    def test_pipenv_correctly_parses_file(self):
        dependencies = collect_locked_dependencies(root_dir='./example/pipenv')

        self.assertIn('certifi==2021.5.30', dependencies)
        self.assertIn("attrs==21.2.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
                      dependencies)

    def test_pipenv_raises_io_exception_when_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            collect_locked_dependencies(root_dir='./example')

    def test_pipenv_raises_exception_when_packages_section_not_found(self):
        with self.assertRaises(Exception) as exc:
            collect_locked_dependencies(root_dir='./example/invalid-pipenv')

        self.assertEquals('Incorrectly formatted Pipfile.lock, missing "default" section', str(exc.exception))
