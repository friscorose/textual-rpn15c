#!/usr/bin/env python3

"""
A visual implementation of a classic 15c RPN calculator.
see [https://en.wikipedia.org/wiki/HP-15C]
or [https://www.hpmuseum.org/forum/archive/index.php?thread-19260.html]
looks like a real calculator.
"""

from asyncio import sleep
from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.reactive import reactive
from textual.widgets import Button, Digits, Label, Static

class HP_Display( Container ):
    def __init__(self, *args, **kwargs):
        self.post_value = "-8,8,8,8,8,8,8,8,8,8,"
        super().__init__( id=kwargs["id"] )

    def compose(self) -> ComposeResult:
        with Vertical( ):
            yield Digits( self.post_value , id="numbers", classes="lcd" )
            with Horizontal( id="status" ):
                yield Label( "USER", id="user-state", classes="lcd" )
                yield Label( "f", id="f-shift-state", classes="lcd" )
                yield Label( "g", id="g-shift-state", classes="lcd" )
                yield Label( "BEGIN", id="begin-state", classes="lcd" )
                yield Label( "GRAD", id="grad-state", classes="lcd" )
                yield Label( "DMY", id="dmy-state", classes="lcd" )
                yield Label( "C", id="c-state", classes="lcd" )
                yield Label( "PRGM", id="prgm-state", classes="lcd" )


class HP_Buttons( Container ):
    class HP_Button( Button ):
        def __init__(self, *args, **kwargs):
            super().__init__( id=kwargs["id"] )
            self.label = args[0]
            self.border_title = args[1]
            self.border_subtitle = args[2]

    def compose(self) -> ComposeResult:
        calc_buttons =  Grid(id="hp_buttons")
        calc_buttons.border_subtitle = "H   E   W   L   E   T   T  •  P   A   C   K   A   R   D"
        with calc_buttons:
            yield self.HP_Button("√x", "A", "  x²   ", id="sqrt-x")
            yield self.HP_Button("eˣ", "B", "  LN   ", id="exp-x")
            yield self.HP_Button("10ˣ", "C", "  LOG  ", id="ten-x")
            yield self.HP_Button(" yˣ", "D", "   %   ", id="wye-x")
            yield self.HP_Button("1/x", "E", "  Δ%   ", id="inverse-x")
            yield self.HP_Button("CHS", " MATRIX", "  ABS  ", id="chs")
            yield self.HP_Button("7", "FIX", "  DEG  ", id="digit-7")
            yield self.HP_Button("8", "SCI", "  RAD  ", id="digit-8")
            yield self.HP_Button("9", "ENG", "  GRD  ", id="digit-9")
            yield self.HP_Button("÷", "SOLVE", "  x≤y  ", id="division")

            yield self.HP_Button("SST", "LBL", "  BST  ", id="sst")
            yield self.HP_Button("GTO", "HYP", " HYP⁻¹ ", id="gto")
            yield self.HP_Button("SIN", "DIM", " SIN⁻¹ ", id="sin")
            yield self.HP_Button("COS", "(i)", " COS⁻¹ ", id="cos")
            yield self.HP_Button("TAN", "I", " TAN⁻¹ ", id="tan")
            yield self.HP_Button("EEX", " RESULT", "   π   ", id="eex")
            yield self.HP_Button("4", "x ≷", "  S F  ", id="digit-4")
            yield self.HP_Button("5", "DSE", "  C F  ", id="digit-5")
            yield self.HP_Button("6", "ISG", "  F ?  ", id="digit-6")
            yield self.HP_Button("×", "∫ᵧˣ", "  x=0  ", id="multiplication")

            yield self.HP_Button("R/S", "PSE", "  P/R  ", id="rtos")
            clear_cluster =  Grid(id="cluster")
            clear_cluster.border_title = "╭───────────────── CLEAR ──────────────────╮  "
            with clear_cluster:
                yield self.HP_Button("GSB", "Σ", "  RTN  ", id="gsb")
                yield self.HP_Button("R↓", "PRGM", "  R↑   ", id="r-down")
                yield self.HP_Button("x ≷ y", "REG", "  RND  ", id="x-swap-y")
                yield self.HP_Button("←", "PREFIX", "  CLx  ", id="backspace")
            yield self.HP_Button("E\nN\nT\nE\nR", " RAN # ", " LSTx  ", id="enter")
            yield self.HP_Button("1", "→ R", "  → P  ", id="digit-1")
            yield self.HP_Button("2", "→H.MS", "  → H  ", id="digit-2")
            yield self.HP_Button("3", "→RAD", " →DEG  ", id="digit-3")
            yield self.HP_Button("−", "Re ≷ Im", "  TEST ", id="subtraction")

            yield self.HP_Button("ON", "", "", id="on")
            yield self.HP_Button("f", "", "       ", id="shift-f")
            yield self.HP_Button("g", "", "       ", id="shift-g")
            yield self.HP_Button("STO", "FRAC", "  INT  ", id="sto")
            yield self.HP_Button("RCL", "USER", "  MEM  ", id="rcl")
            yield self.HP_Button("0", "x!", "   x̄   ", id="digit-0")
            yield self.HP_Button("•", "s", "  ŷ,r  ", id="decimal")
            yield self.HP_Button("Σ+", "L.R.", "  Σ-   ", id="sum")
            yield self.HP_Button("+", "Py,x", " Cy,x  ", id="addition")

class RPN_CalculatorApp(App):
    """A working TUI calculator."""
    CSS_PATH = "rpn_15c.tcss"

    def compose(self) -> ComposeResult:
        """Add our buttons."""
        with Container(id="calculator"):
            with Horizontal(id="upper"):
                yield HP_Display( id="hp_display" )
                with Vertical(id="logo"):
                    yield Label("hp", id="rpn-make")
                    yield Label("15 C", id="rpn-model")
            yield HP_Buttons( )

    @on( Button.Pressed, "#on" )
    async def calculator_post( self ) -> None:
        hp_lcd = self.query(".lcd")
        hp_lcd.add_class("active")
        await sleep( 0.5 )
        hp_status = self.query("Label")
        hp_status.remove_class("active")
        self.query_one("Digits").update( "0.0000" )
        

if __name__ == "__main__":
    RPN_CalculatorApp().run()
