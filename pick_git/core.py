import subprocess
import sys
import os
from subprocess import STDOUT, PIPE
from functools import wraps


def repository_root():
    """Return full path to root of repo.
    """
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')


def cd_repository_root():
    """Change directory to repo root. `os.chdir` means directory is changed for
    instance of shell from which script is executed, rather than only in child
    process.
    """
    os.chdir(repository_root())


def current_branch():
    """Return name of currently checked out branch.
    """
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')


def add_new_line(b):
    """To end of `str` or `bytes` instance.
    """
    if sys.version_info < (3, 0, 0):
        if b[-1] != '\n':
            b += '\n'
    else:
        if b[-1:] != bytes('\n', 'utf-8'):
            b += bytes('\n', 'utf-8')
    return b


def exit_on_keyboard_interrupt(f):
    """Decorator that allows user to exit script by sending a keyboard interrupt
    (ctrl + c) without raising an exception.

    WARNING: there is no guarantee KeyboardInterrupt will be raised if `ctrl+c` is
    pressed while the subprocess is running, which means we also need to guard
    against empty results from `pick`!

    See here: https://stackoverflow.com/questions/39499959/terminating-a-subprocess-with-keyboardinterrupt/39503654
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        raise_exception = kwargs.pop('raise_exception', False)
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt:
            if not raise_exception:
                sys.exit()
            raise KeyboardInterrupt
    return wrapper


@exit_on_keyboard_interrupt
def pick_branch(*args):
    """Pick a branch, local or remote.
    """
    branches = subprocess.check_output(('git', 'branch', '-a') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    branch = p.communicate(input=branches)[0]
    if not branch:
        raise KeyboardInterrupt
    return branch.split()[-1].decode('utf-8')


@exit_on_keyboard_interrupt
def pick_tag(*args):
    """Pick a local tag.
    """
    branches = subprocess.check_output(('git', 'tag', '-l') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    branch = p.communicate(input=branches)[0]
    if not branch:
        raise KeyboardInterrupt
    return branch.split()[-1].decode('utf-8')


@exit_on_keyboard_interrupt
def pick_commit(*args):
    """Pick a commit hash.
    """
    commits = subprocess.check_output(('git', 'log', "--pretty=format:%h %ad | %s%d [%an]", '--date=short') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=add_new_line(commits))[0]
    if not commit:
        raise KeyboardInterrupt
    return commit.split()[0].decode('utf-8')


@exit_on_keyboard_interrupt
def pick_commit_reflog(*args):
    """Pick a commit hash from the reflog.
    """
    commits = subprocess.check_output(('git', 'reflog', '--date=short') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=add_new_line(commits))[0]
    if not commit:
        raise KeyboardInterrupt
    return commit.split()[0].decode('utf-8')


@exit_on_keyboard_interrupt
def pick_modified_file(*args):
    """Pick a file whose state differs between branches or commits, which are
    passed in `args`. `args` can contain between 0 and 2 elements.
    """
    files = subprocess.check_output(('git', 'diff', '--name-only') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    file = p.communicate(input=files)[0]
    if not file:
        raise KeyboardInterrupt
    return file.strip().decode('utf-8')


@exit_on_keyboard_interrupt
def pick_file(*args):
    """Pick a file from the index.
    """
    branch = current_branch()
    files = subprocess.check_output(('git', 'ls-tree', '-r', branch, '--name-only') + args)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    file = p.communicate(input=files)[0]
    if not file:
        raise KeyboardInterrupt
    return file.strip().decode('utf-8')
