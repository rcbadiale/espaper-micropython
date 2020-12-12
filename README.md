# ESPaper with MicroPython

This module creates the interface between the main code and the EPaper display on the ESPaper from Thingpulse.

The pins on this module are fixed as shown below, since the display is attached to the ESP8266 through the ESPaper board.

## Board
### Model
ESPaper - 2.9 inch E-Paper Display with ESP8266
### Pinout
    | PIN     | NAME  | DESCRIPTION                                      |
    |---------|-------|--------------------------------------------------|
    | 2       | RESET | LOW will enable the RESET                        |
    | 4       | BUSY  | HIGH when Display is busy, LOW when IDLE         |
    | 5       | DC    | LOW will write COMMANDS, HIGH will write DATA    |
    | 14      | CS    | LOW will enable comminucation to the Display     |
    | DEFAULT | SPI   | 4-wire communication using the SPI1 from ESP8266 |
### Link
    https://thingpulse.com/product/espaper-lite-kit-wifi-epaper-display/

## Display:
### Model
    GooDisplay 2.9 inch e-paper display GDEH029A1
### Link
    https://www.good-display.com/product/201.html
### Datasheet
    docs\GDEH029A1-1.pdf