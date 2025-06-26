import os
from dotenv import load_dotenv
from llm.googleLLM import GoogleLLM
from utils.generic import GenericUtils

class ModelLoader:

    def __init__(self):
        load_dotenv()
        self.__googleLLM = GoogleLLM()

    def load_llm(self):
        """
        Load the chat model
        """
        required_vars = ['GOOGLE_API_KEY']
        GenericUtils().validate_env(required_vars)

        return self.__googleLLM.get_chat_llm()

    def load_embedding_llm(self):
            """
            Load the embedding model
            """
            required_vars = ['GOOGLE_API_KEY']
            GenericUtils().validate_env(required_vars)

            return self.__googleLLM.get_embedding_llm()


if __name__ =='__main__':
     model = ModelLoader().load_llm()
     response = model.invoke('hi')
     print(response)

