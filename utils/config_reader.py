import yaml
import os

class ConfigReader:
    
    def __init__(self, path:str=""):

        if path:
            self.__path = path
        else:
            base_dir = os.path.dirname(__file__)
            self.__path =os.path.abspath(os.path.join(base_dir,'..','config','config.yaml'))
    
    def load_config(self) -> dict:
        """
        Reads the config yaml file & returns the value
        """
        with open(self.__path,'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def get_config(self,key:str):
        """
        Returns the value of a given key in the yaml file
        """
        config = self.load_config()
        if key in config:
            return config[key]
        else:
            raise KeyError(f"Key {key} not found in config file.")
        

if __name__  == "__main__":
    config = ConfigReader()
    value = config.get_config("astradb")
    print(value)
    value = config.load_config()
    print(value)