# pick-git

__pick-git__ is a set of command line tools for leveraging [pick](https://github.com/calleerlandsson/pick) to turbocharge your Git workflow.

`git` can be a bit of a pain, especially when passing branches or commit hashes as args. Big projects have lots of branches and tons of commits. Finding and copying commit hashes to compare commits, for example, is awkward and slow.

`pick`, however, was literally born for jobs like this. `pick-git` uses `pick` to make working with branches, commits and files in your project's repo a breeze.

It's installable via `pip` and works with Python 2/3.


## Installation
~~~sh
pip install pick-git
~~~


## Dependencies
- [pick](https://github.com/calleerlandsson/pick)
- [pyperclip](https://github.com/asweigart/pyperclip) (optional, and anyway it's automatically included if you install with `pip`)


## Usage
Check out how `pick-git` removes the pain of finding and comparing commits.

![pick-git -b commit git diff](https://raw.githubusercontent.com/kylebebak/pick-git/master/examples/ghp.gif)


`~/.bash_profile`

~~~sh
alias gbp="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function branch"
alias ghp="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function commit"
alias grp="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function commit_reflog"
alias gfp="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function file"

alias gbpf="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function branch_file"
alias ghpf="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function commit_file"
alias grpf="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function commit_reflog_file"
alias gpf="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function file_commit"

alias gbc="pick-git --shell /bin/bash --rcfile ~/.git_aliases --function branch_compare"
~~~


`~/.git_aliases`

~~~sh
alias gb='git branch'
alias go='git checkout'
alias gc='git commit'
alias gm='git merge'
alias gd='git diff'
alias ga='git add'
alias gr='git reset'
~~~


## Contributing
The "primitives" for the package are defined in `pick_git/core.py`, and are listed below. If you think of other useful primitives please fork the repo and submit a pull request.

- `pick_branch`
- `pick_commit`
- `pick_commit_reflog`
- `pick_modified_file`
- `pick_file`

The public methods whose names are passed to `pick-git` as one of its command line args, e.g. `branch`, `commit` `branch_compare`, etc, are defined in a mixin class in `pick_git/helpers.py`.

### Tests
The package currently has no tests. This is because `pick-git`'s functions, even the "primitives" in `pick_git/core.py`, require user keystrokes to return a value. Sending keystrokes isn't part of Python's standard library, and anyway Python doesn't seem like the best way to do this, although [this seems promising](http://stackoverflow.com/questions/12755968/sending-arrow-keys-to-popen).

If anyone has ideas I'd love to hear them.


## License
This code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
