import sys

from ned.ned_component import NEDComponent
from tests.test_text import TestText

sys.path.append('../.')

class TestingComponent:
    def __init__(self) -> None:
        self.dataset : [TestText]
        self.micro_acc = 0
        self.macro_acc = 0

    def load_dataset(self,dataset):
        self.dataset = dataset

    def test_ned(self, NED:NEDComponent):
        for set in self.dataset:
            NED.NED(set)
        self.calculate_micro_and_macro_accuracy()

    def get_ned_micro_accuracy(self):
        return self.micro_acc
    
    def get_ned_macro_accuracy(self):
        return self.macro_acc

    def calculate_micro_and_macro_accuracy(self):
        count = 0
        accurate = 0
        sum = 0
        for set in self.dataset:
            set: TestText
            count += set.get_accurate_count()
            accurate += set.get_entities_count()
            sum += set.get_ned_accuracy()
        self.micro_acc = accurate/count    
        self.macro_acc = sum/len(self.dataset)

    def get_text(self,index:int):
        return self.dataset[index]

#dataset -> new TestClass for entities -> additional field "target_url"?
#2x dataset one with target values, one tested