from retriever.retriever import Retriever
from utils.model_loader import ModelLoader
from exceptions.custom_exception import RAGException
from langchain.prompts import ChatPromptTemplate
from prompt_library.prompt import PROMPT_TEMPATE
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class GenerateResponse:

    def __init__(self):
        self.__retriever = Retriever()
        self.__model = ModelLoader().load_llm()

    def generate_response(self,query):
        """
        Generate response from llm based on retrieved context
        """

        try:
            retriever = Retriever().load_retriever()
            prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPATE['product_bot'])

            chain = (
                {'context':retriever, 'question':RunnablePassthrough()}|
                prompt | 
                self.__model | 
                StrOutputParser()
            ) 

            response = chain.invoke(query)
            return response

        except Exception as e:
            raise RAGException(f'Exception occcurred while generating llm response {e}')
        
if __name__ == '__main__':
    query = 'Suggest the best head phone'
    response = GenerateResponse().generate_response(query)
    print(response)