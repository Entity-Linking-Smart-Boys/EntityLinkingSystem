if __name__ == "__main__":
    pass


import sys
sys.path.append('../.')
from data.text import Text


class FileIO:
    """
    Class for loading and saving texts from/to files 
    """
    def __init__(self) -> None:
        pass
    

    def load(self,textPath) -> Text:
        file = open(textPath)
        text = file.read()
        file.close()
        return Text(text)
    
    def load_string(self,text_str: str) -> Text:
        return Text(text_str)
    
    def load_tagged(self,textPath) -> Text:
        pass
    

    def save_tagged(self,text,path):
        pass
    
    def save_html(self,text,path):
        pass