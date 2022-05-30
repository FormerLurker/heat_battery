from setuptools import setup, find_packages
setup(
    name='heat_battery',
    version='0.1.0',
    description='Use energy more efficiently by turning your home into a heat batter',
    author="Brad Hochgesang",
    author_email="formerlurker@protonmail.com",
    entry_points={
      'console_scripts': ['path=heat_battery.main:main']
    },
    install_requires=['requests'],
    packages=find_packages()
)
