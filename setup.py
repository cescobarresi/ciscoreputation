# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Command
# To use a consistent encoding
from codecs import open
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
# Get the 'about' information from relevant file
about = {}
with open(os.path.join(base_dir, "ciscoreputation", "__about__.py")) as f:
    exec(f.read(), about)

# Get the long description from the relevant file
with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


class ChangelogDebPackage(Command):
    """
    Update the debian package's changelog
    """
    description="update the debian package's changelog"
    user_options=[
        ('pyversion', None, 'Use about[__version__]'),
        ('version=', None, "Package version"),
        ('distribution=', None, "Distribution of package"),
        ('release', None, "Release package")
        ]
    def initialize_options(self):
        self.version = None
        self.distribution = None
        self.release = None
        self.pyversion = None
    def finalize_options(self):
        if self.version is not None and self.release is not None:
            raise AssertionError, "Can't set 'version' when using 'release'"
        if self.pyversion and self.version:
            raise AssertionError, "Conflicting options --pyversion and --version="
        if self.pyversion:
            self.version = about['__version__']
    def run(self):
        if self.release:
            os.system('dch --release %s' % (
                '--distribution %s' % self.distribution if self.distribution else ''))
        elif self.version:
            os.system('dch %s -v %s --changelog %s' % (
                '--distribution %s' % self.distribution if self.distribution else '',
                self.version,
                os.path.join(base_dir, 'debian','changelog')))
        else:
            os.system('dch %s --changelog %s' % (
                '--distribution %s' % self.distribution if self.distribution else '',
                os.path.join(base_dir, 'debian','changelog')))

class BuildDebPackage(Command):
    """
    Create deb package using dh_virtualenv.
    First cleans previous runs, then create python package with sdist and afterwards 
    create DEB package in folder deb/
    """
    description = "create deb package using dh_virtualenv"
    user_options=[
        ('nosdist', None, 'don\'t run command \'clean\' and \'sdist\' before building package'),
        ]
    def initialize_options(self):
        self.nosdist = None
    def finalize_options(self):
        pass
    def run(self):
        source_dir = os.path.join(base_dir, "dist/deb/source/")
        if not self.nosdist:
            os.system('python ./setup.py clean; python ./setup.py sdist')
        os.system('mkdir -p %s' % source_dir)
        os.system('tar -xf ./dist/*.tar.gz -C %s --strip-components=1' % source_dir)
        os.system('cp -R ./debian/ %s' % source_dir)
        os.system('cd %s; dpkg-buildpackage -uc -us' % source_dir)
        os.system('rm -r %s' % source_dir)
        os.system('rm -r ./*.egg-info/')
        print "DEB package generated in %s" % os.path.join(base_dir, "dist/deb/")

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    description="custom clean command to tidy up the project root."
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

setup(
    name=about['__title__'],
    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],

    author=about['__author__'],
    author_email=about['__email__'],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project?
        "Development Status :: 4 - Beta",

        # Intended for
        "Environment :: Console",
        "Intended Audience :: System Administrators",

        # License
        "License :: OSI Approved :: MIT License",

        # Python support
        "Programming Language :: Python :: 2.7",

        # Others
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        ],
    keywords='',
    packages=find_packages(exclude=['venv', 'env']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. 
    install_requires=['docopt','requests'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.

    entry_points={
    #  The functions you specify are called with no arguments, and their return
    # value is passed to sys.exit(), so you can return an errorlevel or message
    # to print to stderr.
        'console_scripts': [
            'ciscoreputation=ciscoreputation:main',
        ],
    },
    cmdclass={
        'clean': CleanCommand,
        'debdist': BuildDebPackage,
        'debchangelog': ChangelogDebPackage
    }
)
