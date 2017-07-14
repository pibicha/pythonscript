# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

"""
不使用循环控制变量合并两个行数相同的文件；
"""


def merge(file1, file2):
    gfile = generate_file(file2)
    with open(r'merge_file.txt', 'w') as wf:
        with open(file1) as f:
            for line in f:
                wf.write(line.strip() + ':' + gfile.next().strip() + "\n")


def generate_file(file):
    with open(file) as f:
        for line in f:
            yield line


if __name__ == '__main__':
    merge(sys.argv[1], sys.argv[2])
