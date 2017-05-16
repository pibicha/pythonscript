# -*- coding: utf-8 -*-
"""
解析excel文件，将其中每个sheet页的每行每列，存到运行脚本的目录下
"""
import xlrd
import os
import sys

dirname = os.path.dirname(sys.argv[0])


def read_excel():
    workbook = xlrd.open_workbook(sys.argv[1])
    with open(dirname + 'x.txt', 'w') as f:
        # 遍历每个sheet
        for i in range(len(workbook.sheet_names())):
            sheet = workbook.sheet_by_index(i)
            rows = sheet.nrows
            cols = sheet.ncols
            for j in range(rows):
                for k in range(cols):
                    # print sheet.cell(j,k).value
                    cell = str(sheet.cell(j, k).value)
                    if cell == '' or cell is None:
                        f.write('\t')
                    else:
                        f.write(cell)
                    f.write('\t\t\t')
                # print '\n'
                f.write('\r\n')


if __name__ == '__main__':
    read_excel()
