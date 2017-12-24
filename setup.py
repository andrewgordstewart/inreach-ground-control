from distutils.core import setup

setup(
    name='InreachGroundControl',
    version='0.1.0',
    author='Andrew Stewart',
    author_email='andrew.gord.stewart@gmail.com',
    packages=['inreach_ground_control', 'inreach_ground_control.test'],
    scripts=[],
    license='LICENSE.txt',
    description='An app for consuming and responding to messages from an Inreach satellite messenger.',
    long_description=open('README').read(),
    install_requires=[
    ],
)