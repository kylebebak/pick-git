from os import getenv
from subprocess import Popen
import pyperclip

from .helpers import (cd_repository_root, current_branch, pick_branch, pick_commit,
                      pick_commit_reflog, pick_file, pick_modified_file,)


# if pyperclip doesn't work, `copy` is initialized to a NOOP
try:
    pyperclip.copy('')
    _copy = pyperclip.copy
except pyperclip.exceptions.PyperclipException:
    _copy = lambda text: None

def copy(s):
    _copy(s.decode('utf-8') if type(s) is bytes else s)

def execute(command):
    if not isinstance(command, str):
        command = ' '.join(command)
    print(command)

    shell = getenv('SHELL')
    if shell:
        p = Popen([shell, '-i', '-c', command])
        p.communicate()
    else:
        p = Popen(command)
        p.communicate()


def branch(*args):
    branch = pick_branch()
    if not args:
        copy(branch)
    else:
        execute(args + tuple(branch))

def branch_file(show=False):
    cd_repository_root()
    branch = pick_branch()
    file = pick_modified_file(branch)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(branch, file)])
    else:
        execute(['git', 'diff', '{} -- {}'.format(branch, file)])

def branch_compare(both=False, detailed=False):
    that = pick_branch()
    this = pick_branch() if both else current_branch()
    if detailed:
        execute('git log --stat {that}..{this} && git log --stat {this}..{that}'.format(
                this=this, that=that))
    else:
        execute('git rev-list --left-right --count {}...{}'.format(this, that))


def commit(*args):
    commit = pick_commit()
    if not args:
        copy(commit)
    else:
        execute(args + tuple(commit))

def commit_file(show=False):
    cd_repository_root()
    commit = pick_commit()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])

def commit_reflog(*args):
    commit = pick_commit_reflog()
    if not args:
        copy(commit)
    else:
        execute(args + tuple(commit))

def commit_reflog_file(show=False):
    cd_repository_root()
    commit = pick_commit_reflog()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])


def file_commit():
    pass

if __name__ == '__main__':
    branch_compare(detailed=True)
