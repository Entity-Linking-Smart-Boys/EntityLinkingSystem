if __name__ == "__main__":
    pass

import sys

sys.path.append('../.')

from dbp.repository import DBpediaRepository
from data.text import Text
from abc import ABC, abstractmethod


class NEDComponent(ABC):
    """
    Named entity disambiguation component
    """

    # def __init__(self) -> None:
    #     self.dbpedia :DBpediaRepository = DBpediaRepository() 
    #     pass

    @abstractmethod
    def NED(self, taggedText):
        pass
