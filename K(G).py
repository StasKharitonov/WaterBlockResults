import openpyxl
from parser import column_headers, get_column_by_header, get_sheet
from utils import valid_file_name
import statistics

# k = (Q // (F1 * dt))

sheetlist = valid_file_name()
for filename in sheetlist:
    sheet = get_sheet(filename)

headers_to_find = ['Qiv', 'Tin', 'Tout']
column_numbers = {}
for header in headers_to_find:
    column_numbers[header] = get_column_by_header(sheet, column_headers[header])
print(column_numbers)

header_idx = {
    'Qiv_idx': column_numbers['Qiv'] - 1,
    'Tin_idx': column_numbers['Tin'] - 1,
    'Tout_idx': column_numbers['Tout'] - 1,
    
}
print(header_idx)

Qiv_Tin_Tout_values = []
for row in sheet.iter_rows(values_only=True):
    Qiv = row[header_idx['Qiv_idx']]
    Tin = row[header_idx['Tin_idx']]
    Tout = row [header_idx['Tout_idx']]
    Qiv_Tin_Tout_values.append({
        'Qiv': Qiv,
        'Tin': Tin,
        'Tout': Tout
    })

# Qiv = sorted(Qiv_Tin_Tout_values[0][Qiv])


print(Qiv_Tin_Tout_values)
print(sheet)
print(sheetlist)
