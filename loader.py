from config import config
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
def data_loader(path):
    loader = TextLoader(path, encoding='utf8')#这里标注编码类型
    texts = loader.load()
    return texts
def get_file_name(path):
    name = path.split('/')[-1].split('.')[0]
    return name   

def text_splitter(texts):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, 
        chunk_overlap=0,
        length_function=len,
        separators=["\n"]
        )
    return text_splitter.split_documents(texts)

def doc_to_vector(documents,file_name):
    model_name = config['model_name']
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs
        )
    #保存向量库路径
    save_path = os.path.join('./bge_vectorstore', file_name)

    faiss_vectorstore = FAISS.from_documents(documents,embed_model,distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
    # 确保目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    faiss_vectorstore.save_local(save_path)
    return faiss_vectorstore

def build_vectorStore(path):
    file_name = get_file_name(path)
    texts = data_loader(path)
    documents = text_splitter(texts)
    return doc_to_vector(documents,file_name)   
def data_processor(file_path,input):
    faiss_vectorstore = build_vectorStore(file_path)
    retriever = faiss_vectorstore.as_retriever(search_type="similarity", search_kwargs={"score_threshold": 0.5, "k": 3})
    related_passages = retriever.invoke(input)
    return related_passages


if __name__ == "__main__":
    file_path = config['file_path'][0] 
    faiss_vectorstore = build_vectorStore(file_path)
    retriever = faiss_vectorstore.as_retriever(search_type="similarity", search_kwargs={"score_threshold": 0.1, "k": 5})
    related_passages = retriever.invoke('疏散楼梯')
    print(related_passages)
            
    