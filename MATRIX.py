import xlwt
import xlrd

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('邻接矩阵', cell_overwrite_ok=True)

data_excel = xlrd.open_workbook('./InsList.xls')
table = data_excel.sheets()[3]
list = table.col_values(0, start_rowx=1, end_rowx=None)

print(list)
n = 1

if __name__ == '__main__':
    for name in list:
        sheet.write(0, n, name)
        sheet.write(n, 0, name)
        n = n + 1

    print(n)

    for i in range(1, len(list)+1):
        item = table.row_values(i, start_colx=2, end_colx=None)
        for x in range(0, len(list)):
            if list[x] in item:
                sheet.write(i, x + 1, 1)
            else:
                sheet.write(i, x + 1, 0)

book.save('MATRIX.xls')
