#!/usr/bin/env python
#-*-coding:utf-8-*-

def write_txt(list):
    file = open('answer.txt', 'w')
    for i in range(len(list)):
        s = str(list[i]).replace('[', '(').replace(']', ')') + '\n'  # 去除[],这两行按数据不同，可以选择
        #s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

all_path = [[1,2,3,4],[1,2,3,5]]
write_txt(all_path)