from machine import Pin, SPI
from time import sleep_ms


class Display:
    """
    This class creates the interface between the main code and
    the EPaper display on the ESPaper from Thingpulse.

    Display model: GooDisplay 2.9 inch e-paper display GDEH029A1

    The pins on this module are fixed as shown below, since the
    display is attached to the ESP8266 through the ESPaper board.

    Pinout:
      | NAME  | PIN     | DESCRIPTION                                      |
      | DC    | 5       | LOW will write COMMANDS, HIGH will write DATA    |
      | RESET | 2       | LOW will enable the RESET                        |
      | CS    | 14      | LOW will enable comminucation to the Display     |
      | BUSY  | 4       | is HIGH when Display is busy, LOW when IDLE      |
      | SPI   | default | 4-wire communication using the SPI1 from ESP8266 |
    
    Args:
      portrait (bool): Set the (0, 0) position on the top-right corner.
      fast (bool): Set the display for partial / fast refresh.
    """
    def __init__(self, portrait=False, fast=False):
        # Screen size (x, y)
        self.size = (296, 128)
        self.portrait = portrait

        # Refresh mode
        self.fast = fast

        # Image size, pre-alocation and lookup table
        self.n_bytes = self.size[0] * self.size[1] // 8
        self.image = bytearray()
        self.blank_image()
        self.lut_full = (
            b'\x50\xaa\x55\xaa\x11\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\xff\xff\x1f\x00'
            b'\x00\x00\x00\x00\x00\x00'
        )
        self.lut_partial = (
            b'\x10\x18\x18\x08\x18\x18'
            b'\x08\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x13\x14\x44\x12'
            b'\x00\x00\x00\x00\x00\x00'
        )

        # Board -> Display pinout
        pins = {
            'DC': (5, Pin.OUT),
            'RESET': (2, Pin.OUT),
            'CS': (15, Pin.OUT),
            'BUSY': (4, Pin.IN),
        }

        # Pins definition
        self.dc = Pin(*pins.get('DC'))
        self.rst = Pin(*pins.get('RESET'))
        self.cs = Pin(*pins.get('CS'))
        self.busy = Pin(*pins.get('BUSY'))

        # SPI definition
        self.spi = SPI(1, baudrate=4000000, polarity=0, phase=0)

        # Display first cycle
        self.dc.on()
        self.cs.on()
        self.rst.on()
        self.reset()

    def reset(self):
        """Display reset cycle."""
        self.rst.off()
        sleep_ms(10)
        self.rst.on()
        sleep_ms(10)

    def blank_image(self, black=False):
        """
        Set a blank image with the desired color.

        args:
          - black (bool): black image when True, white image when False
        """
        self.image = bytearray()
        if black:
            self.image = bytearray(b'\x00' * self.n_bytes)
        else:
            self.image = bytearray(b'\xff' * self.n_bytes)

    def wait_until_idle(self):
        """Display idle check to avoid sending commands when busy."""
        while self.busy.value() == 1:
            sleep_ms(10)

    def write_cmd(self, cmd):
        """
        Prepare the display then send the command to it.

        args:
          - cmd (bytearray): command to be sent to the display.
        """
        self.wait_until_idle()
        self.cs.off()
        self.dc.off()
        self.spi.write(cmd)
        self.cs.on()

    def write_data(self, data):
        """
        Prepare the display then send the data to it.

        args:
          - data (bytearray): data to be sent to the display.
        """
        self.wait_until_idle()
        self.cs.off()
        self.dc.on()
        self.spi.write(data)
        self.cs.on()

    def set_memory_area(self):
        """
        Set the position to write in the RAM.
        """
        # Set RAM-X Address Start-End Position
        self.write_cmd(b'\x44')
        if self.portrait:
            self.write_data(b'\x00\x0f')
        else:
            self.write_data(b'\x0f\x00')
        # Set RAM-Y Address Start-End Position
        self.write_cmd(b'\x45')
        if self.portrait:
            self.write_data(b'\x00\x00\x27\x01')
        else:
            self.write_data(b'\x27\x01\x00\x00')

    def set_memory_pointer(self):
        """
        Set the memory pointer position to write to the RAM.
        """
        # Set RAM-X Address count
        self.write_cmd(b'\x4e')
        if self.portrait:
            self.write_data(b'\x00')
        else:
            self.write_data(b'\x0f')
        # Set RAM-Y Address count
        self.write_cmd(b'\x4f')
        if self.portrait:
            self.write_data(b'\x00\x00')
        else:
            self.write_data(b'\x27\x01')

    def init(self):
        """
        Prepare the display for normal operation.

        The basic sequence of commands is found on the
        datasheet of the display.
        """
        # Driver Output Control
        print('Driver Output Control')
        self.write_cmd(b'\x01')
        self.write_data(b'\x27\x01\x00')
        # Booster soft start
        print('Booster soft start')
        self.write_cmd(b'\x0C')
        self.write_data(b'\xd7\xd6\x9d')
        # VCOM Voltage
        print('VCOM Voltage')
        self.write_cmd(b'\x2c')
        self.write_data(b'\xa8')
        # Dummy Line
        print('Dummy Line')
        self.write_cmd(b'\x3a')
        self.write_data(b'\x1a')
        # Gate Time
        print('Gate Time')
        self.write_cmd('\x3b')
        self.write_data('\x08')
        # Data Entry Mode
        print('Data Entry Mode')
        self.write_cmd(b'\x11')
        if self.portrait:
            self.write_data(b'\x03')
        else:
            self.write_data(b'\x04')
        # Border Wave Form
        print('Border Wave Form')
        self.write_cmd(b'\x3c')
        self.write_data(b'\x33')
        # Set Memory Area
        print('Set Memory Area')
        self.set_memory_area()
        # Set Memory Pointer
        print('Set Memory Pointer')
        self.set_memory_pointer()
        # Write LUT (LookUpTable)
        print('Write LUT')
        self.write_cmd(b'\x32')
        if self.fast:
            self.write_data(self.lut_partial)
        else:
            self.write_data(self.lut_full)

    def write_image(self):
        """
        Write the image to the Display RAM.

        Send the command to write data to RAM then send
        the IMAGE to it.
        """
        self.set_memory_area()
        self.set_memory_pointer()
        self.write_cmd(b'\x24')
        self.write_data(self.image)

    def update(self):
        """
        Show the image from RAM on the display.

        Send the command to update the display then send
        the command to activate it.
        """
        self.write_cmd(b'\x22')
        self.write_data(b'\xc4')
        self.write_cmd(b'\x20')
        self.write_cmd(b'\xff')

    def full_refresh(self):
        self.blank_image(True)
        self.write_image()
        self.update()
        sleep_ms(300)
        self.blank_image()
        self.write_image()
        self.update()
