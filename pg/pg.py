from os import getenv
from subprocess import Popen
import pyperclip

from .helpers import (cd_repository_root, current_branch, pick_branch, pick_commit,
                      pick_commit_reflog, pick_file, pick_modified_file,)


try:
    pyperclip.copy('')
    _copy = pyperclip.copy
except pyperclip.exceptions.PyperclipException:
    _copy = lambda text: None

def copy(s):
    """Copy `s` using `_copy`, which is `pyperclip.copy`, or a NOOP if
    `pyperclip` doesn't work.
    """
    _copy(s.decode('utf-8') if type(s) is bytes else s)

def execute(command):
    """Make sure `command` is a string, and execute it using the shell specified
    by the $SHELL env var, or by the default shell if $SHELL isn't defined.

    Print `command` for logging purposes.
    """
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


def branch(*args, **kwargs):
    """Pick a branch and pass it to `args`, or copy the branch name.
    """
    branch = pick_branch()
    if not args:
        copy(branch)
    else:
        execute(args + (branch,))

def branch_file(*args, show=False, **kwargs):
    """Pick a branch, diff files with HEAD, pick one of these files and diff or
    `show` it.
    """
    cd_repository_root()
    branch = pick_branch()
    file = pick_modified_file(branch)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(branch, file)])
    else:
        execute(['git', 'diff', '{} -- {}'.format(branch, file)])

def branch_compare(*args, both=False, detailed=False, **kwargs):
    """Find out how far ahead or behind `this` branch is compared with `that`. A
    `detailed` comparison shows all commits instead of just the commit count.
    """
    this = pick_branch() if both else current_branch()
    that = pick_branch()
    if detailed:
        execute('git log --stat {that}..{this} && git log --stat {this}..{that}'.format(
                this=this, that=that))
    else:
        execute('git rev-list --left-right --count {}...{}'.format(this, that))


def commit(*args, **kwargs):
    """Pick a commit and pass it to `args`, or copy the commit hash.
    """
    commit = pick_commit()
    if not args:
        copy(commit)
    else:
        execute(args + (commit,))

def commit_file(*args, show=False, **kwargs):
    """Pick a commit, diff files with HEAD, pick one of these files and diff or
    `show` it.
    """
    cd_repository_root()
    commit = pick_commit()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])

def commit_reflog(*args, **kwargs):
    """Pick a commit from the reflog pass it to `args`, or copy the commit hash.
    """
    commit = pick_commit_reflog()
    if not args:
        copy(commit)
    else:
        execute(args + (commit,))

def commit_reflog_file(*args, show=False, **kwargs):
    """Pick a commit from the reflog, diff files with HEAD, pick one of these
    files and diff or `show` it.
    """
    cd_repository_root()
    commit = pick_commit_reflog()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])


def file_commit(*args, show=False, **kwargs):
    """Pick a file from index, and show all commits for this file. Pick a commit
    and diff file against HEAD or `show` it.
    """
    cd_repository_root()
    file = pick_file()
    copy(file)
    commit = pick_commit('--follow', '--', file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])
