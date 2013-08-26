from setuptools import setup, find_packages

setup(
    name='statika',
    version='0.1',
    description='Primitive and fast builder of static blocks (js, css)'
    ' to bundles',
    long_description='',
    author='Alexander Pokatilov',
    author_email='thasonic@gmail.com',
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    install_requires = ['watchdog'],
)
