from entity_linking_system import EntityLinkingSystem
from tests.evaluation_component import EvaluationComponent

if __name__ == "__main__":
#     text_str = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    EL = EntityLinkingSystem()
    EL.select_ner(0)
    EL.select_ned(0)
    EL.ned_use_ner_class(False)

    #EL.load_dataset("test_datasets/aida_test.json")
    EL.load_dataset("test_datasets/ace2004_test.json")

    EL.text = EL.test.get_text(0)
    #EL.ned()
    EL.test.dataset = [EL.test.dataset[0]]
    EL.ned_tests()
    print(EL.get_accuracy())


    # EL.load_text("siema.json")

#     EL.load_text("text_mj.txt")
# #   EL.load_text_string(text_str)

#     EL.save_html("siem.html")
#     EL.ner()
#     # print(EL.text.get_tagged_text())

    EL.save_html("siem.html")

#     EL.ned()

    #EL.save_html("siem.html")

    #EL.save_text("siema.json")
    pass