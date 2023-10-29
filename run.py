from entity_linking_system import EntityLinkingSystem


if __name__ == "__main__":
    text_str = "Nikola Tesla (Serbian Cyrillic: Никола Тесла) was a Serbian-American inventor, electrical engineer, mechanical engineer, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system."

    EL = EntityLinkingSystem()
    EL.select_ner(0)
    EL.select_ned(0)

#    EL.load_text("siema.json")
    EL.load_text("text1.txt")
#   EL.load_text_string(text_str)

    EL.save_html("siem.html")
    EL.ner()
    # print(EL.text.get_tagged_text())

    EL.save_html("siem.html")

    #EL.ned()
    #EL.save_html("siem.html")
    
    #EL.save_text("siema.json")
    pass
