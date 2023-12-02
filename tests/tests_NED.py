import unittest

from entity_linking_system import EntityLinkingSystem


class TestNEDSelect(unittest.TestCase):

    def setUp(self):
        self.EL = EntityLinkingSystem()

    def test_select_ned_Lookup(self):
        ned_id = 0
        self.EL.select_ned(ned_id)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Lookup")

    def test_select_ned_Graph(self):
        ned_id = 1
        self.EL.select_ned(ned_id)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Graph")

    def test_select_ned_Math(self):
        ned_id = 2
        self.EL.select_ned(ned_id)
        selected_ned = self.EL.NED.candidateType
        self.assertEqual(selected_ned, "Math")


class TestNEDRun(unittest.TestCase):

    def setUp(self):
        self.EL = EntityLinkingSystem()
        self.test_text = "test_text.txt"

    def test_run_ned_Lookup(self):
        ner_id = 0  # Spacy
        ned_id = 0  # Lookup
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Graph(self):
        ner_id = 0  # Spacy
        ned_id = 1  # Graph
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")

    def test_run_ned_Math(self):
        ner_id = 0  # Spacy
        ned_id = 2  # Math
        self.EL.select_ner(ner_id)
        self.EL.select_ned(ned_id)

        self.EL.load_text(self.test_text)

        self.EL.ner()

        self.EL.ned()

        self.EL.save_html("test_text_saved.html")


if __name__ == '__main__':
    unittest.main()
