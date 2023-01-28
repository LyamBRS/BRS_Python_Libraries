import cairocffi as cairo

svg_file = r"C:\Users\cous5\Documents\BRS_Documents\Librairies\Icons\Applications\Icons_BRS\Logos\UniLetters\BRS_B.svg"
png_file = r"C:\Users\cous5\Documents\BRS_Documents\Librairies\Icons\Applications\Icons_BRS\Logos\UniLetters\BRS_B.png"

with open(svg_file, "rb") as f:
    svg_data = f.read()

with open(png_file, "wb") as f:
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
    context = cairo.Context(surface)
    cairo.SVGSurface.create_for_stream(context, f.write, 100, 100)
    context.show_svg_element(svg_data)