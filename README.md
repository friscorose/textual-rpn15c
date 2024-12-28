# A TUI RPN Calculator with an HP 15C theme
![rpn_15c](https://repository-images.githubusercontent.com/819673411/3fbc9495-9114-48cb-bb6d-36b0ff53b1cf)

and yes, that is just text. Pretty sigma, eh!?

## Quick Start

In a modern terminal emulator that is at least 126 characters wide and 31 characters tall perform the following steps:
### Establish uv/uvx
If you already have `uv` and `uvx` skip this step ->
`pipx install uv uvx`

### Run the calculator
`uvx --from git+https://github.com/friscorose/textual-rpn15c.git rpn-15c`

### Or install into your env
```bash
uv tool install --from git+https://github.com/friscorose/textual-rpn15c.git textual-rpn15c
```
then run straight from your CLI
```bash
rpn-15c
```

## The older method
Clone this repo, create a pip environment, add textual and start rpn_15c.py with Python.

Establish your TUI environment... do this only once
``` bash
$  echo $COLUMNS
$  echo $LINES
$  mkdir rpn_test_dir
$  cd rpn_test_dir
$  git clone https://github.com/friscorose/textual-rpn15c.git
$  python -m venv .venv
$  .venv/bin/python -m pip install textual
```
Start the calculator...
``` bash
$  source rpn_test_dir/.venv/bin/activate
$  python rpn_test_dir/textual-rpn15c/src/textual_rpn15c/rpn_15c.py
$  deactivate 
```
or as a one liner.
``` bash
rpn_test_dir/.venv/bin/python rpn_test_dir/textual-rpn15c/src/textual_rpn15c/rpn_15c.py
```
