import subprocess, os, sys
from subprocess import STDOUT, PIPE
from functools import wraps


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


def exit_on_keyboard_interrupt(f):
    """Decorator that allows user to exit script by sending a keyboard interrupt
    (ctrl + c) without raising an exception.
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
    branches = subprocess.Popen(('git', 'branch', '-a') + args, stdout=PIPE)
    branch = subprocess.check_output(['pick'], stdin=branches.stdout)
    return branch.split()[-1].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_commit(*args):
    """Pick a commit hash.
    """
    commits = subprocess.check_output(('git', 'log', "--pretty=format:%h %ad | %s%d [%an]", '--date=short') + args)
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_commit_reflog(*args):
    """Pick a commit hash from the reflog.
    """
    commits = subprocess.check_output(('git', 'reflog', '--all', '--date=short') + args)
    commits = add_new_line(commits)
    p = subprocess.Popen(['pick'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    commit = p.communicate(input=commits)[0]
    return commit.split()[0].decode('utf-8')

@exit_on_keyboard_interrupt
def pick_modified_file(*args):
    """Pick a file whose state differs between two branches or commits, which are
    passed in `args`. If `args` contains only one branch or commit, this is
    compared against HEAD.
    """
    files = subprocess.Popen(('git', 'diff', '--name-only',) + args, stdout=PIPE)
    file = subprocess.check_output(['pick'], stdin=files.stdout)
    return file.strip().decode('utf-8')

@exit_on_keyboard_interrupt
def pick_file(*args):
    """Pick a file from the index.
    """
    files = subprocess.Popen(('git', 'ls-tree', '-r', 'master', '--name-only') + args, stdout=PIPE)
    file = subprocess.check_output(['pick'], stdin=files.stdout)
    return file.strip().decode('utf-8')


class PGMethodMixin(object):
    ###############
    # BRANCHES/COMMITS
    ###############
    def _pick_both(self, *args, function, **kwargs):
        """Helper that invokes a pick helper `function` one or two times, and
        passes the string git `entities`, e.g. branches or commit hashes, to
        `args`.
        """
        entities = [function(), function() if kwargs.pop('both', False) else None]
        if not entities[1]:
            entities.pop()
        if not args:
            self.copy(', '.join(entities))
        else:
            self.execute(*(args + tuple(entities)))

    def branch(self, *args, **kwargs):
        """Pick branch(es) and pass them to `args`, or copy branch names.
        """
        self._pick_both(*args, function=pick_branch, **kwargs)

    def commit(self, *args, **kwargs):
        """Pick a commit hash(es) and pass them to `args`, or copy commit hash
        names.
        """
        self._pick_both(*args, function=pick_commit, **kwargs)

    def commit_reflog(self, *args, **kwargs):
        """Pick commit hash(es) from the reflog and pass them to `args`, or copy
        commit hash names.
        """
        self._pick_both(*args, function=pick_commit_reflog, **kwargs)


    ###############
    # FILES BETWEEN BRANCHES/COMMITS
    ###############
    def _pick_file(self, *args, function, **kwargs):
        """Helper that invokes a pick helper `function` one or two times, and
        passes the string git `entities`, e.g. branches or commit hashes, to
        `args`.
        """
        show = kwargs.pop('show', False)
        cd_repository_root()
        entities = [function(), function() if kwargs.pop('both', False) else 'HEAD']
        file = pick_modified_file(entities); self.copy(file)
        if show:
            self.execute('git', 'show', '{}:{}'.format(entities[0], file))
        else:
            self.execute('git', 'diff', '{} {} -- {}'.format(entities[0], entities[1], file))

    def branch_file(self, *args, **kwargs):
        """Pick branch(es), get list of files that are different in these
        branches, pick one of these files and diff or `show` it.
        """
        self._pick_file(*args, function=pick_branch, **kwargs)

    def commit_file(self, *args, **kwargs):
        """Pick commit(s), get list of files that are different in these commits,
        pick one of these files and diff or `show` it.
        """
        self._pick_file(*args, function=pick_commit, **kwargs)

    def commit_reflog_file(self, *args, **kwargs):
        """Pick commit(s) from the reflog, get list of files that are different in
        these commits, pick one of these files and diff or `show` it.
        """
        self._pick_file(*args, function=pick_commit_reflog, **kwargs)


    ###############
    # MISCELLANEOUS
    ###############
    def branch_compare(self, *args, **kwargs):
        """Find out how far ahead or behind `this` branch is compared with `that`. A
        `detailed` comparison shows all commits instead of just the commit count.
        """
        both = kwargs.pop('both', False)
        detailed = kwargs.pop('detailed', False)
        this = pick_branch() if both else current_branch()
        that = pick_branch()
        if detailed:
            self.execute('git log --stat {that}..{this} && git log --stat {this}..{that}'.format(
                    this=this, that=that))
        else:
            self.execute('git rev-list --left-right --count {}...{}'.format(this, that))


    def file_commit(self, *args, **kwargs):
        """Pick a file from index, and show all commits for this file. Pick a commit
        and diff file against HEAD or `show` it.
        """
        show = kwargs.pop('show', False)
        cd_repository_root()
        file = pick_file(); self.copy(file)
        commit = pick_commit('--follow', '--', file)
        try:
            other_file = pick_modified_file(commit, raise_exception=True)
        except KeyboardInterrupt:
            other_file = file
        if show:
            self.execute('git', 'show', '{}:{}'.format(commit, file))
        else:
            self.execute('git', 'diff', '{} -M25 -- {} {}'.format(commit, file, other_file))
