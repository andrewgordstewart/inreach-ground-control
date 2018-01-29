from setuptools import setup, find_packages


setup(
    name='InreachGroundControl',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        weather_report=inreach_ground_control.weather_report:cli
    ''',
)
