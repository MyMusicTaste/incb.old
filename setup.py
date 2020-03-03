import os
import setuptools
import subprocess
import sys


requirements = [
    'six>=1.10.0',
]

extras = {}

def get_version():
    import incb
    return incb.__version__


def readme():
    with open('README.md') as f:
        return f.read()


class Venv(setuptools.Command):
    user_options = [('python=', None, 'Which interpreter to build your venv with')]

    def initialize_options(self):
        self.python = ''

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'incb')
        print('Creating virtual environment in {path}'.format(path=venv_path))
        if '3' in self.python or sys.version_info[0] >= 3:
            import venv
            venv.main(args=[venv_path])
        else:
            venv_cmd = ['virtualenv']
            if self.python:
                venv_cmd.extend(['-p', self.python])
            venv_cmd.append(venv_path)
            subprocess.check_call(venv_cmd)
        print('Linking `activate` to top level of project.\n')
        print('To activate, simply run `source activate`.')
        try:
            os.symlink(
                os.path.join(venv_path, 'bin', 'activate'),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'activate')
            )
        except OSError:
            # symlink already exists
            pass


setuptools.setup(
    name='incb',
    version=get_version(),
    description="A python library for generating nginx configs.",
    long_description=readme(),
    author="Jin Nguyen",
    author_email='dangtrinhnt@mymusictaste.com',
    url='https://github.com/MyMusicTaste/incb',
    packages=setuptools.find_packages('incb'),
    package_dir={'': 'incb'},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras,
    license="BSD license",
    keywords='incb',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    cmdclass={'venv': Venv},
)
