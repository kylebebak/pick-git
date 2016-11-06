import subprocess, os
from subprocess import STDOUT, PIPE

import pyperclip

from .helpers import (cd_repository_root, pick_branch, pick_commit,
                      pick_commit_reflog, pick_file, pick_modified_file,)


# if pyperclip doesn't work, `copy` is initialized to a NOOP
try:
    pyperclip.copy('')
    _copy = pyperclip.copy
except pyperclip.exceptions.PyperclipException:
    _copy = lambda text: None

def copy(s):
    _copy(s.decode('utf-8') if type(s) is bytes else s)

def execute(commands):
    command = ' '.join(commands)
    print(command)

    shell = os.getenv('SHELL')
    if shell:
        p = subprocess.Popen([shell, '-i', '-c', command])
        p.communicate()
    else:
        p = subprocess.Popen(command)
        p.communicate()


def branch(*args):
    branch = pick_branch()
    if not args:
        copy(branch)
    else:
        execute([*args, branch])

def branch_file(show=False):
    cd_repository_root()
    branch = pick_branch()
    file = pick_modified_file(branch)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(branch, file)])
    else:
        execute(['git', 'diff', '{} -- {}'.format(branch, file)])


if __name__ == '__main__':
    branch_file(True)
