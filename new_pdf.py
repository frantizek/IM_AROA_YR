import csv
import fpdf

with open("gremio_aroa.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)

pdf = fpdf.FPDF(orientation = 'L', unit = 'mm', format='A4')

pdf.add_page()

pdf.add_font('DejaVu', '', 'K:/ttf/DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 8)
pdf.set_fill_color(255, 255, 255)
pdf.set_draw_color(0, 0, 0)

for header in data[0]:
    pdf.cell(100, 10, header, 1, 0, "C", True)

for row in data[1:]:
    for cell in row:
        pdf.cell(100, 10, cell, 1, 0, "C")

pdf.output("data.pdf")