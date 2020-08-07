from setuptools import setup, find_packages

setup(
    name='myfortune',
    description=(
        'Daily horoscope scraper modules for'
        'various Japanese television websites'
    ),
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'appdirs',
        'beautifulsoup4',
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        myfortune=myfortune.__main__:main
    ''',
)
