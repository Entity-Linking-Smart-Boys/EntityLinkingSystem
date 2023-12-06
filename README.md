
<!-- TOC --><a name="entity-linking-system"></a>
# Entity Linking System

The Entity Linking System is a project designed to enable users to tag input text using a desktop application. The system incorporates a powerful Entity Recognition (NER) and Entity Disambiguation (NED) mechanism, utilizing the DBpedia Lookup service. This system enhances the understanding of textual data by linking recognized entities to their corresponding entries in the DBpedia knowledge base.

<!-- TOC --><a name="requirements"></a>

## Table of contents:
- [Entity Linking System](#entity-linking-system)
   * [Requirements](#requirements)
   * [Installation](#installation)
   * [Named Entity Recognition](#named-entity-recognition)
      + [NER using spaCy](#ner-using-spacy)
      + [NER using BERT model](#ner-using-bert-model)
   * [Named Entity Disambiguation](#named-entity-disambiguation)
      + [Algorithm Structure](#algorithm-structure)
      + [Developed EL Algorithms](#developed-el-algorithms)
   * [Desktop Application Features](#desktop-application-features)
      + [Input Options](#input-options)
      + [Configuration Options](#configuration-options)
      + [Entity Linking Process](#entity-linking-process)
      + [Results Display](#results-display)
   * [Usage](#usage)


## Requirements
- **Python 3.10:** Download from [the official Python.org website](https://www.python.org/downloads/)

<!-- TOC --><a name="installation"></a>
## Installation
```bash
pip install -r .\requirements.txt
python -m spacy download en_core_web_lg  # needed for NER using spaCy
```

<!-- TOC --><a name="named-entity-recognition"></a>
## Named Entity Recognition
In our work we focused on two NER approaches presented in this section.

<!-- TOC --><a name="ner-using-spacy"></a>
### NER using spaCy

**spaCy**, recognized as the swiftest NLP framework in Python, stands out for its efficiency in implementing individualized functions for each NLP task. Its user-friendly nature allows for the seamless execution of straightforward tasks with just a few lines of code.

Read more at the official spaCy website: [Named Entity Recognition (NER) using spaCy ](https://spacy.io/universe/project/video-spacys-ner-model-alt)

<!-- TOC --><a name="ner-using-bert-model"></a>
### NER using BERT model

In our work, we focus on the **BERT model**, a Transformer-based architecture, leveraging its unique features:

- **Parallel Input Processing:**
  - Drastically speeds up model training time.
  - Particularly beneficial for batch training.
  - Allows efficient usage of hardware units like GPUs and TPUs.

- **Input Embedding Layer:**
  - Converts input tokens into continuous vector representations.
  - Vectors learned during training and stored in an embedding matrix.
  - Enables mathematical operations on vector representations, simulating language understanding.

- **Positional Encoding Layer:**
  - Addresses the importance of token positioning within a sentence.
  - Typically generated using sinusoidal functions.
  - Combined representation captures semantic meaning and position in the sequence.

- **Multi-Head Attention Layer:**
  - Key feature of the Transformer architecture.
  - Allows the model to focus on different aspects of the input simultaneously.
  - Improves the ability to capture both local and global dependencies.

- **Feed Forward Layer:**
  - Essential component of the Transformer architecture.
  - Contributes to the model's ability to process and understand input data effectively.

<!-- TOC --><a name="named-entity-disambiguation"></a>
## Named Entity Disambiguation

Three robust Entity Linking (EL) algorithms have been meticulously crafted by amalgamating the previously outlined candidate disambiguation approaches. The primary goal of each algorithm is to assign scores to candidates, taking into account both contextual information and other pertinent aspects related to the recognized named entity and the candidate.

<!-- TOC --><a name="algorithm-structure"></a>
### Algorithm Structure

1. **Partial Scores:** Candidates within each algorithm are subject to receiving partial scores from each disambiguation approach. These partial scores collectively contribute to the final score of the candidate.

2. **Equal Weightage:** All disambiguation approaches within a given algorithm carry equal weight, ensuring a balanced influence on the final candidate score.

3. **Normalization:** To maintain consistency and fairness, a normalization process is applied to each partial score. This mapping transforms each score into a value within the range of 0 to 1. The candidate with the highest score attains a normalized partial score of 1, while the lowest-scoring candidate receives a normalized partial score of 0. This normalization procedure guarantees that each disambiguation approach contributes proportionally to the final candidate score, facilitating a just and standardized evaluation.

4. **Final Scores:** The resultant final scores, ranging between 0 and 1, facilitate a straightforward ranking. Candidates closer to 1 are prioritized as more suitable disambiguation outcomes.

5. **Sorting:** The concluding step involves sorting candidates in descending order based on their final total score, which is the sum of all partial scores for that candidate. The candidate holding the highest score in the sorted list is identified as the best candidate according to the algorithm.

<!-- TOC --><a name="developed-el-algorithms"></a>
### Developed EL Algorithms

1. **NED Lookup-Context-Levenshtein:**
   - **Components:**
     - DBpedia Lookup Score
     - Context Similarity
     - Levenshtein Distance Calculation
   - **Objective:** This algorithm combines the DBpedia Lookup Score with additional layers of context-based similarity and Levenshtein Distance calculation. The synergy of these components enhances the precision and relevance of the entity linking process.

2. **NED Lookup-Connectivity-Popularity:**
   - **Components:**
     - DBpedia Lookup Score
     - Connectivity Analysis
     - Popularity of Candidates
   - **Objective:** In this algorithm, the DBpedia Lookup Score is complemented by insights from connectivity analysis and the overall popularity of candidates. This multi-faceted approach aims to provide a comprehensive evaluation of candidate entities.

3. **NED Lookup:**
   - **Components:**
     - DBpedia Lookup Score
   - **Objective:** Focused on simplicity and efficiency, this algorithm relies solely on the DBpedia Lookup Score. It provides a streamlined approach for users seeking a straightforward and effective entity linking solution.

These EL algorithms offer users flexibility in choosing the approach that aligns with their specific requirements and preferences. Whether prioritizing contextual similarity, connectivity, or simplicity, these algorithms cater to diverse needs in the entity linking process.

<!-- TOC --><a name="desktop-application-features"></a>
## Desktop Application Features
Upon launching the application, users are presented with a single window that encompasses three distinct panels.

<!-- TOC --><a name="input-options"></a>
### Input Options
- **Input Text:** Users can either manually input text or import text from a *.txt file, providing flexibility for various use cases.

<!-- TOC --><a name="configuration-options"></a>
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

    
<!-- TOC --><a name="entity-linking-process"></a>
### Entity Linking Process
- **Run Entity Linking:** Initiates the Entity Linking process, where the system analyzes the input text to identify entities and link them to relevant DBpedia entries.
- **Processing Time:** The duration of the Entity Linking process depends on the length of the text. Longer texts may require several minutes for comprehensive analysis.

<!-- TOC --><a name="results-display"></a>
### Results Display
- **Middle Panel:** The linked entities are displayed in this panel after the Entity Linking process. Each entity is associated with a hyperlink.
- **Right Panel:** Clicking on a recognized and linked entity's hyperlink opens the corresponding DBpedia webpage, providing additional information about the entity.

<!-- TOC --><a name="usage"></a>
## Usage
1. Launch the application.
2. Input or import text.
3. Configure NER and NED options.
4. Run the Entity Linking process.
5. View results in the middle panel.
6. Click on hyperlinks for detailed information in the right panel.

Enhance your text analysis and knowledge extraction with the Entity Linking System!



