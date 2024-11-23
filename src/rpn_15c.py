#!/usr/bin/env python3

"""
A visual implementation of a classic 15c RPN calculator.
see [https://en.wikipedia.org/wiki/HP-15C]
or [https://www.hpmuseum.org/forum/archive/index.php?thread-19260.html]
looks like a real calculator.
"""

import math
from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.reactive import var
from textual.widgets import Button, Digits, Label, Static
from textual.widget import Widget


class HP_Display( Widget ):
    """LCD panel that approximates the HP 15c layout"""

    DEFAULT_CSS = """
    HP_Display {
        text-style: bold;
        margin-left: 16;
        height: 7;
        width:45;
        /* bezel */
        background: darkgrey 40%;
        padding: 1;

        #lcd_display {
            background: aquamarine 20%;
            color: darkslategray 10%;
            .lcd.active{
                color: darkslategray 100%;
            }
            #lcd_digits {
                Digits {
                    border-top: tall slategray 50%;
                }
                .separator {
                    width:1;
                }
            }
            #lcd_status {
                height: 1;
                padding-left: 3;
                Label {
                    margin-left: 2;
                }
            }
        }
    }
    """
    
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

    def watch_value(self) -> None:
        self.parse_value()

    def parse_value(self) -> None:
        buffer = self.value
        n_chars = len( buffer )
        for idx in range( self.n_digits ):
            self.lcd_seps[idx].remove_class("active")
            self.lcd_seps[idx].update( self.off_val[ 2*idx ] )
            self.lcd_digs[idx].remove_class("active")
            self.lcd_digs[idx].update( self.off_val[ 2*idx+1] )
            if n_chars:
                if buffer[0] in '-.,':
                    self.lcd_seps[idx].update( buffer[0] )
                    self.lcd_seps[idx].add_class("active")
                    buffer = buffer[1:]
                    n_chars -= 1
                if n_chars and buffer[0] in '0123456789ABCDEF':
                    self.lcd_digs[idx].update( buffer[0] )
                    self.lcd_digs[idx].add_class("active")
                    buffer = buffer[1:]
                    n_chars -= 1


