from typing import List
from langchain_core.documents import Document
from exceptions.custom_exception import RAGException
from utils.load_csv_data import CSVDataLoader
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os
from utils.config_reader import ConfigReader
from utils.model_loader import ModelLoader

class DataIngestion:

    def __init__(self):
        self.__dataLoader = CSVDataLoader()
        load_dotenv()
        config = ConfigReader()

        self.__astradb_api_key = os.getenv('ASTRADB_API_KEY')
        self.__astradb_endpoint = os.getenv('ASTRADB_ENDPOINT')
        self.__astradb_keyspace = config.get_config('astradb')['keyspace']
        self.__astradb_collections = config.get_config('astradb')['collection']

        self.__embedding_model = ModelLoader().load_embedding_llm()

    def transform_data(self,df):
        """
        Transform the product dataframe  into langchain document format
        """

        try:
            documents = []

            for _,row in df.iterrows():
                doc = Document(
                    page_content=row['review'],
                    metadata = {
                        'product_id':row['product_id'],
                        'product_title':row['product_title'],
                        'rating':row['rating'],
                        'summary':row['summary']
                    }
                )
                
                documents.append(doc)
        except Exception as e:
            raise RAGException(f"Error occurred while transforming document {e}")
        
        return documents
    
    def store_data_in_vector_db(self,documents: List[Document]):
        """
        Store the documents in the vector db
        """

        try:
            vector_store = AstraDBVectorStore(
                collection_name=self.__astradb_collections,
                embedding =self.__embedding_model,
                api_endpoint = self.__astradb_endpoint,
                namespace = self.__astradb_keyspace,
                token =self.__astradb_api_key
            )

            inserted_ids = vector_store.add_documents(documents)
            print(f'Inserted {len(inserted_ids)} into vector store')

        except Exception as e:
            raise RAGException(f'Exception occcurred while storing data in vector db {e}')


        return vector_store,inserted_ids

    def run_pipeline(self):
        """
        Run the pipeline to transform & ingest the data
        """

        try:
            df = self.__dataLoader.load_product_data()
            documents = self.transform_data(df)
            self.store_data_in_vector_db(documents)
        except Exception as e:
            raise RAGException(f'Error occurred while running ingestion {e}')
        return documents

if __name__ =='__main__':
    data_ingestion = DataIngestion()
    documents = data_ingestion.run_pipeline()
    print(len(documents))
    print(documents[0])