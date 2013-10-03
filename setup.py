from setuptools import setup, find_packages

setup(
    name = 'tripmonitor-client',
    version = '0.1.0-dev',
    author = 'PlannerStack',
    author_email = 'contact@plannerstack.org',
    license = 'MIT',
    description = 'Client for the trip monitor system',
    long_description = open('README.rst').read(),
    url = 'http://github.com/plannerstack/tripmonitor-client',
    download_url = 'http://github.com/plannerstack/tripmonitor-client/archives/master',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    platforms = ['all'],
    entry_points = {
        'console_scripts': [
            'tripmonitor-client = tripmonitor.client:main',
        ],
    },
    install_requires = [
        'requests',
        'websocket-client',
        'pyzmq',
        'simplejson',
        'python-dateutil',
    ],
)
