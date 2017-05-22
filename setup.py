from setuptools import setup

setup(
    name='jupyterhub-crowdauhenticator',
    version='1.0',
    description='CROWD Authenticator for JupyterHub',
    url='https://github.com/kooper/crowdauhenticator',
    author='Rob Kooper',
    author_email='kooper@illinois.edu',
    license='3 Clause BSD',
    packages=['crowdauhenticator'],
    install_requires=[
        'requests'
    ]
)
