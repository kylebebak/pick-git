from setuptools import setup

setup(
    name='pick-git',
    version='0.1.0',
    description='Use pick by thoughtbot to transform the way you use Git',
    long_description='Check it out on GitHub',
    keywords='pick git thoughtbot fuzzy select terminal',
    url='https://github.com/kylebebak/pick-git',
    download_url = 'https://github.com/kylebebak/pick-git/tarball/0.1.0',
    author='kylebebak',
    author_email='kylebebak@gmail.com',
    license='MIT',
    packages=['pick-git'],
    install_requires=['pyperclip'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
