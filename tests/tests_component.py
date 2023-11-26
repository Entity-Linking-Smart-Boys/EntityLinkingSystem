import sys

from ned.ned_component import NEDComponent

sys.path.append('../.')
from data.text import TestText

class TestingComponent:
    def __init__(self) -> None:
        self.dataset : [TestText]
        self.micro_acc = 0
        self.macro_acc = 0

    def load_dataset(self,dataset):
        """Load dataset to component"""
        self.dataset = dataset

    def test_ned(self, NED:NEDComponent):
        """Run ned tests and calculate accuracies"""
        for set in self.dataset:
            NED.NED(set)
        self.calculate_micro_and_macro_accuracy()

    def get_ned_micro_accuracy(self):
        """Get micro accuracy for latest test \n
        calculated per whole corpus
        """
        return self.micro_acc
    
    def get_ned_macro_accuracy(self):
        """Get macro accuracy for latest test, \n
        average for document
        """
        return self.macro_acc

    def calculate_micro_and_macro_accuracy(self):
        """Calculate accuracies for latest test"""
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

    def get_text(self,index:int) -> TestText:
        """Get text from loaded dataset"""
        return self.dataset[index]
    
    def get_dataset_length(self):
        """Get length of loaded dataset"""
        return len(self.dataset)

#dataset -> new TestClass for entities -> additional field "target_url"?
#2x dataset one with target values, one tested