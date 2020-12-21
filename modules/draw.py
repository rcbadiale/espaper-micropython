"""
Most implementation is based on the framebuf module.
In order for the display to work horizontally the VMSB
implementation, which is not present in the framebuf
module, was needed and is implemented here.
"""
from math import floor, sqrt

from epaper import Display
from font import font


class Draw(Display):
    def __init__(self, portrait=False, fast=False):
        super(Draw, self).__init__(portrait, fast)

    def draw(self):
        """
        Draw the buffered image to the display.
        """
        self.write_image()
        self.update()

    def text(self, text: str, xo: int, yo: int, color: int):
        """
        Write the text in the image buffer at given position with the color.

        args:
          text (str): text to be written.
          xo (int): x position on the screen (left of the first letter).
          yo (int): y position on the screen (bottom of the first letter).
          color (int): 0 = black, 1 = white.
        """
        for offset, letter in enumerate(text):
            template = font.get(letter)
            for x, line in enumerate(template):
                line_str = '{:08b}'.format(line).replace('0b', '')
                if self.portrait:
                    line_str = reversed(line_str)
                for y, pix in enumerate(line_str):
                    if pix == '1':
                        self.pixel(xo + x + (offset * 8), yo + y, color)

    def position(self, x, y):
        if self.portrait:
            # HMSB
            index = (x + y * self.size[0]) >> 3
            offset = 7 - (x & 0x07)
        else:
            # VMSB
            index = (y >> 3) * self.size[0] + x
            offset = 7 - (y & 0x07)
        return index, offset

    def pixel(self, x: int, y: int, color: int):
        """
        Paint a pixel in the buffer with the color.

        args:
          x (int): x position on the screen.
          y (int): y position on the screen.
          color (int): 0 = black, 1 = white.
        """
        if (
            (x < self.size[0] and y < self.size[1]) and (x >= 0 and y >= 0)
        ):
            index, offset = self.position(x, y)
            self.image[index] = (
                self.image[index] & ~(0x01 << offset)
            ) | (
                (color != 0) << offset
            )
        else:
            return

    def line(self, xi: int, yi: int, xf: int, yf: int, color: int):
        """
        Draw a line in the image buffer.

        This is the most generic line function.

        args:
          xi (int): first x position on the screen.
          yi (int): first y position on the screen.
          xf (int): last x position on the screen.
          yf (int): last y position on the screen.
          color (int): 0 = black, 1 = white.
        """
        if xi == xf:
            self.vline(xi, yi, yf - yi, color)
        elif yi == yf:
            self.hline(xi, yi, xf - xi, color)
        else:
            m = (yf - yi) / (xf - xi)

            for x in range(xi, xf + 1):
                y = int(m * (x - xi) + yi)
                self.pixel(x, y, color)

    def hline(self, xi: int, yi: int, length: int, color: int):
        """
        Draw a horizontal line in the image buffer.

        args:
          xi (int): first x position on the screen.
          yi (int): first y position on the screen.
          length (int): the length in pixels of the line to draw.
          color (int): 0 = black, 1 = white.
        """
        for x in range(length):
            self.pixel(xi + x, yi, color)

    def vline(self, xi: int, yi: int, length: int, color: int):
        """
        Draw a vertical line in the image buffer.

        args:
          xi (int): first x position on the screen.
          yi (int): first y position on the screen.
          length (int): the length in pixels of the line to draw.
          color (int): 0 = black, 1 = white.
        """
        for y in range(length):
            self.pixel(xi, yi + y, color)

    def rect(self, xi: int, yi: int, xf: int, yf: int, color: int, fill=False):
        """
        Draw a box (filled or not) in the image buffer.

        args:
          xi (int): first x position on the screen.
          yi (int): first y position on the screen.
          xf (int): last x position on the screen.
          yf (int): last y position on the screen.
          color (int): 0 = black, 1 = white.
          fill (bool): if the box should be filled or not.
        """
        width = xf - xi
        height = yf - yi

        if fill:
            for x in range(xi, xf + 1):
                for y in range(yi, yf + 1):
                    self.pixel(x, y, color)
        else:
            self.hline(xi, yi, width, color)
            self.hline(xi, yf, width, color)
            self.vline(xi, yi, height, color)
            self.vline(xf, yi, height, color)

    def circle(self, xo: int, yo: int, radius: int, color: int, fill=False):
        """
        Draw a circle (filled or not) in the image buffer.

        Will raise an error if the radius is too big.

        args:
          xo (int): x center position on the screen.
          yo (int): y center position on the screen.
          radius (int): radius of the circle in pixels.
          color (int): 0 = black, 1 = white.
          fill (bool): if the circle should be filled or not.
        """
        for x in range(xo - radius, xo + radius + 1):
            square = sqrt(radius ** 2 - (x - xo) ** 2)
            y = yo + square
            self.pixel(x, floor(y), color)
            y = yo - square
            self.pixel(x, floor(y), color)
        for y in range(yo - radius, yo + radius + 1):
            square = sqrt(radius ** 2 - (y - yo) ** 2)
            x = xo + square
            self.pixel(floor(x), y, color)
            x = xo - square
            self.pixel(floor(x), y, color)
        if fill:
            if radius > 1:
                self.circle(xo, yo, radius - 1, color, True)
            else:
                self.circle(xo, yo, radius - 1, color, False)
