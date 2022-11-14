import os
import glob
import re
import configparser
import pdfplumber as pp

cfg = configparser.ConfigParser()
cfg.read('config.txt', encoding='utf-8')

in_dir = './input/'
str_pattern = '\S+'
num_pattern = '\d+'
# key_patterns = {'借款人（乙方）':str_pattern, '收件人':str_pattern, '手机号码':num_pattern}
# separator = r'[:：]'
# end_str = r'[\s]'

key_words_str = cfg['pdf_extract']['key_words_str'].split(';')
key_words_num = cfg['pdf_extract']['key_words_num'].split(';')
end_str = '['+cfg['pdf_extract']['end']+']'
separator = '['+cfg['pdf_extract']['separator']+']'

file_rst_list = []
for pdf_path in glob.glob(os.path.join(in_dir, '*.pdf')):
    with pp.open(pdf_path) as pdf:
        print('Open ', pdf_path)
        rst_dict = dict()
        for key in key_words_str:
            rst_dict[key] = list()
        for key in key_words_num:
            rst_dict[key] = list()
        
        for page in pdf.pages:
            text = page.extract_text()
            # for key, _pattern in key_patterns.items():

            
            for key in key_words_str:
                # print(key, _pattern)
                pattern = '('+key+')'+separator+'('+str_pattern+')'+end_str
                rst_list = re.findall(pattern, text)
                for rst in rst_list:
                    if rst is not None:
                        print(rst)
                        rst_dict[key].append(rst[1])

            for key in key_words_num:
                pattern = '('+key+')'+separator+'('+num_pattern+')'+end_str
                rst_list = re.findall(pattern, text)
                for rst in rst_list:
                    if rst is not None:
                        print(rst)
                        rst_dict[key].append(rst[1])

        file_rst_list.append(rst_dict)

fd = open('./rst.txt','w')
for file_rst in file_rst_list:
    for key, values in file_rst.items():
        for v in values:
            fd.write(v+'\t')
    fd.write('\n')
fd.close()

os.system('pause')