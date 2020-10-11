import pandas as pd
import numpy as np

### creating timestamp ###
ts = pd.Timestamp.now()
ts = str(ts.ceil(freq='1T'))   #rounding the timestamp to the nearest next minute
ts = ts.replace(':','-')

### read in file ###
infile = 'organisation-test.xlsx'
df = pd.read_excel(infile, usecols = "A:R") 

### format output file ###
filename = 'organisation-test'+ts+'.xlsx'

writer = pd.ExcelWriter(filename, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index = False)

workbook  = writer.book
worksheet = writer.sheets['Sheet1']

#change sheet size to match column width (manually, this does not auto-fit)
worksheet.set_column('A:A', 4)  # ID column, width for larger number (>999)
worksheet.set_column('B:B', 17) # name column
worksheet.set_column('C:C', 9)  # category column
worksheet.set_column('D:D', 17)
worksheet.set_column('E:E', 17)
worksheet.set_column('F:G', 15)
worksheet.set_column('H:H', 12)
worksheet.set_column('I:I', 12)
worksheet.set_column('J:J', 15)
worksheet.set_column('M:N', 17) # timestamps fit perfectly inside width=17 cells (in excel)
worksheet.set_column('O:O', 12)
worksheet.set_column('Q:Q', 12) # measured effort 
#column p is comment, no need for setting any width because it is the last column

writer.save()

print('successfully backed up {}'.format(filename))