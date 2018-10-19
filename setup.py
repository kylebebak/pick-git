from setuptools import setup


setup(
    name='pick-git',
    version='1.2.2',
    description="Use pick by thoughtbot to turbocharge your Git workflow",
    long_description='Check it out on GitHub',
    keywords='pick git thoughtbot fuzzy select terminal productivity',
    url='https://github.com/kylebebak/pick-git',
    download_url='https://github.com/kylebebak/pick-git/tarball/1.2.2',
    author='kylebebak',
    author_email='kylebebak@gmail.com',
    license='MIT',
    packages=['pick_git'],
    entry_points={
        'console_scripts': ['pick-git=pick_git.command_line:main'],
    },
    install_requires=[
        'pyperclip',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
