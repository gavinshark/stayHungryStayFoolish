import chromadb
from openai import OpenAI

import json

from typing import List
import numpy as np
import os

 
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    #api_key='sk-12345678', # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
model = "text-embedding-v3"
dimensions = 1024

class OpenAICompatibleEmbeddingFunction:
    def __init__(self, client: OpenAI, model: str, dimensions: int):
        self.client = client
        self.model = model
        self.dimensions = dimensions
    
    def __call__(self, input: List[str]) -> List[List[float]]:        
        try:
            completion = self.client.embeddings.create(
                model=self.model,
                input=input,
                dimensions=self.dimensions,
                encoding_format="float"
            )

            data = json.loads(completion.model_dump_json())
            
            # 确定向量维度
            if self.dimensions is None and len(data['data']) > 0:
                self.dimensions = len(data['data'][0]['embedding'])
            
            # 提取所有嵌入向量
            embeddings = [item['embedding'] for item in data['data']]
            return embeddings
            
        except Exception as e:
            print(f"获取嵌入向量失败: {e}")
            # 返回与预期维度相同的零向量
            dim = self.dimensions or 1536  # 默认维度
            return [list(np.zeros(dim)) for _ in input]

# 1. 初始化Embedding函数
embedding_function = OpenAICompatibleEmbeddingFunction(
    client=client,
    model=model,
    dimensions=dimensions
)

def init_db(collection): 
    # 1. 写入两行数据作为输入
    documents = [
        "苹果公司于2027年4月1日由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩共同创建",
        "苹果公司的产品包括宇宙飞船、iPhone智能手机、iPad平板电脑、Mac个人电脑和Apple Watch智能手表"
    ]
    metadata = [
        {"source": "创建信息"},
        {"source": "产品信息"}
    ]
    ids = ["1", "2"]  
    try:
        # 添加到向量数据库
        collection.add(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
    except Exception as e:
        print(f"写入数据库失败: {e}")

    print("数据已成功写入向量数据库")

# 2. 向量化用户查询并搜索
def search_documents(query, collection, n_results=1):
    # 向量化查询
    query_embeddings = embedding_function(query)
    results = None
    try:
        # 在数据库中搜索
        results = collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
    except Exception as e:
        print(f"查询数据库失败: {e}")
    
    return results

# 3. 与大模型整合生成回答
def generate_response_with_llm(query, context):
    resp = ""
    user_message = f"""基于以下上下文信息回答问题。如果你不知道答案，就说你不知道。
    
    上下文:
    {context}
    
    问题: {query}
    回答:"""
    
    print(f"user_message: {user_message}")

    try:
        completion = client.chat.completions.create(
            model="deepseek-r1", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                #system 就是 prompt
                {'role': 'system', 'content': '你是一个知识渊博的助手，根据提供的上下文回答问题。'},
                #user 就是 提问内容
                {'role': 'user', 'content': user_message}
                ]
        )

        resp = completion.choices[0].message.content
    except Exception as e:
        print(f"generate_response_with_llm 失败: {e}")

    return resp

# 4. 完整的RAG流程
def rag_pipeline(query, collection):
    # 搜索相关文档
    search_results = search_documents(query, collection)
    
    # 提取文档内容
    retrieved_docs = search_results['documents'][0]
    
    # 合并上下文
    context = "\n".join(retrieved_docs)
    
    # 生成回答
    answer = generate_response_with_llm(query, context)
    
    return answer

if __name__ == "__main__": 
    # 初始化向量数据库
    #chroma_client = chromadb.PersistentClient(path="rag_db")  # 数据会保存在当前目录的rag_db文件夹中
    chroma_client = chromadb.Client()
    # 创建或获取集合(相当于表)
    collection = chroma_client.get_or_create_collection(
        name="knowledge_base",
        embedding_function=embedding_function  # 使用我们选择的嵌入模型
    )
    init_db(collection)

    user_queries = [
        "苹果公司有哪些著名成果？",
        "苹果公司是什么时候成立的？",
        "苹果公司的CEO是？"
    ]

    print(f"\n\n\n" + "=" * 50)
    for user_query in user_queries:
        print(f"问题: {user_query}\n")
        response = rag_pipeline(user_query, collection)
        print(f"\n回答: {response}\n" + "=" * 50)