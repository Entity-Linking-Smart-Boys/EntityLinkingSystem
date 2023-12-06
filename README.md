# Entity Linking System

The Entity Linking System is a project designed to enable users to tag input text using a desktop application. The system incorporates a powerful Entity Recognition (NER) and Entity Disambiguation (NED) mechanism, utilizing the DBpedia Lookup service. This system enhances the understanding of textual data by linking recognized entities to their corresponding entries in the DBpedia knowledge base.

## Requirements
- **Python 3.10:** Download from [the official Python.org website](https://www.python.org/downloads/)

## Installation
```bash
pip install -r .\requirements.txt
python -m spacy download en_core_web_lg
```

## Desktop Application Features
Upon launching the application, users are presented with a single window that encompasses three distinct panels.

### Input Options
- **Input Text:** Users can either manually input text or import text from a *.txt file, providing flexibility for various use cases.

### Configuration Options
**Left Panel:**
- This panel hosts various components for input and configuration.
  - **Textbox and "Load Text" Button:** The top section enables users to input or paste text directly into the application. Clicking "Load Text" loads the entered text into the middle panel.
  - **"Load File" Button:** Users can search for and load text from a file directly into the application.
  - **NER and NED Algorithm Selection:** Users can choose from available Named Entity Recognition (NER) and Entity Disambiguation (NED) algorithms. Checkboxes allow users to decide whether to use NER or not during the process.
    - **NER Type Selection:** Users can choose the Named Entity Recognition (NER) type, tailoring the system to recognize specific entities such as persons, organizations, or locations.
    - **NED Type Selection:** Users can specify the Entity Disambiguation (NED) type, refining the process of linking recognized entities to their corresponding entries in the DBpedia knowledge base.
    - **Use NER Types during NED:** Users have the option to leverage NER types during the NED process, enhancing the accuracy of entity linking.

  - **"Start" Button:** Initiates the selected algorithms and outputs the tagged text into the middle panel.

    
### Entity Linking Process
- **Run Entity Linking:** Initiates the Entity Linking process, where the system analyzes the input text to identify entities and link them to relevant DBpedia entries.
- **Processing Time:** The duration of the Entity Linking process depends on the length of the text. Longer texts may require several minutes for comprehensive analysis.

### Results Display
- **Middle Panel:** The linked entities are displayed in this panel after the Entity Linking process. Each entity is associated with a hyperlink.
- **Right Panel:** Clicking on a recognized and linked entity's hyperlink opens the corresponding DBpedia webpage, providing additional information about the entity.

## Usage
1. Launch the application.
2. Input or import text.
3. Configure NER and NED options.
4. Run the Entity Linking process.
5. View results in the middle panel.
6. Click on hyperlinks for detailed information in the right panel.

Enhance your text analysis and knowledge extraction with the Entity Linking System!



