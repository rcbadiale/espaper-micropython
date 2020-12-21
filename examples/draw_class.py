"""
This is an example file on how to use the Draw class implemented at
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
from draw import Draw
from font import font


def main(portrait=False):
    d = Draw(portrait)

    width = d.size[0]
    height = d.size[1]

    # Center pixel
    d.pixel(width // 2, height // 2, 0)

    # 3-by-3 vertical lines
    for i in range(height):
        d.pixel(width // 3, i, 0)
        d.pixel(2 * width // 3, i, 0)
    # 3-by-3 horizontal lines
    for i in range(width):
        d.pixel(i, height // 3, 0)
        d.pixel(i, 2 * height // 3, 0)

    # Diagonals
    d.line(0, 0, width - 1, height - 1, 0)
    d.line(0, height - 1, width - 1, 0, 0)

    # Center lines
    d.hline(0, height // 2, width, 0)
    d.vline(width // 2, 0, height, 0)

    # Sixths box using all the lines functions
    # Horizontal and Vertical lines using the hline and vline functions
    d.hline(width // 6, height // 6, 4 * width // 6, 0)
    d.vline(width // 6, height // 6, 4 * height // 6, 0)
    # Horizontal and Vertical lines using the line functions
    d.line(width // 6, 5 * height // 6, 5 * width // 6, 5 * height // 6, 0)
    d.line(5 * width // 6, height // 6, 5 * width // 6, 5 * height // 6, 0)

    # Quarter box using rect function
    d.rect(width // 4, height // 4, 3 * width // 4, 3 * height // 4, 0)

    # Third box using rect function with fill
    d.rect(width // 3, height // 3, 2 * width // 3, 2 * height // 3, 0, True)

    # Circle
    radius = min(height // 3, width // 3)
    d.circle(width // 2, height // 2, radius, 0)

    # Circle with fill
    radius = min(height // 6, width // 6)
    d.circle(width // 6, height // 2, radius, 0, True)

    # Write "this is only a text" at the origin of the display
    d.text('this is only a text', 0, 0, 0)

    # Write every available character on the screen.
    all_chars = sorted(font.keys())
    y = height
    x = 0
    for n, letter in enumerate(all_chars):
        if (n * 8) % width == 0:
            y -= 8
            x = 0
        else:
            x += 8
        d.text(letter, x, y, 0)

    d.draw()
