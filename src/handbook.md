# RPN 15C User's Handbook

A visual TUI mimicry of classic HP 15C pocket calculator. Just as
the appearance is only similar, so to is the operation only similar.

All operations are based on reverse polish notation or RPN where an
operation is performed on data previosly entered into a stack of values.

In this handbook the square brackets around an identifier denote a button.

# Operations

## Nullary Operations

These operations are considered immediate operations and do not make use of
values on the stack. One can consider these to be state change operations. The
simplest is turning on the interface by pressing the [ON] button, which also
resets the calculator. In order to have more inputs than 'physical' buttons
there are also the [f] and [g] shift states. Another use for state is a change
of basis like setting the angular metric for trigonometric functions. The
default here is that angles are measured in degrees so that [1][8][0][COS]
evaluates to -1.0000 as a result, but [g][RAD] (on the 8 button) which means
that [g][π][COS] now evaluates to -1.0000 as the result.

## Unary Operations

The simplest value operations are unary, that is they perform an action on a
single stack level. An example of a unary operation is setting the display
precision which defaults to four digits after the decimal. To change it to
three digits type [3] then the [f] shift and [FIX] (on the [7]).

Another single value operation would be the square root function. Type in
any number, say [1][6][9] then press the [√x] button at the top left.

## Binary Operations

Most arithmetic operations process two values, for instance the addition [+]
which which will add a second value to a first value already entered. For
example typing [3] [ENTER] [2] [+] results in an answer of 5.
