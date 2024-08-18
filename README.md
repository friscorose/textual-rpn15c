# A TUI RPN Calculator with an HP 15C themed skin

## Quick Start

In a terminal emulator that is at least 126 characters wide and 31 characters tall perform the following steps:
Clone this repo, create a pip environment, add textual and start rpn_15c.py with Python.

Establish your TUI environment...
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
$  python rpn_test_dir/textual-rpn15c/src/rpn_15c.py
$  deactivate 
```
