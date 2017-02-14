# pick-git

__pick-git__ is a set of command line tools for leveraging thoughtbot's [pick](https://github.com/calleerlandsson/pick) to turbocharge your Git workflow.

Git can be a bit of a pain, especially when passing branches or commit hashes as args. Big projects have lots of branches and tons of commits. Finding and copying commit hashes to compare commits, for example, is awkward and slow.

`pick`, however, was literally born for jobs like this. __pick-git__ uses `pick` to make working with branches, commits and files in your project's repo a breeze.

It's installable via `pip` and works with Python 2/3.


## Installation
~~~sh
pip install pick-git
~~~


## Dependencies
- [pick](https://github.com/calleerlandsson/pick)
- [pyperclip](https://github.com/asweigart/pyperclip) (optional, and anyway it's automatically included if you install with `pip`)


## Usage
Check out how __pick-git__ removes the pain of finding and comparing commits.

![pick-git -b commit git diff](https://raw.githubusercontent.com/kylebebak/pick-git/master/examples/ghp.gif)


I invoked `ghp -b gd`, but what just happened? Let's break it down.

I have `ghp` aliased to `pick-git --function commit`. The function argument is one of the public functions exposed by pick-git.

`gd` is a shortcut I have that resolves to `git diff`. The `-b` flag allows me to pick both commits and compare them, instead of just picking one and comparing it with HEAD.

At the end the final command that was invoked, `gd 28faaf7 4750072`, was printed to the console. I was able to find two commits and compare them very quickly and with very few keystrokes. __Even if these commits had been in a much bigger project and were months old__, pick's fuzzy select would have found them in no time as long as my commit messages were descriptive.

### Shortcuts to pick-git Public Functions
It's a good idea to create shortcut aliases to all of the functions exposed by __pick-git__. You can simply copy and paste the following into your startup script, e.g. `.bash_profile`.

~~~sh
alias gbp="pick-git --function branch"
alias gtp="pick-git --function tag"
alias ghp="pick-git --function commit"
alias grp="pick-git --function commit_reflog"
alias gfp="pick-git --function file"

alias gbpf="pick-git --function branch_file"
alias ghpf="pick-git --function commit_file"
alias grpf="pick-git --function commit_reflog_file"
alias gpf="pick-git --function file_commit"

alias gbc="pick-git --function branch_compare"
~~~

Here are descriptions of __pick-git__'s public functions. Run `pick-git -h` to get help/information about optional arguments!

- __branch__: Pick branch(es) and pass them to `args`, or copy branch names.
- __commit__: Pick commit hash(es) and pass them to `args`, or copy commit hash names.
- __commit_reflog__: Pick commit hash(es) from the reflog and pass them to `args`, or copy commit hash names.
- __file__: Pick a modified file relative to last commit, pass it to `args`, or copy file name. Optionally pick from files that have been `staged` for commit.
- __branch_file__: Pick branch(es), get list of files that are different in these branches, pick one of these files and diff or `show` it.
- __commit_file__: Pick commit(s), get list of files that are different in these commits, pick one of these files and diff or `show` it.
- __commit_reflog_file__: Pick commit(s) from the reflog, get list of files that are different in these commits, pick one of these files and diff or `show` it.
- __branch_compare__: Find out how far ahead or behind `this` branch is compared with `that`. A `detailed` comparison shows all commits instead of just the commit count.
- __file_commit__: Pick a file from index, and show all commits for this file. Pick a commit and diff file against HEAD or `show` it.

### --shell and --rcfile
I actually lied above. I really have `ghp` aliased to `pick-git --shell /bin/bash --rcfile ~/.git_aliases --function commit`. What are these --shell and --rcfile args, and why are they useful?

When __pick-git__ is invoked, it creates a child process to execute whichever public function you specify. The child process invokes your default shell and sources the corresponding rcfile. This is nice, but if your startup file is loaded with crap, like mine, you might experience lag every time you invoke __pick-git__ and the rcfile is sourced.

To avoid this, I have a lightweight startup file called `.git_aliases` that defines a few Git shortcuts and nothing else. When I invoke __pick-git__, I used the --rcfile argument to make sure only this file is sourced.

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

### Help
Run `pick-git -h`.


## Contributing
The "primitives" for the package are defined in `pick_git/core.py` and are listed below. These are the functions that actually invoke `pick`. If you think of other useful primitives please fork the repo and submit a pull request.

- `pick_branch`
- `pick_commit`
- `pick_commit_reflog`
- `pick_modified_file`
- `pick_file`

The public methods whose names are passed to __pick-git__ in the `--function` argument, for example `branch` or `commit`, are defined in a mixin class in `pick_git/helpers.py`. I'm sure there are use cases I haven't thought of that deserve public functions, and I would be grateful for contributors.


## Tests
The package currently has no tests. This is because __pick-git__ requires user keystrokes to return a value. Sending keystrokes isn't part of Python's standard library, and anyway Python doesn't seem like the best way to do this, although [this seems promising](http://stackoverflow.com/questions/12755968/sending-arrow-keys-to-popen).

If anyone has ideas I'd love to hear them.


## License
This code is licensed under the [MIT License](https://opensource.org/licenses/MIT).


## Thanks
To Calle Erlandsson and thoughtbot for writing pick =)
