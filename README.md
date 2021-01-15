# simple-linter

Very simple container based on Alpine that runs several linting tools:

- [`ansible-lint`](https://pypi.org/project/ansible-lint/)
- [`yamllint`](https://pypi.org/project/yamllint/)
- [`flake8`](https://pypi.org/project/flake8/)
- [`pylint`](https://pypi.org/project/pylint/)
- [`shellcheck`](https://github.com/koalaman/shellcheck/)

## Building

Build the container:

```shell
$ docker build -t simple-linter .
```

Test with [`demo`](data) content:

```shell
$ docker run -v `pwd`/demo:/data simple-linter
./demo.yml
  3:12      warning  truthy value should be one of [false, true]  (truthy)

./demo.py:1:21: W292 no newline at end of file
************* Module demo
demo.py:1:0: C0304: Final newline missing (missing-final-newline)
demo.py:1:0: C0114: Missing module docstring (missing-module-docstring)

-------------------------------------
Your code has been rated at -10.00/10

./demo.sh
  2:1       warning  missing document start "---"  (document-start)
  3:13      error    no new line character at the end of file  (new-line-at-end-of-file)
```
