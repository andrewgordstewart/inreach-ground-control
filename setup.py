from setuptools import setup, find_packages

setup(
    name='InreachGroundControl',
    version='0.1.0',
    description='A command line utility for sending weather reports to the middle of nowhere.',
    url='https://github.com/andrewgordstewart/inreach-ground-control',
    author='Andrew Stewart',
    author_email='andrew.gord.stewart@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'bs4',
        'click',
        'datetime',
        'imapclient',
        'forecastiopy',
        'psycopg2',
        'pytest',
        'requests',
        'sqlalchemy',

    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        weather_report=inreach_ground_control.weather_report:cli
    ''',
)
