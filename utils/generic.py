import os
from typing import List

class GenericUtils:

    def __init__(self):
        pass

    def validate_env(self,required_var:List[str]):
        """"
        Validate if all required variables are set in the environment
        """

        missing_vars = [var for var in required_var if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError('Missing environment variables'+ ' '.join(missing_vars))
        else:
            return True