from .core import pick_branch, pick_tag, pick_commit, pick_commit_reflog, pick_modified_file, pick_file, cd_repository_root, current_branch


class PGPublicMethodMixin(object):
    ###############
    # BRANCHES/COMMITS/FILES
    ###############
    def _pick_both(self, *args, **kwargs):
        """Helper that invokes a pick helper `function` one or two times, and
        passes the git `entities` string, e.g. branches or commit hashes, to
        `args`.
        """
        function = kwargs.get('function')
        entities = [function(), function() if kwargs.pop('both', False) else None]
        if not entities[1]:
            entities.pop()
        if not args:
            self.copy(' '.join(entities))
        else:
            self.execute(*(args + tuple(entities)))

    def branch(self, *args, **kwargs):
        """Pick branch(es) and pass them to `args`, or copy branch names.
        """
        self._pick_both(*args, function=pick_branch, **kwargs)

    def tag(self, *args, **kwargs):
        """Pick tag(s) and pass them to `args`, or copy tag names.
        """
        self._pick_both(*args, function=pick_tag, **kwargs)

    def commit(self, *args, **kwargs):
        """Pick commit hash(es) and pass them to `args`, or copy commit hash
        names.
        """
        self._pick_both(*args, function=pick_commit, **kwargs)

    def commit_reflog(self, *args, **kwargs):
        """Pick commit hash(es) from the reflog and pass them to `args`, or copy
        commit hash names.
        """
        self._pick_both(*args, function=pick_commit_reflog, **kwargs)

    def file(self, *args, **kwargs):
        """Pick a modified file relative to last commit, pass it to `args`, or
        copy file name. Optionally pick from files that have been `staged` for
        commit.
        """
        cd_repository_root()
        file = pick_modified_file('--staged') if kwargs.pop('staged', False) else pick_modified_file()
        if not args:
            self.copy(file)
        else:
            self.execute(*args + (file,))

    ###############
    # FILES BETWEEN BRANCHES/COMMITS
    ###############
    def _pick_file(self, *args, **kwargs):
        """Helper that invokes a pick helper `function` one or two times, and
        passes the string git `entities`, e.g. branches or commit hashes, to
        `args`.
        """
        function = kwargs.get('function')
        show = kwargs.pop('show', False)
        cd_repository_root()
        entities = [function(), function() if kwargs.pop('both', False) else 'HEAD']
        self.copy(' '.join(entities))
        file = pick_modified_file(*entities)
        if show:  # ugly syntax, but (a, b*, c) syntax isn't valid in python 2
            self.execute(*('git', 'show') + args + ('{}:{}'.format(entities[0], file),))
        else:
            self.execute(*('git', 'diff') + args + ('{} -- {} {}'.format(entities[0], entities[1], file),))

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
        file = pick_file()
        self.copy(file)
        commit = pick_commit('--follow', '--', file)
        try:
            other_file = pick_modified_file(commit, raise_exception=True)
        except KeyboardInterrupt:
            other_file = file
        if show:
            self.execute(*('git', 'show') + args + ('{}:{}'.format(commit, file),))
        else:
            self.execute(*('git', 'diff') + args + ('{} -- {} {}'.format(commit, file, other_file),))
