from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.config_reader import ConfigReader
import os
from exceptions.custom_exception import RAGException

class GoogleLLM:
    
    def __init__(self):
        self.__config = ConfigReader()
        load_dotenv()

    def get_chat_llm(self):
        try:
            return ChatGoogleGenerativeAI(
                model = self.__config.get_config("llm")["model_name"],
                temparature = self.__config.get_config("llm")["temparature"],
                max_tokens = self.__config.get_config("llm")["max_tokens"],
                api_key = os.environ['GOOGLE_API_KEY']
            )
        except Exception as e:
            raise RAGException(f"Exception occurred while loading LLM {e}")

    def get_embedding_llm(self):
        try:
            return GoogleGenerativeAIEmbeddings(
                model = self.__config.get_config("embedding-model")["model_name"],
                api_key = os.environ['GOOGLE_API_KEY']
            )
        except Exception as e:
            raise RAGException(f"Exception occurred while loading embedding LLM {e}")