#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import *
import os
import datetime
import csv

def getFileInfo():
    cur_time_str = datetime.date.today().strftime("%Y%m%d")
    output_dir_path = '..//doc//upload//' + cur_time_str
    base_date =[2018, 1, 15];
    base_date = datetime.date(base_date[0], base_date[1], base_date[2])
    timegap = datetime.date.today() - base_date
    output_file_list = [i + timegap.days*8 for i in range(1, 9)]
    src_file_path = '..\\doc\\upload\\predict_result_mean.csv'
    output_file_name_base = 'test_result.csv'
    return src_file_path, output_dir_path, output_file_list, output_file_name_base


def genOutputFile(src_file_path, output_dir_path, output_file_list, output_file_name_base, steplength=100):
    if True != os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    file_type = output_file_name_base[output_file_name_base.rindex("."):]
    file_base_name = output_file_name_base[:output_file_name_base.rfind(".")]
    for index in output_file_list:
        src_csv_file = csv.reader(open(src_file_path))
        linenum = 1
        output_file_name = file_base_name + str(index) + file_type
        output_file_path = output_dir_path + '//' + output_file_name
        print('output file : %s' % output_file_path)
        try:
            dst_csv_file = open(output_file_path, 'wt', encoding="UTF8", newline='')
            writer = csv.writer(dst_csv_file, delimiter=",")
            for linecontent in src_csv_file:
                dstcontent = linecontent.copy()
                if linenum != index:
                    writer.writerow(dstcontent)
                else:
                    dstcontent[-1] = str(float(dstcontent[-1]) + steplength)
                    writer.writerow(dstcontent)
                    print('write %s to the %dth line \r\n' % (dstcontent[-1], linenum))
                linenum += 1
        except IOError as err:
            print("IOError in handling %s, error code %d", output_file_path, err.errno)


if __name__ == '__main__':
    '''
    genOutputFile('..\\doc\\upload\\predict_result.csv',
                  '..//doc//upload//20180121',
                  [10, 11, 12, 13, 14, 15, 16, 17],
                  'test_result.csv',
                  100)
    '''

    src_file_path, output_dir_path, output_file_list, output_file_name_base = getFileInfo()
    print("src_file_path", src_file_path)
    print("output_dir_path", output_dir_path)
    print("output_file_list", output_file_list)
    print("output_file_name_base", output_file_name_base)
    genOutputFile(src_file_path, output_dir_path, output_file_list, output_file_name_base, 100)
