# -*- coding: utf-8 -*-
import xlrd
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
dirname = os.environ.get(__name__)


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(sys.argv[1])

    with open(result_file, 'w') as f:
        # 遍历每个sheet
        for i in range(len(workbook.sheet_names())):
            sheet = workbook.sheet_by_index(i)
            rows = sheet.nrows
            cols = sheet.ncols
            for j in range(rows):
                if j in range(start_row): continue
                for k in range(cols):
                    if k in range(start_col): continue
                    cell = str(sheet.cell(j, k).value)
                    if cell == '' or cell is None:
                        f.write('NULL:')

                    else:
                        f.write(cell + ':')

                # print '\n'
                f.write('\r\n')


if __name__ == '__main__':
    try:
        result_file = sys.argv[1].split('.')[0] + '.txt'
    except Exception:
        print "缺失文件参数"
        exit(-1)
    start_row = input("which row from parse:")
    start_col = input("which col from parse:")
    read_excel()
    os_path = os.getcwd()
    print "parse completed ,result save in %s%s" % (os_path, result_file)
