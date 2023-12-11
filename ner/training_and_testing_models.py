import datasets
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizerFast
from transformers import DataCollatorForTokenClassification
from transformers import AutoModelForTokenClassification
from transformers import AutoTokenizer
from transformers import pipeline
from transformers import TrainingArguments, Trainer
import json
import os


class Entity(object):

    def __init__(self):
        self.surface_form: str
        self.ner_class: str
        self.position: (int, int)
        self.uri: str
        self.dbpedia_class: str
        self.candidates: []

    def __init__(self, surface_form: str, ner_class: str, position: (int, int)) -> None:
        self.surface_form: str = surface_form
        self.ner_class: str = ner_class
        self.position: (int, int) = position
        self.uri: str = ""
        self.dbpedia_class: str = " "
        self.candidates: []





def check_cuda():
    # time.sleep(5)
    # print("Tensorflow's num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    print("Is CUDA available:" + str(torch.cuda.is_available()))
    print(f"Is CUDA supported by this system? {torch.cuda.is_available()}")
    print(f"CUDA version: {torch.version.cuda}")
    # Storing ID of current CUDA device
    cuda_id = torch.cuda.current_device()
    print(f"ID of current CUDA device:{torch.cuda.current_device()}")
    print(f"Name of current CUDA device:{torch.cuda.get_device_name(cuda_id)}")


def tokenize_and_align_labels(examples):
    """
    function responsible for proper labeling since tokenizer returns more tokens than initial words

    examples - dictionary containing
            "tokens" : list of tokens within a sentence
            "ner_tags" : list of corresponding labels for each token
    """
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
    # for i, label in enumerate(examples["tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        # Special tokens are mapped by default to None, we change it to -100
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(label[word_idx])
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs


