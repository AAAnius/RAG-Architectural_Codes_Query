'''
根据已有得向量数据库进行查询
'''
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import config
from loader import build_vectorStore
from call_larg_model import call_zhipuai

def build_embedding_model():
    model_name = config['model_name']
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embed_model
def get_name_list():
    paths = config['vectorstore_path']
    name_list =[]
    for name,path in paths.items():
        name_list.append(name)
    return name_list
def get_sentence_similarity(query,sentence_list,):
        max_score = 0
        doc_name = ''
        for sentence in sentence_list:
            char1  = set(query)
            char2  = set(sentence)
            score = len(char1.intersection(char2))/len(char1.union(char2))
            if score > max_score:
                max_score = score
                doc_name = sentence
        if max_score == 0:
            print('查询不到相关内容')
        else:
            print(doc_name)
            return doc_name
        

def choose_vetor_path(input):
    name_list = get_name_list()
    vectorstore_path = ''
    return vectorstore_path

def local_query():
    name_list = get_name_list()
    user_input = input('请输入查询的规范名称或关键字：')
    doc_name = get_sentence_similarity(user_input,name_list)
    print('查询到相关规范：',doc_name)
    vectorstore_path = config['vectorstore_path'][doc_name]
    print(vectorstore_path)
    embed_model = build_embedding_model()
    #输入向量库，输入嵌入模型，允许反序列化
    faiss_vectorstore = FAISS.load_local(vectorstore_path, embed_model,allow_dangerous_deserialization=True)

    query = input('请输入查询的内容或关键字：')
    prompt = faiss_vectorstore.similarity_search_with_score(query,k = 5)
    res = call_zhipuai(query,prompt)
    return res
def gradio_query(input):
    vectorstore_path = config['vectorstore_path']['建筑设计防火规范']
    embed_model = build_embedding_model()
    #输入向量库，输入嵌入模型，允许反序列化
    faiss_vectorstore = FAISS.load_local(vectorstore_path, embed_model,allow_dangerous_deserialization=True)
    query = input
    prompt = faiss_vectorstore.similarity_search_with_score(query,k = 5)
    res = call_zhipuai(query,prompt)
    return res


if __name__ == "__main__":
    res = local_query()
    print(res)
    
    

    print('=======Done========')