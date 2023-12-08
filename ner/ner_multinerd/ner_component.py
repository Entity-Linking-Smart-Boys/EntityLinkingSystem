if __name__ == "__main__":
    pass

import sys
sys.path.append('../.')

from data.text import Text
from abc import ABC, abstractmethod

class NERComponent(ABC):
    """
    Named entity recognition component
    """
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def NER(self, text: Text) -> Text:
        pass
    
    @abstractmethod
    def _map_ner_class_to_dbp():
        """
        Ommitable, It is possible for NER to only tag entities without classifing them.
        """
        pass