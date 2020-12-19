import epaper
import framebuf
from time import sleep

def main(fast=False):
    d = epaper.Display(portrait=True, fast=fast)
    fb = framebuf.FrameBuffer(d.image, 128, 296, framebuf.MONO_HLSB)
    for n in range(16):
        fb.text('Hello', n * 8, n * 8, 0)
    for n in range(24):
        fb.text('olleH', 128 - (n * 8), (15 + n) * 8, 0)
    fb.line(0, 0, 128, 296, 0)
    fb.line(0, 296, 128, 0, 0)
    d.write_image()
    d.update()

    sleep(15)

    d = epaper.Display(fast=fast)
    fb = framebuf.FrameBuffer(d.image, 296, 128, framebuf.MONO_VLSB)
    for n in range(16):
        fb.text('this is only a text', n * 8, n * 8, 0)
    fb.line(0, 0, 296, 128, 0)
    fb.line(0, 128, 296, 0, 0)
    d.write_image()
    d.update()

    sleep(15)

    if fast:
        d.full_refresh()
