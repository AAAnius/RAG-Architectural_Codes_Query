config = {
    #文档路径
    'file_path':
    ['./archDataSet/GB50016-2014_ver_2018.txt',
    './archDataSet/GB50096-2011.txt',
     './archDataSet/GB50368-2005.txt'],

     'vectorstore_path':{'高层建筑防火规范':'./vectorStore/GB50016-2014_ver_2018',
                         '居住建筑规范(废除)':'./vectorStore/GB50368-2005',
                         '住宅设计规范':'./vectorStore/GB50096-2011'},

     'model_name':'./bce-embedding-base_v1',
    #  'model_name':'BAAI/bge-large-zh-v1.5',
     }


if __name__ == "__main__":
    print(config['model_name'])
    print(config['file_path'][1])