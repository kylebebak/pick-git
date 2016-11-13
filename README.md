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
Check out how `pick-git` removes the pain finding and comparing commits.

![pick-git -b commit git diff](https://raw.githubusercontent.com/kylebebak/pick-git/master/examples/ghp.gif)


## Tests
~~~sh
# from the project root
python -m unittest discover tests -v
~~~

The tests don't do anything yet.


## Contributing
The "primitives" for the package are defined in `pg/core.py`, and are listed below. If you think of other useful primitives please fork the repo and submit a pull request.

- `pick_branch`
- `pick_commit`
- `pick_commit_reflog`
- `pick_modified_file`
- `pick_file`

The public methods whose names are passed to `pick-git` as one of its command line args, e.g. `branch`, `commit` `branch_compare`, etc, are defined in a mixin class in `pg/helpers.py`.

The package currently has no tests, but I would like to write tests for the primitives and the public methods. I would be grateful if anyone wants to help.


## License
This code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
