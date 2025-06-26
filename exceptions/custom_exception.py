class RAGException(Exception):
    """Base class for all RAG exceptions"""

    def __init__(self,message:str):
        super().__init__(message)
