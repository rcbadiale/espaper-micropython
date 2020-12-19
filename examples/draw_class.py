from draw import Draw


def main():
    width = 296
    height = 128

    d = Draw()

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
    d.line(0, 0, 295, 127, 0)
    d.line(0, 127, 295, 0, 0)

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

    # d.text('this is only a text', 0, 0, 0)
    d.draw()