class HP_Buttons( Container ):
    class HP_Button( Button ):
        def __init__(self, *args, **kwargs):
            super().__init__( id=kwargs["id"] )
            self.label = args[0]
            self.border_title = args[1]
            self.border_subtitle = args[2]

    def compose(self) -> ComposeResult:
        calc_buttons =  Grid(id="hp_buttons")
        calc_buttons.border_subtitle = " H   E   W   L   E   T   T  •  P   A   C   K   A   R   D "
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

    number_X = var( float('nan') )
    buffer_X = var("")
    angle_M = var('deg')


    def state_reset( self ) -> None:
        self.state= {}
        self.state['fix'] = 4
        self.state['angle_deg'] = True
        self.state['angle_rad'] = False
        self.state['angle_grad'] = False
        self.state['X'] = float( 'nan' )
        self.state['Y'] = float( 'nan' )
        self.state['Z'] = float( 'nan' )
        self.state['T'] = float( 'nan' )
        self.angle_M = 'deg'

    def on_mount( self ):
        self.state_reset()

    def compose(self) -> ComposeResult:
        """Add our buttons."""
        with Container(id="calculator"):
            with Horizontal(id="upper"):
                yield HP_Display( id="hp_display" )
                with Vertical(id="logo"):
                    yield Label("hp", id="rpn-make")
                    yield Label("15 C", id="rpn-model")
            yield HP_Buttons( )

    def watch_number_X(self):
        if math.isnan( self.number_X ):
            self.query_one("HP_Display").value = '{0:,.{1}f}'.format(0, self.state['fix'])
        else:
            self.query_one("HP_Display").value = '{0:,.{1}f}'.format(self.number_X, self.state['fix'])

    def watch_buffer_X(self):
        self.query_one("HP_Display").value = self.buffer_X

    def enter_actions( self ) -> None:
        if self.buffer_X:
            self.push_X( float(self.buffer_X) )
            self.buffer_X = ""
        self.number_X = self.state['X']

    def watch_angle_M(self):
        self.state['angle_deg'] = False
        self.state['angle_rad'] = False
        self.state['angle_grad'] = False
        angle_status = self.query_one("#GRAD-state")
        angle_status.remove_class( "active" )
        angle_status.update( "GRAD" )
        if self.angle_M == 'grad':
            angle_status.add_class( "active" )
            self.state['angle_grad'] = True
        elif self.angle_M == 'rad':
            angle_status.update( " RAD" )
            angle_status.add_class( "active" )
            self.state['angle_rad'] = True
        else:
            self.angle_M = 'deg'
            self.state['angle_deg'] = True

    def pop_T(self) -> float:
        number = self.state['T']
        self.state['T'] = float( 'nan' )
        return number

    def pop_Z(self) -> float:
        number = self.state['Z']
        self.state['Z'] = self.pop_T()
        return number

    def pop_Y(self) -> float:
        number = self.state['Y']
        self.state['Y'] = self.pop_Z()
        return number

    def pop_X(self) -> float:
        number = self.state['X']
        self.state['X'] = self.pop_Y()
        return number

    def push_X(self, number) -> None:
        self.state['T'] = self.state['Z']
        self.state['Z'] = self.state['Y']
        self.state['Y'] = self.state['X']
        self.state['X'] = number

    @on( Button.Pressed )
    def toggle_status( self, event ) -> None:
        if event.button.id == "shift-f":
            self.query_one( "#f-state" ).toggle_class( "active" )
        if event.button.id == "shift-g":
            self.query_one( "#g-state" ).toggle_class( "active" )

        if event.button.id == "enter":
            self.enter_actions()

        if event.button.id == "digit-0":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.factorial( int( self.pop_X() ) )
                self.number_X = self.state['X']
            else:
                self.buffer_X += "0"
        if event.button.id == "digit-1":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "1"
        if event.button.id == "digit-2":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "2"
        if event.button.id == "digit-3":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "3"
        if event.button.id == "digit-4":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "4"
        if event.button.id == "digit-5":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "5"
        if event.button.id == "digit-6":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "6"
        if event.button.id == "digit-7":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.angle_M = 'deg'
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['fix'] = int( self.pop_X() )
                self.number_X = self.state['X']
            else:
                self.buffer_X += "7"
        if event.button.id == "digit-8":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.angle_M = 'rad'
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "8"
        if event.button.id == "digit-9":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.angle_M = 'grad'
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.buffer_X += "9"
        if event.button.id == "decimal":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                if "." not in self.buffer_X:
                    if self.buffer_X: 
                        self.buffer_X += "."
                    else:
                        self.buffer_X += "0."
        
        
        if event.button.id == "addition":
            self.enter_actions()
            self.state['X'] += self.pop_Y()
            self.number_X = self.state['X']
        
        if event.button.id == "subtraction":
            self.enter_actions()
            self.state['X'] = self.pop_Y() - self.state['X']
            self.number_X = self.state['X']
        
        if event.button.id == "multiplication":
            self.enter_actions()
            self.state['X'] *= self.pop_Y()
            self.number_X = self.state['X']

        if event.button.id == "division":
            self.enter_actions()
            self.state['X'] = self.pop_Y() / self.state['X']
            self.number_X = self.state['X']

        if event.button.id == "sqrt-x":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] =  self.pop_X()**2
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.buffer_X += 'A'
            else:
                self.enter_actions()
                self.state['X'] = math.sqrt( self.pop_X() )
                self.number_X = self.state['X']

        if event.button.id == "exp-x":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.log( self.pop_X() )
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.buffer_X += 'B'
            else:
                self.enter_actions()
                self.state['X'] = math.exp( self.pop_X() )
                self.number_X = self.state['X']

        if event.button.id == "ten-x":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.log( self.pop_X(), 10 )
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.buffer_X += 'C'
            else:
                self.enter_actions()
                self.state['X'] = 10**self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "wye-x":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.buffer_X += 'D'
            else:
                self.enter_actions()
                self.state['X'] = self.pop_Y()**self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "inverse-x":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.buffer_X += 'E'
            else:
                self.enter_actions()
                self.state['X'] = 1/self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "chs":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = abs( self.pop_X())
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.enter_actions()
                self.state['X'] = -1*self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "sst":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "gto":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "sin":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.enter_actions()
                if self.state[ 'angle_deg' ]:
                    self.state['X'] = math.sin(math.radians( self.pop_X() ))
                elif self.state[ 'angle_rad' ]:
                    self.state['X'] = math.sin( self.pop_X() )
                elif self.state[ 'angle_grad' ]:
                    self.state['X'] = math.sin( self.pop_X()*math.pi/200 )
                self.state['X'] = self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "cos":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.enter_actions()
                if self.state[ 'angle_deg' ]:
                    self.state['X'] = math.cos(math.radians( self.pop_X() ))
                elif self.state[ 'angle_rad' ]:
                    self.state['X'] = math.cos( self.pop_X() )
                elif self.state[ 'angle_grad' ]:
                    self.state['X'] = math.cos( self.pop_X()*math.pi/200 )
                self.state['X'] = self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "tan":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                self.enter_actions()
                if self.state[ 'angle_deg' ]:
                    self.state['X'] = math.tan(math.radians( self.pop_X() ))
                elif self.state[ 'angle_rad' ]:
                    self.state['X'] = math.tan( self.pop_X() )
                elif self.state[ 'angle_grad' ]:
                    self.state['X'] = math.tan( self.pop_X()*math.pi/200 )
                self.state['X'] = self.pop_X() 
                self.number_X = self.state['X']

        if event.button.id == "eex":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.pi
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "rtos":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass
        if event.button.id == "gsb":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "r-down":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "x-swap-y":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "backspace":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "sto":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.modf( self.state['X'] )[1]
                self.number_X = self.state['X']
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
                self.enter_actions()
                self.state['X'] = math.modf( self.state['X'] )[0]
                self.number_X = self.state['X']
            else:
                pass

        if event.button.id == "rcl":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass

        if event.button.id == "sum":
            if self.query_one( "#g-state" ).has_class("active"):
                self.query_one( "#g-state" ).toggle_class( "active" )
            elif self.query_one( "#f-state" ).has_class("active"):
                self.query_one( "#f-state" ).toggle_class( "active" )
            else:
                pass



    @on( Button.Pressed, "#on" )
    def calculator_post( self ) -> None:
        self.query_one("HP_Display").value = ""
        lcd_display = self.query(".lcd")
        lcd_display.add_class("active")
        self.set_timer( 1, self.state_clear )
        
    def state_clear( self ) -> None:
        lcd_display = self.query(".lcd").remove_class("active")
        self.state_reset()
        self.buffer_X = "" 
        self.number_X = float('nan')

def main_cli( self ) -> None:
    RPN_CalculatorApp().run()

if __name__ == "__main__":
    main_cli()
