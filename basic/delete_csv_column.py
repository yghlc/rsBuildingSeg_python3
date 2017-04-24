#!/usr/bin/env python
# Filename: delete_csv_column 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 24 April, 2017
"""

from optparse import OptionParser
import basic, io_function

import csv

def delete_fouth_coloumn_csv(csv_path):

    with open(csv_path, 'rb') as f:
        reader = csv.reader(f)
        input_list = map(tuple, reader)
        f.close()

    save_csv=open('test.csv','wb')
    csv_writer = csv.writer(save_csv)

    for line in input_list:
        save_ele = line[0:3]
        csv_writer.writerows([save_ele])

    save_csv.close()

    return True



def main(options, args):

    # path = args[0]
    path = 'result_buildings.csv'
    delete_fouth_coloumn_csv(path)

    pass




if __name__=='__main__':
    usage = "usage: %prog [options] csv_file "
    parser = OptionParser(usage=usage, version="1.0 2017-4-24")

    (options, args) = parser.parse_args()

    main(options, args)