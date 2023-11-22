import sys
sys.path.append('../.')

from tests.test_entity import TestEntity
from data.text import Text

class TestText(Text):
    def __init__(self, text: str) -> None:
        self.entity_mentions: [TestEntity]
        super().__init__(text)


    def get_accurate_count(self):
        accurate_count = 0
        for entity in self.entity_mentions:
            entity : TestEntity
            if entity.accurate():
                accurate_count += 1
        return accurate_count
        
    def get_entities_count(self):
        return len(self.entity_mentions)
    
    def get_ned_accuracy(self):
        return self.get_accurate_count()/self.get_entities_count()

    # def get_document_f_score(self):
    #     return 2 * self.get_precision() * self.get_recall() / (self.get_recall() + self.get_precision())

    def get_precision(self):
        pass
    def get_recall(self):
        pass