import os
import configparser
import glob
from PyPDF2 import  PdfFileReader, PdfFileWriter

in_dir = './input/'
out_dir = './output/'

cfg = configparser.ConfigParser()
cfg.read('config.txt', encoding='utf-8')

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# print(cfg['pdf_split']['page_ranges'])
page_ranges_str = cfg['pdf_split']['page_ranges']
page_ranges = page_ranges_str.split(';')

for pdf_path in glob.glob(os.path.join(in_dir, '*.pdf')):
    print('Open' + pdf_path)
    pdf_name = os.path.basename(pdf_path).split('.')[0]
    file_reader = PdfFileReader(pdf_path)
    numPages = file_reader.getNumPages()

    for pg_range in page_ranges:
        if pg_range == '':
            continue
        # 实例化对象
        file_writer = PdfFileWriter()
        start_end = pg_range.split(',')
        start = int(start_end[0])
        end = int(start_end[1])
        start = start if start > 1 else 1
        end = end if end < numPages else numPages
        print('split {}-{} pages'.format(start, end))
        for page in range(start-1, end):    #cfg序号从1开始，左右都是闭区间
            # 将遍历的每一页添加到实例化对象中
            file_writer.addPage(file_reader.getPage(page))
        with open(os.path.join(out_dir, pdf_name)+"{}-{}.pdf".format(start,end),'wb') as out:
            # 若报解码错误，可尝试在源码中加入"latin-1"
            file_writer.write(out)

os.system('pause')