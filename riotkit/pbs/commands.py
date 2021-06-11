import sys
import subprocess
import distutils.cmd
import distutils.log


class FreezeCommand(distutils.cmd.Command):
    description = 'Generate static requirements.txt'
    setup_attributes: dict = {}

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for dependency in self.setup_attributes.get('setup_requires'):
            print(dependency)


class InstallCommand(distutils.cmd.Command):
    description = 'Install requirements using pip'
    setup_attributes: dict = {}

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.check_call(['pip', 'install'] + self.setup_attributes.get('setup_requires'))
        except subprocess.CalledProcessError as err:
            sys.exit(err.returncode)
