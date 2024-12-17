'''
根据新文档建立数据库,并进行查询
'''
from loader import data_processor
from config import config 
from call_larg_model import call_zhipuai





if __name__ == "__main__":
    path = config['file_path'][0]
    user_input = input('请输入查询的规范内容：')
    prompt = data_processor(path,user_input)
    call_zhipuai(user_input,prompt)