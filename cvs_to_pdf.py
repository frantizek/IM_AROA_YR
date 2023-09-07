import pdfkit
import pandas as pd

df = pd.read_csv('gremio_aroa.csv')
html_table = df.to_html()

options = {    'page-size': 'Letter',
   'margin-top': '0mm',
   'margin-right': '0mm',
   'margin-bottom': '0mm',
   'margin-left': '0mm'
}


def get_options():
   return {
      'encoding': 'UTF-8',
      'enable-local-file-access': True
   }


pdfkit.from_string(html_table, 'outputs.pdf', verbose=True, options=get_options())
