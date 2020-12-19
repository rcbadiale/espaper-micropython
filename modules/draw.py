import framebuf

from epaper import Display


class Draw(Display):
    def __init__(self, portrait=False, fast=False):
        super(Draw, self).__init__(portrait, fast)
        if self.portrait:
            orientation = framebuf.MONO_HLSB
        else:
            orientation = framebuf.MONO_VLSB
        
        self.fb = framebuf.FrameBuffer(
            self.image,
            self.size[0],
            self.size[1],
            orientation
        )

    def draw(self):
        self.write_image()
        self.update()

    def text(self, text, x, y, color):
        self.fb.text(text, x, y, color)

    def pixel(self, x, y, color):
        self.fb.pixel(x, y, color)

    def line(self, xi, yi, xf, yf, color):
        self.fb.line(xi, yi, xf, yf, color)

    def hline(self, x, y, length, color):
        self.fb.hline(x, y, length, color)

    def vline(self, x, y, height, color):
        self.fb.vline(x, y, height, color)
