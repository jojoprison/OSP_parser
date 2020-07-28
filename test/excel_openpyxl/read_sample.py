import openpyxl

excel_doc = openpyxl.load_workbook("sample.xlsx")

print(type(excel_doc))

sheet = excel_doc["Sheet1"]
print(sheet["A2"].value)

multiple_cells = sheet['A1':'B3']
for row in multiple_cells:
    for cell in row:
        print(cell.value)