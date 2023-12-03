import unittest

from entity_linking_system import EntityLinkingSystem


class TestNEDSelect(unittest.TestCase):

    def setUp(self):
        self.EL = EntityLinkingSystem()
        self.use_NER_class = False

    def test_select_ned_Lookup(self):
        ned_id = 0
        self.EL.select_ned(ned_id, self.use_NER_class)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Lookup")

    def test_select_ned_Graph(self):
        ned_id = 1
        self.EL.select_ned(ned_id, self.use_NER_class)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Graph")

    def test_select_ned_Math(self):
        ned_id = 2
        self.EL.select_ned(ned_id, self.use_NER_class)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Math")


class TestNEDRunUsingNERClass(unittest.TestCase):

    def setUp(self):
        self.EL = EntityLinkingSystem()
        self.test_text = "test_text.txt"
        self.use_NER_class = True

    def test_run_ned_Lookup(self):
        ner_id = 0  # Spacy
        ned_id = 0  # Lookup
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Graph(self):
        ner_id = 0  # Spacy
        ned_id = 1  # Graph
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Math(self):
        ner_id = 0  # Spacy
        ned_id = 2  # Math
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")


class TestNEDRunWithoutUsingNERClass(unittest.TestCase):

    def setUp(self):
        self.EL = EntityLinkingSystem()
        self.test_text = "test_text.txt"
        self.use_NER_class = False

    def test_run_ned_Lookup(self):
        ner_id = 0  # Spacy
        ned_id = 0  # Lookup
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Graph(self):
        ner_id = 0  # Spacy
        ned_id = 1  # Graph
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Math(self):
        ner_id = 0  # Spacy
        ned_id = 2  # Math
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id, self.use_NER_class)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")


if __name__ == '__main__':
    unittest.main()
