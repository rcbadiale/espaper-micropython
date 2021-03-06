"""
This is an example file on how to use the Display class implemented at
https://github.com/rcbadiale/espaper-micropython.

MIT License

Copyright (c) 2020 Rafael C. Badiale.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from time import sleep

import epaper
import framebuf


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
