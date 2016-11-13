from setuptools import setup

setup(
    name='pick-git',
    version='0.2.1',
    description="Use pick by thoughtbot to turbocharge your Git workflow",
    long_description='Check it out on GitHub',
    keywords='pick git thoughtbot fuzzy select terminal productivity',
    url='https://github.com/kylebebak/pick-git',
    download_url = 'https://github.com/kylebebak/pick-git/tarball/0.2.1',
    author='kylebebak',
    author_email='kylebebak@gmail.com',
    license='MIT',
    packages=['pg'],
    entry_points={
        'console_scripts': ['pick-git=pg.command_line:main'],
    },
    install_requires=[
        'pyperclip',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
