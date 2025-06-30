import sys
from custom_logging.log_config import logger

class RAGException(Exception):
    """Base class for all RAG exceptions"""

    def __init__(self,message:str):
        super().__init__(message)

class RAGCustomException(Exception):
    def __init__(self,errormessage,error_details:sys):
        self.errormessage = errormessage

        _,_,exc_tb = error_details.exc_info()

        if exc_tb is not None:
            self.line_no = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.line_no = 'N/A'
            self.file_name = 'N/A'
        logger.error(f"""Error occurred at {self.line_no} inside file {self.file_name} 
            with message: {self.errormessage}""")

    def __str__(self):
        return f"""Error occurred at {self.line_no} inside file {self.file_name} 
            with message: {self.errormessage}
        """


if __name__ == '__main__':
    try:
        a=1/0
    except Exception as e:
        raise RAGCustomException("This is a custom error message", sys)