def compute_metrics(eval_preds):

    metric = datasets.load_metric("seqeval")
    label_list = list(ner_dict.keys())
    pred_logits, labels = eval_preds
    pred_logits = np.argmax(pred_logits, axis=2)

    # We remove all the values where the label is -100
    predictions = [
        [label_list[eval_preds] for (eval_preds, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(pred_logits, labels)
    ]

    true_labels = [
        [label_list[l] for (eval_preds, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(pred_logits, labels)
    ]
    results = metric.compute(predictions=predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


def load_and_tokenize_conll():
    conll2003 = datasets.load_dataset("conll2003")
    tokenized_train = conll2003['train'].map(tokenize_and_align_labels, batched=True)
    tokenized_validation = conll2003['validation'].map(tokenize_and_align_labels, batched=True)
    tokenized_test = conll2003['test'].map(tokenize_and_align_labels, batched=True)
    return tokenized_train, tokenized_validation, tokenized_test


def load_and_save_multinerd():
    """
    function responsible for downloading multinerd dataset and splitting it into three subsets
    """
    multinerd = datasets.load_dataset("tner/multinerd", "en")
    # split dataset into three subsets
    train_data, temp = train_test_split(multinerd['test'], train_size=0.7, random_state=42)
    temp_data = datasets.Dataset.from_dict(temp)
    validation_data, test_data = train_test_split(temp_data, train_size=0.5, random_state=42)

    # Convert datasets back to Dataset object
    train_set = datasets.Dataset.from_dict(train_data)
    validation_set = datasets.Dataset.from_dict(validation_data)
    test_set = datasets.Dataset.from_dict(test_data)

    destination_directory_train = './datasets/multinerd2/train'
    destination_directory_validation = './datasets/multinerd2/validation'
    destination_directory_test = './datasets/multinerd2/test'

    os.makedirs(destination_directory_train, exist_ok=True)
    os.makedirs(destination_directory_validation, exist_ok=True)
    os.makedirs(destination_directory_test, exist_ok=True)

    train_set.save_to_disk(destination_directory_train)
    validation_set.save_to_disk(destination_directory_validation)
    test_set.save_to_disk(destination_directory_test)


def get_tokenized_multinerd():
    """
    function resposible for loading datasets from disc and tokenizing them
    :return: tokenized datasets
    """
    train_set = datasets.load_from_disk('./datasets/multinerd/train')
    validation_set = datasets.load_from_disk('./datasets/multinerd/validation')
    test_set = datasets.load_from_disk('./datasets/multinerd/test')

    tokenized_train = train_set.map(tokenize_and_align_labels, batched=True)
    tokenized_validation = validation_set.map(tokenize_and_align_labels, batched=True)
    tokenized_test = test_set.map(tokenize_and_align_labels, batched=True)

    return tokenized_train, tokenized_validation, tokenized_test


def run_training(tokenized_train, tokenized_validation, train_epochs, run_name):

    # model = AutoModelForTokenClassification.from_pretrained("bert-base-uncased", num_labels=35)
    # model = AutoModelForTokenClassification.from_pretrained("distilbertnerd_model")
    model = AutoModelForTokenClassification.from_pretrained("distilbert-base-cased", num_labels=9)
    data_collator = DataCollatorForTokenClassification(tokenizer)

    args = TrainingArguments(
        run_name + "_training",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=train_epochs,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model,
        args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_validation,
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()

    model.save_pretrained(run_name + "_model")
    tokenizer.save_pretrained(run_name + "_tokenizer")


def use_conll_model(input_sentence):

    config = json.load(open("ner_model/config.json"))
    config["label2id"] = {key: str(value) for key, value in ner_dict2.items()}
    config["id2label"] = {value: key for key, value in config["label2id"].items()}
    json.dump(config, open("ner_model/config.json", "w"))

    model_fine_tuned = AutoModelForTokenClassification.from_pretrained("ner_model")
    nlp = pipeline("ner", model=model_fine_tuned, tokenizer=tokenizer)
    ner_results = nlp(input_sentence)
    # print("\n################   USING CONLL MODEL   ########################")
    #     # print("\nGiven example sentence:\n" + input_sentence + "\n")
    #     # print(ner_results)
    #     # print("Recognized entities:")
    #     # for result in ner_results:
    #     #     print(result['word'] + " " + result['entity'])
    #     # print("\n################################################################\n\n")
    return ner_results


def use_multinerd_model(input_sentence):

    # config = json.load(open("../../Desktop/EntityLinkingSystem-main/ner/ner_multinerd/model/config.json"))
    # config["label2id"] = {key: str(value) for key, value in ner_dict.items()}
    # config["id2label"] = {value: key for key, value in config["label2id"].items()}
    # json.dump(config, open("../../Desktop/EntityLinkingSystem-main/ner/ner_multinerd/model/config.json", "w"))

    config = json.load(open("bertcasednerd_training/checkpoint-7000/config.json"))
    config["label2id"] = {key: str(value) for key, value in ner_dict.items()}
    config["id2label"] = {value: key for key, value in config["label2id"].items()}
    json.dump(config, open("bertcasednerd_training/checkpoint-7000/config.json","w"))

    model_fine_tuned = AutoModelForTokenClassification.from_pretrained("bertcasednerd_training/checkpoint-7000")
    nlp = pipeline("ner", model=model_fine_tuned, tokenizer=tokenizer)
    ner_results = nlp(input_sentence)

    return ner_results



    # print("\n################   USING MNERD MODEL   ########################")
    # print("\nGiven example sentence:\n" + input_sentence + "\n")
    # print(ner_results)
    # print("Recognized entities:")
    # for result in ner_results:
    #     print(result['word'] + " " + result['entity'])
    # print("\n####################################################################\n\n")


def convert_to_entities(ner_results):
    # list of entities to be returned
    entity_list = []
    curr_entity_class = ""
    # string containing a sum of same entity's tokens resulting in a full word
    curr_word = ""
    curr_word_start_idx = -1
    curr_word_last_idx = -1

    for r in ner_results:
        # check if its continuation of entity therefore
        # if previous entity "B-XYX" or "I-XYX" is followed by "I-XYX"
        if "I" + curr_entity_class[1:] == r['entity']:
            # optionally add space between words
            if r['start'] > curr_word_last_idx:
                curr_word += " "
            # remove '##' added by tokenizer
            if r['word'].startswith("##"):
                curr_word += r['word'][2:]
            else:
                curr_word += r['word']
            curr_word_last_idx = r['end']
        else:
            # return previous entity if one exists
            if curr_entity_class != "":
                entity_list.append(Entity(curr_word, curr_entity_class, (curr_word_start_idx, curr_word_last_idx)))
            # and start building new one
            curr_entity_class = r['entity']
            curr_word = r['word']
            curr_word_start_idx = r['start']
            curr_word_last_idx = r['end']

    # loop skips adding last entity if one exists
    if curr_entity_class != "":
        entity_list.append(Entity(curr_word, curr_entity_class, (curr_word_start_idx, curr_word_last_idx)))

    return entity_list



def run_simple_test():
    examples = ["Bill Gates is the Founder of Microsoft","He was born in New York and hates CD Projekt Red located in Poland",
        "Jordan is a river flowing on the border of two countries.","Jordan is also a basketball player."]

    for e in examples:
        use_conll_model(e)
        use_multinerd_model(e)


def run_test(dataset):
    # data, temp = train_test_split(tokenized_test, train_size=0.01, random_state=42)
    # dataset = datasets.Dataset.from_dict(data)

    model_fine_tuned = AutoModelForTokenClassification.from_pretrained("multinerd2_model")
    data_collator = DataCollatorForTokenClassification(tokenizer)
    training_args = TrainingArguments("test-predictions")
    trainer = Trainer(
        model_fine_tuned,
        data_collator=data_collator
    )
    predictions = trainer.predict(dataset)
    print(compute_metrics(predictions[:2]))


##############################################################################
##############################################################################
##############################################################################

ner_dict2 = {
    "O": 0,
    "B-PER": 1,
    "I-PER": 2,
    "B-ORG": 3,
    "I-ORG": 4,
    "B-LOC": 5,
    "I-LOC": 6,
    "B-MISC": 7,
    "I-MISC": 8,
}

ner_dict = {
    "O": 0,
    "B-PER": 1,
    "I-PER": 2,
    "B-LOC": 3,
    "I-LOC": 4,
    "B-ORG": 5,
    "I-ORG": 6,
    "B-ANIM": 7,
    "I-ANIM": 8,
    "B-BIO": 9,
    "I-BIO": 10,
    "B-CEL": 11,
    "I-CEL": 12,
    "B-DIS": 13,
    "I-DIS": 14,
    "B-EVE": 15,
    "I-EVE": 16,
    "B-FOOD": 17,
    "I-FOOD": 18,
    "B-INST": 19,
    "I-INST": 20,
    "B-MEDIA": 21,
    "I-MEDIA": 22,
    "B-PLANT": 23,
    "I-PLANT": 24,
    "B-MYTH": 25,
    "I-MYTH": 26,
    "B-TIME": 27,
    "I-TIME": 28,
    "B-VEHI": 29,
    "I-VEHI": 30,
    "B-SUPER": 31,
    "I-SUPER": 32,
    "B-PHY": 33,
    "I-PHY": 34
  }

##############################################################################
##############################################################################
##############################################################################


tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")

# tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

tokenized_train, tokenized_validation, tokenized_test = load_and_tokenize_conll()
# tokenized_train, tokenized_validation, tokenized_test = get_tokenized_multinerd()
#print("Training set:\n", tokenized_train, "\nValidation set:", tokenized_validation, "\nTest set:", tokenized_test)

run_training(tokenized_train, tokenized_validation, 2, "distilbert_cased_conll")

# entity_list = convert_to_entities(ner_results)

# run_test(tokenized_test)