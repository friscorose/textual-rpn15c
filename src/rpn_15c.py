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
from textual.reactive import var
from textual.widgets import Button, Digits, Label, Static
from textual.widget import Widget


class HP_Display( Widget ):
    value = var("")
    n_digits = 10
    off_val = "-"+",".join( "8"*n_digits )
    status_strs = ["USER", "f", "g", "BEGIN", "GRAD", "DMY", "C", "PRGM"]
    lcd_digs = [None]*n_digits
    lcd_seps = [None]*n_digits
    
    def __init__(self, id:str | None=None) -> None:
        super().__init__( id=id )

    def compose(self) -> ComposeResult:
        with Vertical( id="lcd_display" ):
            with Horizontal( id="lcd_digits" ):
                for i in range( self.n_digits ):
                    if i: self.lcd_seps[i] = Digits( classes="lcd separator idx_"+ str(i) )
                    else: self.lcd_seps[i] = Digits( classes="lcd negative idx_"+ str(i) )
                    self.lcd_digs[i] = Digits( classes="lcd digit idx_"+ str(i) )
                    yield self.lcd_seps[i]
                    yield self.lcd_digs[i]
                yield Digits( " ", classes="separator idx_"+ str(self.n_digits-1) )
            with Horizontal( id="lcd_status" ):
                for l in self.status_strs:
                    yield Label( l, id=l+"-state", classes="lcd" )

    def watch_value(self, value) -> None:
        self.parse_value()

    def parse_value(self) -> None:
        buffer = self.value
        n_chars = len( buffer )
        for idx in range( self.n_digits ):
            if n_chars:
                if buffer[0] in '-.,':
                    self.lcd_seps[idx].update( buffer[0] )
                    self.lcd_seps[idx].add_class("active")
                    buffer = buffer[1:]
                    n_chars -= 1
                if n_chars and buffer[0] in '0123456789':
                    self.lcd_digs[idx].update( buffer[0] )
                    self.lcd_digs[idx].add_class("active")
                    buffer = buffer[1:]
                    n_chars -= 1
            else:
                self.lcd_seps[idx].remove_class("active")
                self.lcd_seps[idx].update( self.off_val[ 2*idx ] )
                self.lcd_digs[idx].remove_class("active")
                self.lcd_digs[idx].update( self.off_val[ 2*idx+1] )


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
        lcd_display = self.query(".lcd")
        lcd_display.add_class("active")
        await sleep( 1.0 )
        lcd_display.remove_class("active")
        await sleep( 0.25 )
        self.query_one("HP_Display").value = ""
        self.query_one("HP_Display").value = "0.0000"
        

if __name__ == "__main__":
    RPN_CalculatorApp().run()
