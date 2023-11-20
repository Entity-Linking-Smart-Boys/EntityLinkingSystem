if __name__ == "__main__":
    pass

import json
import jsonpickle
from pathlib import Path
from htmldom import htmldom

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
        file = open(textPath, encoding="utf-8")
        text = file.read()
        file.close()
        return Text(text)
    
    def load_string(self,text_str: str) -> Text:
        return Text(text_str)
    
    def load_tagged(self,textPath) -> Text:
        file = open(textPath, encoding="utf-8")
        json_file = file.read()
        file.close()
        text =  jsonpickle.decode(json.loads(json_file))[0]
        return text
    
    

    def save_tagged(self, text: Text, path):
        json_text = json.dumps(jsonpickle.encode(text))
        file = open(path,mode = "w",encoding="utf-8")
        file.write(json_text)
        file.close()
        return
    
    def save_html(self, text: Text, path):
        tfile = open(f"{Path( __file__ ).parent.absolute()}/template.xhtml", mode= "r" , encoding="utf-8")
        template = tfile.read()
        tfile.close()
        
        dom = htmldom.HtmlDom().createDom(template)
        dom.find("div[id=content]").text(text.get_html_text())

        file = open(path,mode = "w",encoding="utf-8")
        file.write("<!DOCTYPE html>"+dom.referenceToRootElement.html())
        file.close()