import pdfkit


config = pdfkit.configuration(wkhtmltopdf = 'wkhtmltopdf/bin/wkhtmltopdf.exe')
pdfkit.from_file('cupon/templates/index.html', 'out.pdf', configuration=config)

