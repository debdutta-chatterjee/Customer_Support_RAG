import os
from typing import List
from langchain_astradb import AstraDBVectorStore
from utils.config_reader import ConfigReader
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
from exceptions.custom_exception import RAGException


class Retriever:

    def __init__(self):
        load_dotenv()
        config = ConfigReader()

        self.__astradb_api_key = os.getenv('ASTRADB_API_KEY')
        self.__astradb_endpoint = os.getenv('ASTRADB_ENDPOINT')
        self.__astradb_keyspace = config.get_config('astradb')['keyspace']
        self.__astradb_collections = config.get_config('astradb')['collection']
        self.__top_k = config.get_config('retriever')['k']
        self.__embedding_model = ModelLoader().load_embedding_llm()

        self.__vectorstore = None
        self.__retriever = None

    def load_retriever(self):
        """
        Load the retriever
        """
        try:
            if not self.__vectorstore:
                
                self.__vectorstore = AstraDBVectorStore(
                    collection_name=self.__astradb_collections,
                    embedding =self.__embedding_model,
                    api_endpoint = self.__astradb_endpoint,
                    namespace = self.__astradb_keyspace,
                    token =self.__astradb_api_key
                )

            if not self.__retriever:
                self.__retriever = self.__vectorstore.as_retriever(
                    search_kwargs ={'k':self.__top_k})

                return self.__retriever
        except Exception as e:
            raise RAGException(f'Exception occcurred while creating retriever {e}')
        
    def call_retiever(self,query:str) -> List[str]:
        """
        Call the retriever
        """
        try:
            retriever = Retriever().load_retriever()
            output = retriever.invoke(query)
            return output
        except Exception as e :
            raise RAGException(f'Exception occcurred while calling retriever {e}')

if __name__ == '__main__':
    output = Retriever().call_retiever('Suggest the best head phone')
    print(output)
