import pandas as pd
import os

class CSVDataLoader:

    def __init__(self, path:str=""):

        if path:
            self.__path = path
        else:
            base_dir = os.path.dirname(__file__)
            self.__path =os.path.abspath(os.path.join(base_dir,'..','data','product_review.csv'))

    def load_product_data(self):
        df = pd.read_csv(self.__path)
        #print(df.columns)
        required_fields = {'product_id', 'product_title', 'rating', 'summary', 'review'}

        if not required_fields.issubset(set(df.columns)):
            raise ValueError(f'Required fields {required_fields} not present in the CSV file')
        
        return df[list(required_fields)]