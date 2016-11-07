from os import getenv
from subprocess import Popen
from functools import wraps

import pyperclip

from .helpers import (cd_repository_root, current_branch, pick_branch, pick_commit,
                      pick_commit_reflog, pick_file, pick_modified_file,)


shell, rcfile = ('', '')

def set_shell_globals(f):
    """Decorator that parses `shell` and `rcfile` kwargs and sets them as global
    variables.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        global shell
        global rcfile
        shell = kwargs.pop('shell', '')
        rcfile = kwargs.pop('rcfile', '')
        return f(*args, **kwargs)
    return wrapper

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
    """Make sure `command` is a string, and execute it using the global `shell`
    var, the shell specified by the $SHELL env var, or by the default shell.

    Also prints `command`.
    """
    if not isinstance(command, str):
        command = ' '.join(command)
    print(command)

    global shell
    global rcfile
    shell = shell or getenv('SHELL')
    rcfile = ['--rcfile', rcfile] if rcfile else []
    if shell:
        p = Popen([shell] + rcfile + ['-i', '-c', command])
        p.communicate()
    else:
        p = Popen(command)
        p.communicate()


@set_shell_globals
def branch(*args, **kwargs):
    """Pick a branch and pass it to `args`, or copy the branch name.
    """
    branch = pick_branch()
    if not args:
        copy(branch)
    else:
        execute(args + (branch,))

@set_shell_globals
def branch_file(*args, **kwargs):
    """Pick a branch, diff files with HEAD, pick one of these files and diff or
    `show` it.
    """
    show = kwargs.pop('show', False)
    cd_repository_root()
    branch = pick_branch()
    file = pick_modified_file(branch)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(branch, file)])
    else:
        execute(['git', 'diff', '{} -- {}'.format(branch, file)])

@set_shell_globals
def branch_compare(*args, **kwargs):
    """Find out how far ahead or behind `this` branch is compared with `that`. A
    `detailed` comparison shows all commits instead of just the commit count.
    """
    both = kwargs.pop('both', False)
    detailed = kwargs.pop('detailed', False)
    this = pick_branch() if both else current_branch()
    that = pick_branch()
    if detailed:
        execute('git log --stat {that}..{this} && git log --stat {this}..{that}'.format(
                this=this, that=that))
    else:
        execute('git rev-list --left-right --count {}...{}'.format(this, that))


@set_shell_globals
def commit(*args, **kwargs):
    """Pick a commit and pass it to `args`, or copy the commit hash.
    """
    commit = pick_commit()
    if not args:
        copy(commit)
    else:
        execute(args + (commit,))

@set_shell_globals
def commit_file(*args, **kwargs):
    """Pick a commit, diff files with HEAD, pick one of these files and diff or
    `show` it.
    """
    show = kwargs.pop('show', False)
    cd_repository_root()
    commit = pick_commit()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])

@set_shell_globals
def commit_reflog(*args, **kwargs):
    """Pick a commit from the reflog pass it to `args`, or copy the commit hash.
    """
    commit = pick_commit_reflog()
    if not args:
        copy(commit)
    else:
        execute(args + (commit,))

@set_shell_globals
def commit_reflog_file(*args, **kwargs):
    """Pick a commit from the reflog, diff files with HEAD, pick one of these
    files and diff or `show` it.
    """
    show = kwargs.pop('show', False)
    cd_repository_root()
    commit = pick_commit_reflog()
    file = pick_modified_file(commit)
    copy(file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])


@set_shell_globals
def file_commit(*args, **kwargs):
    """Pick a file from index, and show all commits for this file. Pick a commit
    and diff file against HEAD or `show` it.
    """
    show = kwargs.pop('show', False)
    cd_repository_root()
    file = pick_file()
    copy(file)
    commit = pick_commit('--follow', '--', file)
    if show:
        execute(['git', 'show', '{}:{}'.format(commit, file)])
    else:
        execute(['git', 'diff', '{}:{} {}'.format(commit, file, file)])
