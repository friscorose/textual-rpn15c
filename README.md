# A TUI RPN Calculator with an HP 15C theme
![rpn_15c](https://repository-images.githubusercontent.com/819673411/34048565-6900-495e-99ec-ec8fb407c32b)

and yes, that is just text. Pretty sigma, eh!?

## Quick Start

In a modern terminal emulator that is at least 126 characters wide and 31 characters tall perform the following steps:
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
or as a one liner...
``` bash
rpn_test_dir/.venv/bin/python rpn_test_dir/textual-rpn15c/src/rpn_15c.py
```
