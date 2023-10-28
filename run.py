from entity_linking_system import EntityLinkingSystem


if __name__ == "__main__":
    text_str = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    EL = EntityLinkingSystem()
    EL.load_text_string(text_str)
    EL.select_ner(0)
    EL.select_ned(0)
    
    EL.ner()
    print(EL.text.get_tagged_text())
    EL.ned()
    pass
